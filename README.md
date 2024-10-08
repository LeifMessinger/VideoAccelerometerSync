# VideoAccelerometerSync
Finding cross-correlation lag in seconds between video and an accelerometer for alignment.

Most of the code was originally done by someone named Usha.

AI in Healthcare and Wearables Contributors:
- Isaac Gregory
- Leif Messinger
- Parth Bhanderi
- Shiny Shamma Kota

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

## Code Explanation

The code involved runs through a few steps in order to find the lag. This mainly includes some preprocessing done prior to the actual cross-correlation.

### Sensor Processing

The program is currently setup to read in accelerometer data as a CSV. It takes the x, y, and z values and obtains the magnitude from the three directions combined. This takes place in the process_sensor_data function.

### Video Processing

In order for the video to be processed into a signal, a few steps are required. The original code, though updated by us to use optical flow, that is still present in the ipynb is in the function called video_to_graph. There the mean of the flows' magnitudes is used as the velocity. However, our implementation instead uses the standard deviation, as this accounts for camera shake. 

1. Each frame is looped through
2. The frame and previous frame are converted to gray-scale images, so that only the intensity values are being observed in each
3. Optical Flow is calculated on the data
4. The standard deviation of the points is calculated
5. The value is saved in a list
6. The absolute gradient is then calculated for the points in the list, to convert from velocity to acceleration

### Resampling

Once the two signals are officially obtained, the next step is to synchronize their frequency and lengths for the cross-correlation function. This is because the cross-correlation function takes in the values as lists, with no reference to how those values are distributed. Therefore, the assumption is that the rates and lengths would be near-equivalent. To accomplish this, the higher sampling rate between the video and the sensor is downsampled to the other's rate, or as close as possible. Most of the time this means the sensor is downsampled to the video's FPS. This is done using the np.interp function. The sample with a lower number of values is then padded with zeros (i.e. zeros are added to the list) in order to match the lists' lengths. This, then, will allow the cross-correlation function to work properly.

### Cross-Correlation

Cross-correlation is simple in this program in that it is just a function call from the SciPy library. The function will return a list of cross-correlation values where the theoretical "best-match" is at the highest value. Therefore, the highest value is used as the final prediction, where negative and positive decide whether the video or the sensor started first. Optionally, the top few cross-correlation values may provide additional insights that the single highest prediction does not. Mainly, it could show that there are some other similar options that may actually be correct, but the signals were too noisy. 

### Considering Log

Taking the log of the both signal values further helps the alignment of the signals due to scaling them down similarly. 
