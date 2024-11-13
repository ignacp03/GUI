import numpy as np
import scipy.signal as spsig
from scipy.optimize import curve_fit
from processing.load import ReadImage



class Meassurement():
    def __init__(self, dark, bright, atoms, meas, magnification, pixelSize = None):
        """
        Initiate the class:
        dark, bright, atoms: path to the respective images
        meas: kind of measurement. (MagTrap, HybridTrap, BEC)
        """
        self.dark_path = dark
        self.bright_path = bright
        self.atoms_path = atoms
        dark_img = ReadImage(dark, fast = True, getCamera=False)
        bright_img = ReadImage(bright, fast = True, getCamera=False)
        atoms_img, self.variables, self.pixelSize, self.camera = ReadImage(atoms, fast = False, getCamera=True)
        if pixelSize is not None: 
            self.pixelSize = pixelSize
        self.effectivePS = pixelSize/magnification
        self.magnification = magnification
        self.meas = meas
        self.ROI_size = calc_ROI(meas, self.effectivePS, self.variables["ToFTime"])
        self.OpDen = self.OD(dark_img, bright_img, atoms_img)
        self.center = self.FindMaximum()




    def OD(self, Idark, Ibright, Iatoms):
        "Computes the optical density"

        Iat = Iatoms-Idark
        I_0 = Ibright-Idark
        I_0 = np.where(np.logical_or(I_0 <= 0, np.isnan(I_0) | np.isinf(I_0)), 1e-10, I_0)
        Iat = np.where(np.isnan(Iat) | np.isinf(Iat), 0, Iat)
        OpDen = -np.log(np.where(Iat / I_0 <= 0, 1e-10, Iat / I_0))
        OpDen = np.where(np.isnan(OpDen) | np.isinf(OpDen), 1e-10, OpDen)
        return OpDen
    
    def cropImage(self, ROI = None, center = None):
        """ 
        Crops the optical density.
        ROI: square 
        """
        im = np.copy(self.OpDen)
        imShape = np.shape(im)
        if ROI is None:
            if self.ROI_size is not None:
                ROI = self.ROI_size
            else:
                return im
            

        if self.center[0]+ROI//2 < imShape[1]: 
            Xmax = self.center[0]+ROI//2
        else: 
            Xmax = imShape[1]

        if self.center[0]-ROI//2 > 0:
            Xmin = self.center[0]-ROI//2
        else:
            Xmin = 0

        if self.center[1]+ROI//2 < imShape[0]: 
            Ymax = self.center[1]+ROI//2
        else: Ymax = imShape[0]
        if self.center[1]-ROI//2 > 3:
            Ymin = self.center[1]-ROI//2
        else: Ymin = 0

        self.ROI = im[Ymin:Ymax, Xmin:Xmax]
        newCx = self.center[0] - Xmin
        NewCy = self.center[1] - Ymin
        self.new_center = (newCx, NewCy)


    def FindMaximum(self):
        " Finds pixel with the maximum value"
        maxpos = np.argmax(smooth2D(self.OpDen,box_pts = 20))
        cy,cx = np.unravel_index(maxpos,self.OpDen.shape)
        self.center = (cx, cy)
        return (cx, cy)
    
    def FitROI(self):
        """
        Fits the ROI (or the opDen if the ROI fails) to a gaussian or a TF depending on the meas variable.
        returns the optimal parameter, the covariance, a fitted image and fitstatus which is 0 if the fit 
        was succesful or 1 otherwise. 
        """
        if self.ROI is not None:
            image = self.ROI
        else: 
            image = self.OpDen

        if self.meas== "MagTrap" or self.meas == "HybridTrap":

            self.popt, self.pcov, self.fitted_image, self.fitStatus = fit_2d_gaussian(image)

        elif self.meas== "BEC":

            self.popt, self.pcov, self.fitted_image, self.fitStatus = fit_2d_thomas_fermi(image)

    def calculateResults(self):
        """
        Calculates temperature(in case of hybrid or magtrap) and atom number
            -Atom number: One can calculate the local density as n(x,y) = OD(x,y)/absorption_cross_section.
                          The N = sum_{x,y} n(x,y)*A_pixel = sum_{x,y} n(x,y) eff_pixel_size**2.
            -Temperature: T = m * effsigma_x*effsigma_y/(TOF**2*kB) = m * (sigma*eff_pixel)**2/(TOF**2*kB)
        """
        cross_section = 3*(767e-9)**2/2/np.pi
        self.results = {}
        if self.fitStatus == 0:
            kB = 1.38e-23
            m = 6.8e-26
            fitted_atom_number = np.sum(self.fitted_image)*self.effectivePS**2/cross_section
            integrated_atom_number = np.sum(self.ROI)*self.effectivePS**2/cross_section
            if self.meas=="MagTrap" or self.meas == "Hybridtrap":
                temp = (self.popt[3]*self.effectivePS)**2*m/kB/self.variables["ToFTime"]**2
            else: 
                temp = 0
            self.results["Fitted Atom Number"] = fitted_atom_number
            self.results["Integrated Atom Number"] = integrated_atom_number
            self.results["Temperature"] = temp
        else: 
            self.results["Fitted Atom Number"] = 0
            self.results["Integrated Atom Number"] = 0
            self.results["Temperature"] = 0
            
    
        
    


######### HELPER FUNCTIONS #############


def smooth2D(y, box_pts):
    box = np.ones([box_pts,box_pts])/box_pts**2
    box /= np.sum(box)
    y_smooth = spsig.fftconvolve(y, box, mode='same')
    return y_smooth

def calc_ROI(meas, effPS, TOF):
    """
    Calculates the optimal ROI based on the kind of measurement
    For this it is assumed: 
        * MagTrap: T = 35 uK, 
        * HybridTrap: T = 1.5 uK
        * BEC: T = 500 nk

    Parameters:
        - meas: str with the kind of measurement (MagTrap, HybridTrap, BEC)
        - effPS: effective pixel size (pixsize/magnification)
        - TOF: time of flight in s.
    Returns:
        - ROI_size:  3 times the width of the thermal cloud
    """
    kB = 1.38e-23
    m = 6.8e-26
    if meas == "MagTrap":
        Tmt = 35e-6
        sigma = np.sqrt(kB*Tmt/m*TOF**2)
        sigmaPixel = sigma/effPS
        return int(sigmaPixel*3)
    
    elif meas == "HybridTrap":
        Tht = 1.5e-6
        sigma = np.sqrt(kB*Tht/m*TOF**2)
        sigmaPixel = sigma/effPS
        return int(sigmaPixel*3)
    
    elif meas == "BEC":
        Tbec = 0.5e-6
        sigma = np.sqrt(kB*Tbec/m*TOF**2)
        sigmaPixel = sigma/effPS
        return int(sigmaPixel*4)
    




########### FITTING FUNCTIONS ###########



def gaussian_2d(xy, amp, xo, yo, sigma_x, sigma_y, theta, offset):
    """
    2D Gaussian function.
    
    Parameters:
    - xy: Tuple of x and y grid arrays (flattened).
    - amp: Amplitude of the Gaussian.
    - xo, yo: x and y center of the Gaussian.
    - sigma_x, sigma_y: Standard deviations along x and y.
    - theta: Rotation angle of the Gaussian.
    - offset: Baseline offset.
    
    Returns:
    - Flattened array of the Gaussian function evaluated at (x, y).
    """
    x, y = xy
    xo = float(xo)
    yo = float(yo)
    a = (np.cos(theta) ** 2) / (2 * sigma_x ** 2) + (np.sin(theta) ** 2) / (2 * sigma_y ** 2)
    b = -(np.sin(2 * theta)) / (4 * sigma_x ** 2) + (np.sin(2 * theta)) / (4 * sigma_y ** 2)
    c = (np.sin(theta) ** 2) / (2 * sigma_x ** 2) + (np.cos(theta) ** 2) / (2 * sigma_y ** 2)
    
    g = offset + amp * np.exp(-(a * (x - xo) ** 2 + 2 * b * (x - xo) * (y - yo) + c * (y - yo) ** 2))
    return g.ravel()

def fit_2d_gaussian(image):
    """
    Fits a 2D Gaussian to the provided image data.
    
    Parameters:
    - image: 2D numpy array representing the image data.
    
    Returns:
    - popt: Optimal parameters for the 2D Gaussian fit.
           [amp, xo, yo, sigma_x, sigma_y, theta, offset]
    - pcov: Covariance of popt.
    - fitted_image
    -exit_code: 0 if succesful fitting, 1 otherwise
    """
    exit_code = 0
    # Generate x and y coordinate arrays
    x = np.arange(0, image.shape[1])
    y = np.arange(0, image.shape[0])
    x, y = np.meshgrid(x, y)
    
    # Flatten the image and coordinate arrays for the fitting function
    xy = (x.ravel(), y.ravel())
    image_flat = image.ravel()
    
    # Initial guess for the Gaussian parameters
    initial_guess = (image.max(), image.shape[1] / 2, image.shape[0] / 2, image.shape[0]/3, image.shape[0]/3, 0, np.min(image))
    
    # Perform the curve fitting
    try:
        popt, pcov = curve_fit(gaussian_2d, xy, image_flat, p0=initial_guess)
        fitted_image = gaussian_2d(xy,*popt)
    except:
        fitted_image = np.zeros((image_flat.shape[0]))
        exit_code +=1
        popt, pcov = None, None

    return popt, pcov, fitted_image.reshape(image.shape), exit_code



def thomas_fermi_2d(xy, amp, xo, yo, radius_x, radius_y, offset):
    """
    2D Thomas-Fermi distribution function (inverted parabola).
    
    Parameters:
    - xy: Tuple of x and y grid arrays (flattened).
    - amp: Amplitude (peak density) of the distribution.
    - xo, yo: Center coordinates of the distribution.
    - radius_x, radius_y: Radii along x and y where the density drops to zero.
    - offset: Baseline offset.
    
    Returns:
    - Flattened array of the Thomas-Fermi distribution evaluated at (x, y).
    """
    x, y = xy
    xo = float(xo)
    yo = float(yo)
    
    # Inverted parabola for TF distribution, zero outside the radius
    r_x = (x - xo) / radius_x
    r_y = (y - yo) / radius_y
    rho = np.maximum(0, amp * (1 - r_x**2 - r_y**2)) + offset
    
    return rho.ravel()

def fit_2d_thomas_fermi(image):
    """
    Fits a 2D Thomas-Fermi distribution to the provided image data.
    
    Parameters:
    - image: 2D numpy array representing the image data.
    
    Returns:
    - popt: Optimal parameters for the 2D Thomas-Fermi fit.
            [amp, xo, yo, radius_x, radius_y, offset]
    - pcov: Covariance of popt.
    - fitted_image
    -exit_code: 0 if succesful fitting, 1 otherwise
    """
    exit_code = 0
    # Generate x and y coordinate arrays
    x = np.arange(0, image.shape[1])
    y = np.arange(0, image.shape[0])
    x, y = np.meshgrid(x, y)
    
    # Flatten the image and coordinate arrays for the fitting function
    xy = (x.ravel(), y.ravel())
    image_flat = image.ravel()
    
    # Initial guess for the Thomas-Fermi parameters
    initial_guess = (
        image.max(),              # Amplitude (peak density)
        image.shape[1] / 2,       # x-center
        image.shape[0] / 2,       # y-center
        image.shape[1] / 4,       # radius_x, half the width of image as initial guess
        image.shape[0] / 4,       # radius_y, half the height of image as initial guess
        np.min(image)             # Offset
    )
    
    # Perform the curve fitting
    try: 
        popt, pcov = curve_fit(thomas_fermi_2d, xy, image_flat, p0=initial_guess, maxfev=10000)
        fitted_image = thomas_fermi_2d(xy,*popt)
    except:
        #Fill the fitted image with 0 in case of fitting failing
        fitted_image = np.zeros((image_flat.shape[0]))
        exit_code += 1 #Updating exit code
    return popt, pcov, fitted_image.reshape(image.shape), exit_code