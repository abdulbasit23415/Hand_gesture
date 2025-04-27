import cv2
import os

# Directory containing the images
image_dir = "/data/data/"

# Load all images into a list
images = []
for filename in os.listdir(image_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # Add other extensions if needed
        img_path = os.path.join(image_dir, filename)
        img = cv2.imread(img_path)  # Load the image
        if img is not None:  # Ensure the image was loaded successfully
            images.append(img)
        else:
            print(f"Warning: Failed to load image {img_path}")

print(f"Loaded {len(images)} images.")