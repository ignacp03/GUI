import os
import time
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from processing.ImgProc import Meassurement
from processing.SaverLoader import saveData



def process_images(dark_img_path, bright_img_path, atoms_img_path, meas, magnification, pixelSize, savefile):
    """
    Function for imaging processing.
    1) Uses the path of the Dark Bright and Atoms images to initiate the Measurement class (processing.ImgProc)
    2) Process: crops ROI, Fits iamge, calculate atom number
    3) saves the data in the same folder than the images

    Inputs:
        * Image paths
        * meas [string] = kind of measurement (MagTrap, HybridTrap, BEC)
        * magnification [float] = magnification of the imagig system
        *pixelSize [float] = pixel size in m

    """
    #print("Processing images:")
    #print(f"Dark: {dark_img_path}")
    #print(f"Bright: {bright_img_path}")
    #print(f"Atoms: {atoms_img_path}")
    data = Meassurement(dark_img_path, bright_img_path, atoms_img_path, meas, magnification, pixelSize)
    data.cropImage()
    data.FitROI()
    data.calculateResults()
    print("Image processed successfully. Saving...")
    filename = os.path.basename(atoms_img_path)
    match = re.search(r'_(\d+)\.png$', filename)
    if match:
        # Return the numeric identifier as an integer
        identifier =  int(match.group(1))
    else:
        # Return 0 if no identifier is present
        identifier = 0

    folderPath = os.path.dirname(atoms_img_path)
    full_path = os.path.join(folderPath, savefile)
    saveData(data, identifier, full_path)
    print("Data saved in: "+full_path)






class ImageSetHandler(FileSystemEventHandler):
    def __init__(self, parent_folder, savefile, meas, magnification, pixelSize = None):
        self.parent_folder = parent_folder
        self.meas = meas
        self.magnification = magnification
        self.pixelSize = pixelSize
        self.savefile = savefile
        self.image_sets = {}  # Dictionary to store sets of images for each subfolder

    def on_created(self, event):
        # Check if the created file is an image
        if event.is_directory:
            return

        file_name = os.path.basename(event.src_path)
        folder_path = os.path.dirname(event.src_path)

        # Check if the file name contains one of the required identifiers
        if any(keyword in file_name for keyword in ["Dark", "Bright", "Atoms"]):
            # Initialize tracking for this folder if not already done
            if folder_path not in self.image_sets:
                self.image_sets[folder_path] = {"Dark": None, "Bright": None, "Atoms": None}

            # Update the tracking dictionary with the new file
            if "Dark" in file_name:
                self.image_sets[folder_path]["Dark"] = event.src_path
            elif "Bright" in file_name:
                self.image_sets[folder_path]["Bright"] = event.src_path
            elif "Atoms" in file_name:
                self.image_sets[folder_path]["Atoms"] = event.src_path

            # Check if all three images are available
            if all(self.image_sets[folder_path].values()):
                # Load and process images
                dark_img = self.image_sets[folder_path]["Dark"]
                bright_img = self.image_sets[folder_path]["Bright"]
                atoms_img = self.image_sets[folder_path]["Atoms"]
                print("!!! New set of images detected. Processing... !!!")

                process_images(dark_img, bright_img, atoms_img,  self.meas, self.magnification, self.pixelSize, self.savefile)

                # Reset the tracking for this folder after processing
                self.image_sets[folder_path] = {"Dark": None, "Bright": None, "Atoms": None}



# Set up the observer
def monitor_folder(parent_folder):
    event_handler = ImageSetHandler(parent_folder)
    observer = Observer()
    observer.schedule(event_handler, path=parent_folder, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
