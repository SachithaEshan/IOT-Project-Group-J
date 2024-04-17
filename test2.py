import cv2
import numpy as np
from scipy.spatial import distance as dist
from imutils import face_utils
import dlib
import playsound
from threading import Thread
import time
import urllib.request

# Function to play sound alarm
def sound_alarm(path):
    playsound.playsound(path)

# Function to calculate eye aspect ratio
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Define arguments
shape_predictor_arg = "shape_predictor_68_face_landmarks.dat"
alarm_arg = "alarm.wav"
webcam_arg = "http://192.168.96.88/cam-lo.jpg"

# Store arguments in the args dictionary
args = {"shape_predictor": shape_predictor_arg, "alarm": alarm_arg, "webcam": webcam_arg}

# Define constants for eye drowsiness detection
EYE_AR_THRESH = 0.23
EYE_AR_CONSEC_FRAMES = 5
COUNTER = 0
ALARM_ON = False

# Load facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# Grab the indexes of the facial landmarks for the left and right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Create a named window
cv2.namedWindow("live Cam Testing", cv2.WINDOW_AUTOSIZE)

# Create a VideoCapture object
cap = cv2.VideoCapture(args["webcam"])

# Check if the IP camera stream is opened successfully
if not cap.isOpened():
    print("Failed to open the IP camera stream")
    exit()

# Read and display video frames
while True:
    # Read a frame from the video stream
    img_resp = urllib.request.urlopen(args["webcam"])
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    im = cv2.imdecode(imgnp, -1)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    rects = detector(gray, 0)

    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # Extract left and right eye coordinates
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        # compute the convex hull for the left and right eye, then visualize each of the eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(im, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(im, [rightEyeHull], -1, (0, 255, 0), 1)

        # Check for drowsiness
        if ear < EYE_AR_THRESH:
            COUNTER += 1
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                if not ALARM_ON:
                    ALARM_ON = True
                    # Sound the alarm
                    if args["alarm"] != "":
                        t = Thread(target=sound_alarm, args=(args["alarm"],))
                        t.deamon = True
                        t.start()
                    # Print message
                    print("DROWSINESS DETECTED!")
                    # Draw drowsiness alert on the frame
                    cv2.putText(im, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            COUNTER = 0
            ALARM_ON = False

        # Draw EAR on the frame
        cv2.putText(im, "EAR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('live Cam Testing', im)

    # Check for 'q' key press to exit
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the VideoCapture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
