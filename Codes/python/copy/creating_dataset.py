from PIL import Image, ImageDraw

# Load the image
img = Image.open("/Users/oliviergianoli/Desktop/Project TriMax/Codes/python/4_points_recognition/DATASET")

# Convert the image to HSV format
hsv_img = img.convert("HSV")

# Define the blue color range in HSV format
lower_blue = (100, 50, 50)
upper_blue = (130, 255, 255)

# Threshold the image to create a binary mask of the blue pixels
blue_mask = hsv_img.point(lambda p: 255 if (p >= lower_blue and p <= upper_blue) else 0, mode="1")

# Invert the mask to get the non-blue pixels
non_blue_mask = Image.invert(blue_mask)

# Find the contours of the non-blue area
contours = find_contours(non_blue_mask, 0.5)

# Find the bounding box of the non-blue area
x, y, w, h = contours[0].bbox

# Draw the bounding box on the original image
draw = ImageDraw.Draw(img)
draw.rectangle((x, y, x+w, y+h), outline="green", width=2)

# Display the result
img.show()
