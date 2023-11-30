#Per fal na:    python3 "/Users/oliviergianoli/Desktop/Project TriMax/Codes/python/4_points_recognition/heatmap.py"

import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# Define the serial port and baud rate for the Arduino
ser = serial.Serial('/dev/cu.usbserial-1420', 9600)

# Create a figure and a heatmap subplot
fig, ax = plt.subplots()
heatmap = ax.imshow(np.zeros((32, 32)), cmap='plasma', vmin=0, vmax=100, interpolation='nearest')

# Set the heatmap colorbar
plt.colorbar(heatmap)

# Initialize an empty matrix
matrix = np.zeros((32, 32))

# Function to update the heatmap data
def update_heatmap(frame):
    global matrix
    # Read the 8x8 matrix from Arduino
    matrix_str = ser.readline().decode().strip()
    new_matrix = np.array([int(value) for value in matrix_str.split(',')])

    # print(new_matrix)
    # Update the individual elements of the matrix with the new values
    matrix = np.reshape(new_matrix, (32,32))
    # print(matrix)

    # Update the heatmap with the new matrix values
    heatmap.set_data(matrix)
    return heatmap,

# Create an animation
ani = FuncAnimation(fig, update_heatmap, interval=100, blit=True)


plt.show()



#old code:

# import serial
# import numpy as np
# import matplotlib.pyplot as plt
# import keyboard

# col = 8
# row = 8

# # Define the serial port and baud rate for the Arduino
# ser = serial.Serial('/dev/cu.usbserial-14310', 9600)
# # Create a figure and a heatmap subplot
# fig, ax = plt.subplots()
# heatmap = ax.imshow(np.zeros((8,8)), cmap='plasma', vmin=0, vmax=300)

# # Set the heatmap colorbar
# plt.colorbar(heatmap)

# # Continuously read and update the heatmap
# while True:
#     # Read the 8x8 matrix from Arduino
#     matrix_str = ser.readline().decode().strip()
    
#     matrix = np.array([[int(x) for x in row.split(',')] for row in matrix_str.split('\n')])
#     matrix = matrix.reshape((8, 8))

#     # Update the heatmap with the new matrix values
#     # print(matrix)
#     heatmap.set_data(matrix)

#     # if keyboard.is_pressed('space'):
#     #     break
    
#     plt.draw()
#     plt.pause(0.001)
