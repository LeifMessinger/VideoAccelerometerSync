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
	accelerometer_filename = sys.argv[1]

if ".mp4" in sys.argv[2]:
	video_filename = sys.argv[2]

import pandas as pd
import numpy as np
import cv2
import scipy
import VidAccSyn
from math import ceil

#Arlene wrote this part. Modified to use as a function
accelerometer_sample_rate = 10 #ms
def process_sensor_data(filename, fieldnames):
	df_raw = pd.read_csv(filename)

	accelerometer_sample_rate = VidAccSyn.polling_rate(df_raw)

	#expand the fieldnames from the input
	x_field, y_field, z_field = fieldnames

	delta_x = df_raw[x_field].diff().dropna()
	delta_y = df_raw[y_field].diff().dropna()
	delta_z = df_raw[z_field].diff().dropna()

	#Maybe something like np.hypot would be better here instead
	mag_changes_res = np.sqrt(delta_x ** 2 + delta_y ** 2 + delta_z **2 )

	return mag_changes_res

FIELD_NAMES =  'Linear Acceleration x (m/s^2)', 'Linear Acceleration y (m/s^2)', 'Linear Acceleration z (m/s^2)'
processed_sensor_data = process_sensor_data(accelerometer_filename, FIELD_NAMES)

frame_diff = VidAccSyn.stdev_video_to_velocity(path=video_filename)
frame_diff = VidAccSyn.velocity_to_acceleration(frame_diff)

# Resampling
#Video is going to have way less samples than acceleration
video_rate = 30
sensor_rate = 100
signal_rs, video_rs = VidAccSyn.downsample(processed_sensor_data, frame_diff, sensor_rate, video_rate)

cc = scipy.signal.correlate(signal_rs, video_rs, mode='full')

list_cc = list(cc)
max_pos = list_cc.index(max(list_cc))
lag_in_sec = (max_pos - len(signal_rs)) / video_rate

if lag_in_sec < 0:
    print(f'The sensor started ~{abs(lag_in_sec):.3} seconds after the video.')
elif lag_in_sec > 0:
    print(f'The video started ~{abs(lag_in_sec):.3} seconds after the sensor.')