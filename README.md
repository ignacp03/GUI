# GUI for the KLab

GUI for the analysis of the absorption images in a ultracold quantum gases experiment. 
The app is located in KLabGUI.py. It watches a directory an analizes the data as new images are saved. The main file also contains the design of the main window and integrates the different widgets. 


## Installation Guide

1) Clone the repository
```bash
git clone "url"

```
2) Install python (I am currently using v.3.11.8)

3) Install pip

4) Create new environment. May be usefull using pyenv

5) Activate venv and go to the gui folder.

```bash
pip install .

```

6) Edit KLabGUI.py and set the default folder in the first attribute called defaultFolder. 

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
 

TO DO:

* Pack the code in an .exe


...



### Future Ideas

* Group custom Aux Plots by parameter
* Set a menu where you can choose the specific image to display in Raw and Aux Highlighted in red the ones with fiStatus 1 (?)
* Maybe reload image?
