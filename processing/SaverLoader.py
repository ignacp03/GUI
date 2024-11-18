from processing.ImgProc import Meassurement
import pickle as pkl
import sqlite3

def saveData(data:Meassurement, identifier, full_path):
    """
    Save the data after being processed by ImgProc in processedData.db file. 
    If the file exists, the new data is appended to the end of the file.
    If the file doesn't exist, a new one is created. 
    The data is saved in a dictionary with the most important info. 

    inputs: 
        *data [measurement]: data after processing
        *identifier [int]: identifier of the repetition number 
        *full_path [str]: path where the images were saved
    
    """

    other = {}
    other["OpDen"] = data.OpDen
    other["Center"] = data.center
    other["New Center"] = data.new_center
    other["popt"] = data.popt
    other["pcov"] = data.pcov

    paths = {}

    paths["Dark"] = data.dark_path
    paths["Bright"] = data.bright_path
    paths["Atoms"] = data.atoms_path

    dataSet = {}
    dataSet["Identifier"] = identifier
    dataSet["Fitted_Image"] = data.fitted_image
    dataSet["fitStatus"] = data.fitStatus
    dataSet["ROI"] = data.ROI
    dataSet["Variables"] = data.variables
    dataSet["Results"] = data.results
    dataSet["Paths"] = paths
    dataSet["Other"] = other

    saveDataToDB(dataSet, full_path)

    
def saveDataToDB(data_dict, dbPath='processedData.db'):
    """
    Save a dictionary as a serialized BLOB to an SQLite database.
    
    Parameters:
        * data_dict [dict]: The dictionary to store.
        * identifier [int]: A unique identifier for the data set.
        * dbPath [str]: The path to the SQLite database.
    """
    # Connect to the database (creates it if it doesn't exist)
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    
    # Create a table if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data BLOB
        )
    ''')
    
    # Serialize the dictionary using pickle
    serialized_data = pkl.dumps(data_dict)
    
    # Insert the serialized data
    cursor.execute('INSERT OR REPLACE INTO data (data) VALUES (?)', ( serialized_data, ))
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

def LoadData(dbPath='processedData.db', load_all = True):
    """
    Load all data from the SQLite database and return as a list of dictionaries.
    
    Parameters:
        * dbPath [str]: The path to the SQLite database.
        
    Returns:
        * List[dict]: A list containing dictionaries of data sets.
    """
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    
    if load_all:
        # Select all rows in the data table
        cursor.execute('SELECT data FROM data')
        rows = cursor.fetchall()
    
        # Deserialize each row and add it to the list
        data_list = [pkl.loads(row[0]) for row in rows]

    else:
        # Select only the last row
        cursor.execute('SELECT data FROM data ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        # Deserialize the row and create a list with a single element
        data_list = pkl.loads(row[0]) if row else []
    
    conn.close()
    return data_list
