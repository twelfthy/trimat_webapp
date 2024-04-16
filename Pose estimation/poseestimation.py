import tkinter as tk
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import cv2
import numpy as np
import tensorflow as tf
from functions import draw_keypoints, draw_connections, knee_angles

# Constants and TensorFlow Lite model setup
EDGES = {
    (0, 1): 'm', (0, 2): 'c', (1, 3): 'm', (2, 4): 'c',
    (0, 5): 'm', (0, 6): 'c', (5, 7): 'm', (7, 9): 'm',
    (6, 8): 'c', (8, 10): 'c', (5, 6): 'y', (5, 11): 'm',
    (6, 12): 'c', (11, 12): 'y', (11, 13): 'm', (13, 15): 'm',
    (12, 14): 'c', (14, 16): 'c'
}
THRESHOLD = 0.3
interpreter = tf.lite.Interpreter(model_path='/Users/nicolaspedrazzi/trimat_webapp/Pose estimation/3.tflite')
interpreter.allocate_tensors()

# Open the PDF
doc = fitz.open('/Users/nicolaspedrazzi/trimat_webapp/Pose estimation/first page.pdf')
page = doc.load_page(0)
pix = page.get_pixmap()
img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

# Setup the main window
root = tk.Tk()
background_photo = ImageTk.PhotoImage(image=img)
background_label = tk.Label(root, image=background_photo)
background_label.pack(fill="both", expand=True)  # Ensure it covers the whole window

# Video capture setup
cap = cv2.VideoCapture(0)
desired_width = 192
desired_height = 192
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

video_label = tk.Label(root)  # Label to display the video
video_label.place(x=192, y=300)  # Adjust this position to match the gray area

def process_frame(frame):
    # Resize and preprocess the frame for TensorFlow Lite model
    img = tf.image.resize_with_pad(np.expand_dims(frame, axis=0), 192, 192)
    input_image = tf.cast(img, dtype=tf.float32)

    # TensorFlow Lite processing
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
    interpreter.invoke()
    keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])

    # Draw keypoints and connections
    draw_connections(frame, keypoints_with_scores, EDGES, THRESHOLD)
    draw_keypoints(frame, keypoints_with_scores, THRESHOLD)

    # Calculate and display knee angles
    left_knee_angle, right_knee_angle = calculate_knee_angles(keypoints_with_scores)

    # Add text overlays
    cv2.putText(frame, f"Left knee angle: {left_knee_angle}", (50, 920), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)
    cv2.putText(frame, f"Right knee angle: {right_knee_angle}", (50, 1000), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)

    return frame

def calculate_knee_angles(keypoints_with_scores):
    # Extract keypoints for angle calculation
    left_hip = keypoints_with_scores[0][0][11]
    left_knee = keypoints_with_scores[0][0][13]
    left_ankle = keypoints_with_scores[0][0][15]
    right_hip = keypoints_with_scores[0][0][12]
    right_knee = keypoints_with_scores[0][0][14]
    right_ankle = keypoints_with_scores[0][0][16]

    # Calculate angles
    left_knee_angle = knee_angles(left_hip, left_knee, left_ankle, THRESHOLD)
    right_knee_angle = knee_angles(right_hip, right_knee, right_ankle, THRESHOLD)

    return left_knee_angle, right_knee_angle

def update_video():
    ret, frame = cap.read()
    if ret:
        processed_frame = process_frame(frame)
        cv_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(cv_frame))
        video_label.config(image=photo)
        video_label.image = photo  # Keep a reference to avoid garbage collection
        root.after(10, update_video)  # Schedule the next frame update

update_video()
root.mainloop()

# Cleanup
cap.release()
cv2.destroyAllWindows()
