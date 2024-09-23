import numpy as np
import cv2

def optical_flow(frame, prev_frame):
    # Convert the frame to grayscale
    # I actually don't know why this step is needed.
    frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prev_frame_grey = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # Calculate absolute difference between frames
    return cv2.calcOpticalFlowFarneback(prev_frame_grey, frame_grey, None, 0.5, 3, 15, 3, 5, 1.2, 0)

def optical_flow_magnitudes(frame, prev_frame):
    of = optical_flow(frame, prev_frame)
    mag = np.hypot(of[..., 0], of[..., 1])
    return mag

#Best
def stdev_signal(frame, prev_frame):
    return np.std(optical_flow_magnitudes(frame, prev_frame))

def stdev_video_to_velocity(**kwargs):
    return video_to_signal(stdev_signal, **kwargs)

#It's pretty good
def mean_signal(frame, prev_frame):
    return np.std(optical_flow_magnitudes(frame, prev_frame))

def mean_video_to_velocity(**kwargs):
    return video_to_signal(stdev_signal, **kwargs)

#Code by Usha to process the video and calculate the difference between frames
def video_to_signal(signal_from_frames=stdev_signal, **kwargs):
    capture = None

    #Handle kwargs
    for key, value in kwargs.items():
        match key:
            case 'capture':
                capture = value
            case 'path':
                capture = cv2.VideoCapture(value)

    if not capture.isOpened():
        import sys
        sys.exit("Error: Could not open video.")

    # Read the first frame
    ret, prev_frame = capture.read()

    frame_diffs = []

    from tqdm import tqdm
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    with tqdm(total=total_frames) as progress_bar:
        while True:
            ret, frame = capture.read()
            if not ret:
                break

            frame_diffs.append(signal_from_frames(frame, prev_frame))

            # Update the previous frame
            prev_frame = frame
            progress_bar.update(1)

    capture.release()

    return frame_diffs

def velocity_to_acceleration(velocity_array):
    #We don't know if positive is up or down for the accelerometer
    #and the same for the other directions
    #so we can't do negative values (unless we wanted to cross correlate the array * -1 again)

    #Just abs value it.
    return np.abs(np.gradient(velocity_array))

#accelerometer_data is the pandas dataframe of the accelerometer csv. It should have Time (s) as the first column
#returns miliseconds
def polling_rate(accelerometer_data):
    return np.average(np.diff(accelerometer_data["Time (s)"].values)) * 1000

def resample(arr, newSize):
    return np.interp(
        np.linspace(0, len(arr) - 1, newSize),
        np.arange(len(arr)),
        arr
    )

def downsample(sensor_data, video_data, sensor_rate, video_rate):

    # Finding downsampling rate by setting higher frequency to the lower frequency
    max_rate = max(sensor_rate, video_rate)
    min_rate = min(sensor_rate, video_rate)
    downsampling = max_rate / min_rate

    # Resampling higher frequency
    if sensor_rate > video_rate:
        signal_rs = np.interp(np.arange(0, len(sensor_data), downsampling), np.arange(len(sensor_data)), sensor_data)
        video_rs = video_data
    elif sensor_rate < video_rate:
        signal_rs = sensor_data
        video_rs = np.interp(np.arange(0, len(video_data), downsampling), np.arange(len(video_data)), video_data)

    # Padding to ensure same amount of data points (necessary for cross-correlation)
    if len(video_rs) > len(signal_rs): 
        signal_rs_new = np.pad(signal_rs, (0, len(video_rs) - len(signal_rs)))
        video_rs_new = video_rs
    elif len(video_rs) < len(signal_rs):
        video_rs_new = np.pad(video_rs, (0, len(signal_rs) - len(video_rs)))
        signal_rs_new = signal_rs

    return signal_rs_new, video_rs_new