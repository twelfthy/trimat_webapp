#Per fal na:    python3 "/Users/oliviergianoli/Desktop/Project TriMax/Codes/python/4_points_recognition/heatmap.py"

import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# Define the serial port and baud rate for the Arduino
ser = serial.Serial('/dev/cu.usbserial-144310', 9600)

# Create a figure and a heatmap subplot
fig, ax = plt.subplots()
heatmap = ax.imshow(np.zeros((16, 16)), cmap='plasma', vmin=0, vmax=150, interpolation='nearest')

# Set the heatmap colorbar
plt.colorbar(heatmap)

# Initialize an empty matrix
matrix = np.zeros((16, 16))

# Function to update the heatmap data
def update_heatmap(frame):
    global matrix
    # Read the 8x8 matrix from Arduino
    matrix_str = ser.readline().decode().strip()
    new_matrix = np.array([int(value) for value in matrix_str.split(',')])

    # print(new_matrix)
    # Update the individual elements of the matrix with the new values
    matrix = np.reshape(new_matrix, (16,16))
    # print(matrix)

    # Update the heatmap with the new matrix values
    heatmap.set_data(matrix)
    return heatmap,

# Create an animation
ani = FuncAnimation(fig, update_heatmap, interval=10, blit=True)


plt.show()