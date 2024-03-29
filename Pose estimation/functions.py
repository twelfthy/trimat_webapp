import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import cv2

def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    print(keypoints[0][0][13])
    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 10, (114,38, 249), -1) 

def draw_connections(frame, keypoints, edges, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    color_mapping = {'m': (217,190,42 ),  # Blue for 'm'
                    'c': (217,190,42),   # Green for 'c'
                    'y': (217,190,42)} # Yellow for 'y'
    
    for edge, color in edges.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]
        
        if (c1 > confidence_threshold) and (c2 > confidence_threshold):  
            edge_color = color_mapping.get(color, (0, 0, 0))  # Default to black if color not found in mapping
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), edge_color, 5)


#############
# Order of points: [nose, left eye, right eye, left ear, right ear, left shoulder, right shoulder, left elbow, right elbow, left wrist, right wrist, left hip, right hip, left knee, right knee, left ankle, right ankle]
# 
# index right hip: 12
# index right knee: 14
# index right ankle: 16
#
# index left hip: 11
# index left knee: 13
# index left ankle: 15


def knee_angles(hip, knee, ankle, confidence_thr):

    c1 = hip[2]
    c2 = knee[2]
    c3 = ankle[2]
    angle_degrees = 0
    
    if (c1 > confidence_thr) & (c2 > confidence_thr) & (c3 > confidence_thr):

        hip_coord = hip[:2]*[480, 640]
        knee_coord = knee[:2]*[480, 640]
        ankle_coord = ankle[:2]*[480, 640]

        # Calculate the vectors
        femor = np.array([knee_coord[0] - hip_coord[0], knee_coord[1] - hip_coord[1]])
        tibia = np.array([ankle_coord[0]- knee_coord[0], ankle_coord[1]- knee_coord[1]])
        
        # Calculate the dot product
        dot_product = np.dot(femor, tibia)
        
        # Calculate the magnitudes of the vectors
        magnitude_AB = np.linalg.norm(femor)
        magnitude_BC = np.linalg.norm(tibia)
        
        # Calculate the cosine of the angle
        cosine_angle = dot_product / (magnitude_AB * magnitude_BC)
        
        # Find the angle in radians
        angle_radians = np.arccos(cosine_angle)
        
        # Convert the angle to degrees
        angle_degrees = int(np.degrees(angle_radians))
    
    return angle_degrees


