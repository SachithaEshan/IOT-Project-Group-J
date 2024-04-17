import cv2
import numpy as np
from scipy.spatial import distance as dist
from imutils import face_utils
import dlib
import pygame
from threading import Thread
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse

# Initialize Pygame mixer
pygame.mixer.init()

# Function to play sound alarm
def sound_alarm(path):
    # Load the sound file
    pygame.mixer.music.load(path)
    # Play the sound file
    pygame.mixer.music.play()

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
webcam_arg = "http://192.168.1.8/cam-lo.jpg"
log_file_arg = "drowsiness_log.txt"

# Store arguments in the args dictionary
args = {"shape_predictor": shape_predictor_arg, "alarm": alarm_arg, "webcam": webcam_arg, "log_file": log_file_arg}

# Define constants for eye drowsiness detection
EYE_AR_THRESH = 0.23
EYE_AR_CONSEC_FRAMES = 10
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

# Function to log speed and location
def log_speed_location(lat, lng, speed):
    LOG_FILE = 'gps_log.txt'
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp} - Latitude: {lat}, Longitude: {lng}, Speed: {speed}\n")
        print(f"Logged data - {timestamp} - Latitude: {lat}, Longitude: {lng}, Speed: {speed}")

# Function to retrieve speed and location from gps_log file
def retrieve_speed_location(drowsiness_time):
    with open('gps_log.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if drowsiness_time in line:
                # Extract latitude, longitude, and speed from the line
                parts = line.split(' - ')
                gps_data = parts[1]
                gps_parts = gps_data.split(', ')
                latitude = gps_parts[0].split(': ')[1]
                longitude = gps_parts[1].split(': ')[1]
                speed = gps_parts[2].split(': ')[1]
                return latitude, longitude, speed
    return None, None, None

# Speed and location detection server
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_data = urllib.parse.parse_qs(post_data.decode())
        latitude = parsed_data.get('lat')[0]
        longitude = parsed_data.get('lng')[0]
        speed = parsed_data.get('speed')[0]
        log_speed_location(latitude, longitude, speed)
        self.send_response(200)
        self.end_headers()

# Define speed and location detection server function
def run_server(server_class=HTTPServer, handler_class=RequestHandler):
    HOST = '0.0.0.0'
    PORT = 8081
    server_address = (HOST, PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Server listening on {HOST}:{PORT}")
    httpd.serve_forever()

# Start speed and location detection server in a separate thread
t_server = Thread(target=run_server)
t_server.daemon = True
t_server.start()

# Open log file in append mode
log_file = open(args["log_file"], "a")

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
                # Log drowsiness detection time
                drowsiness_time = time.strftime("%Y-%m-%d %H:%M:%S")
                # Retrieve speed and location
                latitude, longitude, speed = retrieve_speed_location(drowsiness_time)
                if latitude is not None and longitude is not None and speed is not None:
                    # Log speed and location to drowsiness_log file
                    log_file.write(f"{drowsiness_time} - Speed: {speed}, Latitude: {latitude}, Longitude: {longitude}\n")
                    log_file.flush()
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

# Release the VideoCapture object, close log file, and close all OpenCV windows
log_file.close()
cv2.destroyAllWindows()
