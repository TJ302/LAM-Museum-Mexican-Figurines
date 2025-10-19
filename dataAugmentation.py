import os
import random
from PIL import Image 
from torchvision import transforms


##Configuration load original imagees from folder then save to another 

input = "dataset/..."
output = "dataset/..."
numAugmentsPerImage = 5


os.markedirs(output, exist_ok=True)

##Define augmentation pipeline
augment =  transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomVerticalFlip(p=0.2),
    transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4, hue=0.1),
    transforms.RandomRotation(degrees=30),
    transforms.RandomResizedCrop(size=(224, 224), scale=(0.8, 1.0))
])

def augmentandSave(imagePath, output):
    img = Image.open(imagePath).convert("RGB")
    base = os.path.splitext(os.path.basename(image))[0]

    for i in range(numAugmentsPerImage):
        augImg = augment(img)
        savePath = os.path.join(output, f"{base}_aug{i}.jpg")
        augImg.save(savePath)



##Process all images in the input folder

for filename in os.listdir(input):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        imagePath = os.path.join(input, filename)
        augmentandSave(imagePath, output)

print("Data augmentation completed.")