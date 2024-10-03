# VideoAccelerometerSync
Cross correlation between video and an accelerometer

90% of the code was done by someone named Usha.

## Installation

1. Download visual studio code, if you haven't already.
2. Clone this repository.
3. Open `PrototypeCode.ipynb` in visual studio code.

   Visual studio code might give you a popup to install things like python and jupyter. Click yes to all of those when they show up.

4. Do Ctrl Shift P, search for and click `Python: Create Environment`
5. Click '.venv' (This step is pretty important, as conda gives worse results somehow)
6. It should prompt you to click on requirements.txt. Check requirements.txt.
   - If it doesn't, you'll have to do `pip install -r requirements.txt` in the terminal to install all of the required packages later.
7. Ctrl Shift P, search for and click `Notebook: Select Notebook Kernel`
8. Click the option with '.venv'
   - If it doesn't show, try restarting visual studio code.

## Running

1. Move the video data and CSV data into the folder with the `PrototypeCode.ipynb`

   Please ensure that the VidAccSyn.py file is in this folder as well.

4. Replace `video_filename`and `sensor_filename` with the paths to the video file and `.csv` file respectively.
5. Click `▶️Run All` at the top of the notebook.
6. Scroll down to view the results.
