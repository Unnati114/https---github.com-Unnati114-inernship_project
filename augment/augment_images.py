import os
import cv2
import albumentations as A

# ==========================
# Input and Output Folders
# ==========================

input_folder = "archive/NEU-DET/train/images"

output_folder = "dataset/augmented_images"

# Create output folder automatically
os.makedirs(output_folder, exist_ok=True)

# ==========================
# Augmentation Pipeline
# ==========================

transform = A.Compose([

    A.Rotate(limit=20, p=0.8),

    A.HorizontalFlip(p=0.5),

    A.RandomBrightnessContrast(
        brightness_limit=0.2,
        contrast_limit=0.2,
        p=0.7
    ),

    A.GaussianBlur(blur_limit=3, p=0.3),

    A.GaussNoise(p=0.3),

    A.RandomShadow(p=0.3),

    A.RandomGamma(p=0.5),

    A.CLAHE(p=0.5)

])

# ==========================
# Read Every Image
# ==========================

for filename in os.listdir(input_folder):

    if filename.endswith(".jpg"):

        image_path = os.path.join(input_folder, filename)

        image = cv2.imread(image_path)

        augmented = transform(image=image)

        augmented_image = augmented["image"]

        save_path = os.path.join(output_folder, filename)

        cv2.imwrite(save_path, augmented_image)

        print(f"{filename} Done")

print("Augmentation Completed Successfully!")