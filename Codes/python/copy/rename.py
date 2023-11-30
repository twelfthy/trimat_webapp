import os

# Define the directory containing the files
directory = "/home/ogianoli/Code/cazzate/4_points_recognition/trainset/02_Annotations"

# Get a list of the files in the directory
files = os.listdir(directory)

# Define the new file name pattern
new_name_pattern = "File{:02d}.xml"

# Loop over the files and rename them
for i, file_name in enumerate(files):
    if i>0:
        # Generate the new file name
        new_file_name = new_name_pattern.format(i)
        
        # Get the full paths to the old and new files
        old_path = os.path.join(directory, file_name)
        new_path = os.path.join(directory, new_file_name)
        
        # Rename the file
        os.rename(old_path, new_path)