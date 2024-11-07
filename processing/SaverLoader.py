from processing.ImgProc import Meassurement
import pickle as pkl
import os

def saveData(data:Meassurement, identifier, folderPath):
    """
    Save the data after being processed by ImgProc in processedData.pkl file. 
    If the file exists, the new data is appended to the end of the file.
    If the file doesn't exist, a new one is created. 
    The data is saved in a dictionary with the most important info. 

    inputs: 
        *data [measurement]: data after processing
        *identifier [int]: identifier of the repetition number 
        *folderPath [str]: path where the images were saved
    
    """

    other = {}
    other["OpDen"] = data.OpDen
    other["Center"] = data.center
    other["popt"] = data.popt
    other["pcov"] = data.pcov

    dataSet = {}
    dataSet["Identifier"] = identifier
    dataSet["Fitted_Image"] = data.fitted_image
    dataSet["fitStatus"] = data.fitStatus
    dataSet["ROI"] = data.ROI
    dataSet["Results"] = data.results
    dataSet["Other"] = other

    fileName = "processedData.pkl"
    full_path = os.path.join(folderPath, fileName)

    if os.path.exists(fileName):
        #if the file exists
        with open(full_path, 'rb+') as f:
            try: #Tries to load the data
                f.seek(0)
                existing_data = pkl.load(f)
            except EOFError: #If the file exist but there is no data
                existing_data = []
            existing_data.append(dataSet)
            f.seek(0)
            pkl.dump(existing_data, f)
    else:
        # If the file doesn't exist, create it and write the data
        with open(full_path, 'wb') as f:
            pkl.dump([dataSet], f)



def LoadData(folderPath):
    """
    Loads data from the file processedData.pkl as a list whith the different shots.

    Input: 
        *folderPath[str]: path of the folder where the data is saved.
    Output: 
        data[list]: list with dictionaries containing the data. 
    """
    fileName = "processedData.pkl"
    full_path = os.path.join(folderPath, fileName)
    with open(full_path, 'rb') as f:
        try:
            data = pkl.load(f)
        except: 
            data = None
    
    return data