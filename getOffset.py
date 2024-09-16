# Returns the offset between the accelerometer and the video
# Call like:
# python3 getOffset.py [video] [accelerometer_data]
import sys
if(len(sys.argv) != 3):
	#It's amazing. Python strips out `python3` from the argv, so it's just getOffset.py, video, and accelerometer
	#print(sys.argv)

	sys.exit("Incorrect number of args.\nCall like python3 getOffset.py [video] [accelerometer_data]")

accelerometer_filename = sys.argv[2]
video_filename = sys.argv[1]

#Allow some spoonerism
if ".csv" in sys.argv[1]:
	accelerometer_file_path = sys.argv[1]

if ".mp4" in sys.argv[2]:
	video_file_path = sys.argv[2]

import pandas as pd
import numpy as np
import cv2
import scipy
import VidAccSyn

#Arlene wrote this part. Modified to use as a function
def process_sensor_data(filename, fieldnames):
	df_raw = pd.read_csv(filename)

	#expand the fieldnames from the input
	x_field, y_field, z_field = fieldnames

	delta_x = df_raw[x_field].diff().dropna()
	delta_y = df_raw[y_field].diff().dropna()
	delta_z = df_raw[z_field].diff().dropna()

	#Maybe something like np.hypot would be better here instead
	mag_changes_res = np.sqrt(delta_x ** 2 + delta_y ** 2 + delta_z **2 )

	return mag_changes_res

FIELD_NAMES =  'Linear Acceleration x (m/s^2)', 'Linear Acceleration y (m/s^2)', 'Linear Acceleration z (m/s^2)'
processed_sensor_data = process_sensor_data("walk.csv", FIELD_NAMES)

frame_diff = VidAccSyn.stdev_video_to_velocity(path=video_filename)
frame_diff = VidAccSyn.velocity_to_acceleration(frame_diff)

# Resampling
#resample both signals using the scipy.signal.resample function
#use the longer signal (sensor) as the length
max_len = max(len(processed_sensor_data), len(frame_diff))
resample_size = max_len
signal_rs = scipy.signal.resample(processed_sensor_data, resample_size)
video_rs = scipy.signal.resample(frame_diff, resample_size)

cc = scipy.signal.correlate(signal_rs, video_rs, mode='full')

list_cc = list(cc)
#print(max(list_cc))
#print(list_cc.index(max(list_cc)))
max_pos = list_cc.index(max(list_cc))
lag = max_pos - resample_size
#print(f'lag at the max correlation is: {lag} (ms)')
print(lag)