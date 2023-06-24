# Import libraries
import cv2
import numpy as np

# Define constants
BUFFER_SIZE = 150 # Number of frames to store in buffer
FPS = 30 # Frames per second of the video
FL = 0.8 # Lower frequency of the band pass filter (in Hz)
FH = 3 # Higher frequency of the band pass filter (in Hz)
MIN_FACE_SIZE = 100 # Minimum size of face to detect (in pixels)

# Create a face detector using Haar cascade classifier
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Create a video capture object to read from webcam
video_capture = cv2.VideoCapture(0)

# Check if video capture is opened
if not video_capture.isOpened():
    print("Error: Cannot open video capture")
    exit()

# Create an empty buffer to store the mean color values of ROI
buffer = np.zeros((BUFFER_SIZE, 3))

# Create a window to display the video
cv2.namedWindow('Video')

# Loop until 'q' key is pressed
while True:
    # Read a frame from the video capture
    ret, frame = video_capture.read()

    # Check if frame is read correctly
    if not ret:
        print("Error: Cannot read frame")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame using face detector
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(MIN_FACE_SIZE, MIN_FACE_SIZE))

    # Loop over the detected faces
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Get the region of interest (ROI) from the frame
        roi = frame[y:y + h, x:x + w]

        # Calculate the mean color value of ROI for each channel (BGR)
        mean_color = np.mean(roi, axis=(0, 1))

        # Append the mean color value to the buffer and remove the oldest one
        buffer = np.roll(buffer, -1, axis=0)
        buffer[-1] = mean_color

        # Apply a band pass filter to the buffer to remove noise and DC component
        freqs = np.fft.rfftfreq(BUFFER_SIZE) * FPS # Frequency axis for FFT
        mask = (freqs >= FL) & (freqs <= FH) # Mask for the band pass filter
        fft = np.fft.rfft(buffer, axis=0) # FFT of the buffer
        fft[~mask] = 0 # Apply the mask to the FFT
        filtered_buffer = np.fft.irfft(fft, axis=0) # Inverse FFT of the filtered FFT

        # Calculate the heart rate from the filtered buffer by finding the peak frequency
        peak_freqs = np.argmax(np.abs(fft[mask]), axis=0) # Peak frequency indices for each channel
        heart_rate = freqs[mask][peak_freqs] * 60 # Heart rate for each channel (in BPM)
        heart_rate_mean = np.mean(heart_rate) # Mean heart rate across channels

        # Display the heart rate on the frame
        cv2.putText(frame, f'Heart rate: {heart_rate_mean:.1f} BPM', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Display the frame on the window
    cv2.imshow('Video', frame)

    # Wait for a key press for 1 ms
    key = cv2.waitKey(1)

    # Break the loop if 'q' key is pressed
    if key == ord('q'):
        break

# Release the video capture object and close all windows
video_capture.release()
cv2.destroyAllWindows()
