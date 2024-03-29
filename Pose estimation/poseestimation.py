import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import cv2

from functions import draw_keypoints, draw_connections, knee_angles


interpreter = tf.lite.Interpreter(model_path='/Users/andreasantoro/trimat_webapp/Pose estimation/3.tflite')
interpreter.allocate_tensors()
EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}

THRESHOLD = 0.3


cap = cv2.VideoCapture(0)
desired_width = 192
desired_height = 192
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

while cap.isOpened():
    ret, frame = cap.read()
    
    # Reshape image
    img = frame.copy()
    img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 192,192)
    input_image = tf.cast(img, dtype=tf.float32)
    
    # Setup input and output 
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Make predictions 
    interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
    interpreter.invoke()
    keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
    
    # index right hip: 12
    right_hip = keypoints_with_scores[0][0][12]
    # index right knee: 14
    right_knee = keypoints_with_scores[0][0][14]
    # index right ankle: 16
    right_ankle = keypoints_with_scores[0][0][16]
    #
    # index left hip: 11
    left_hip = keypoints_with_scores[0][0][11]
    # index left knee: 13
    left_knee = keypoints_with_scores[0][0][13]
    # index left ankle: 15
    left_ankle = keypoints_with_scores[0][0][15]

    # Rendering
    draw_connections(frame, keypoints_with_scores, EDGES, THRESHOLD)
    draw_keypoints(frame, keypoints_with_scores, THRESHOLD)

    left_knee_angle = knee_angles(left_hip,left_knee,left_ankle, THRESHOLD)
    right_knee_angle = knee_angles(right_hip,right_knee, right_ankle, THRESHOLD)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    cv2.putText(img= frame, 
                text= f"Left knee angle: {left_knee_angle}", 
                org= (50, 920), 
                fontFace=1, 
                fontScale = 2, 
                color = (0, 0, 0),  
                thickness=4)
    
    cv2.putText(img= frame, 
                text= f"Right knee angle: {right_knee_angle}", 
                org= (50, 1000), 
                fontFace=1, 
                fontScale = 2, 
                color = (0, 0, 0),  
                thickness=4)
    
    cv2.rectangle(img=frame, pt1=(200, 50), pt2=(1100, 150), color=(0, 0, 0), thickness=-1)
    
    if left_knee_angle > 85 and left_knee_angle < 95:
         cv2.putText(img= frame, 
                text= "CORRECT POSITION!", 
                org= (250, 120), 
                fontFace=1, 
                fontScale = 4, 
                color = (0, 128, 0),  
                thickness=4)

    cv2.imshow('TriMat Pose Estimation', frame)
    
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()


