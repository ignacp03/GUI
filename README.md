# GUI for the KLab

GUI for the analysis of the absorption images in a ultracold quantum gases experiment. 
The app is located in KLabGUI.py. It watches a directory an analizes the data as new images are saved. The main file also contains the design of the main window and integrates the different widgets. 


## Installation Guide

More detailed guide [here](#detailed-installation-guide). 

1) Clone the repository

2) Install python (I am currently using v.3.11.8)

3) Create new environment. May be usefull using pyenv

4) Activate venv and install the GUI.

5) Edit KLabGUI.py and set the default folder in the first attribute called defaultFolder. 

## Widgets Folder

Contains the four main widgets in the main window and the toolbar. Also some helpers. 

### ImageVisualization.py

When a new image is processed it displays that. There are some display options and a box that allows displaying different plots.

### MainPlot.py

Processes and analizes the atom number. One can select between Fitted and Integrated atom number, and also select the limits. When the shots \\
are varying a specific parameter, they appear as an option to group by. 

### AuxiliarPlots.py

By default shows the fit but there are some other options availables. Also one can customize the variables plotted in the x and y axes.

### LogConsole.py

Displays info of the workflow of the GUI. Has an open input that can be use to interact with the GUI. It has not been expoited yet, one can add commands and their \\
function at the end of the file. 

## Processing Folder

Contains the main tools for the processing of the images.

### load.py

Most basic tool to load the metadata of the images. It returns the variables as a dictionary, the pixel size and the camera, together with the images.

### ImgProc.py

This is the core of the processing. It evaluates the optical density, finds the center of the cloud, cuts the ROI and performs the fitting. Also it extracts the results.

### SaverLoader.py

Contains two function to save and load the data. It saves the data to a file called processedData.pkl as a list where each item is a dictionary with the main info about a image. 

### Watcher.py

It is in charge of monitoring the parent folder and trigger the analysis when a new set of images are detected.
 





# Detailed Installation Guide

1) First one neeed to install python. A version newer than 3.11.8 should suffice, but you can install that one for full compatibility (https://www.python.org/downloads/release/python-3118/). When installing, I would recommend to not add python to the path to avoid interfering with previously installed versions. Note the installation path (on Windows it usually is "C:\Users\[user]\AppData\Local\Programs\Python\Python311\python.exe" )

2) Now we need to create a virtual environment. One could create them in a folder where all Venvs are stored or in the same folder than the repository. Open windows powershell:

```bash
"Path\to\Python 3.11\python.exe" -m venv "Path\to\Venv\Name_Of_Venv" 
```
For instance, in the installation on PC1281 the GUI repository is cloned on E:\Experiment\KLabGUI. Therefore:

```bash
C:\Users\lab-qge\AppData\Local\Programs\Python\Python311\python.exe -m venv E:\Experiment\KLabGUI\KLabGUI_venv 
```

3) install the repository on the virtual environment. One can run setup.py or via pip install .

```bash
"Path\to\Venv\Name_Of_Venv\Scripts\activate" 
cd "Path\to\repository"
pip install .
```

Example on PC 1281:

```bash
E:\Experiment\KLabGUI\KLabGUI_venv\Scripts\activate 
cd E:\Experiment\KLabGUI\GUI-main
pip install .
```


4) Right now one can launch the app by activating the virtual environment. To easy the launching one can create a script for this and create a shortcut. For this, lauch notepad or a text editor. Write

```bash
# Activate the virtual environment
& ""Path\to\Venv\Name_Of_Venv\Scripts\Activate.ps1"

# Run the GUI
python "Path\to\Repo\KLabGUI.py"
```
and save it as a "Name.ps1". It can be stored anywhere, for example on the GUI folder. 

Then move to the folder when one wants to have the shortcut. Right click, new, shortcut. Then, on "location on the item" one must type:

C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File "Path\to\.ps1"

Right click on the shortcut, under properties one can change the icon. 




### Future Ideas

* Group custom Aux Plots by parameter
* Set a menu where you can choose the specific image to display in Raw and Aux Highlighted in red the ones with fiStatus 1 (?)
* Maybe reload image?
