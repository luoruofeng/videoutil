import os
from PIL import Image
import torch
from torchvision import transforms
from transformers import CLIPProcessor, CLIPModel

def load_image(image_path):
    return Image.open(image_path)

def get_image_features(image, model, processor):
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        features = model.get_image_features(**inputs)
    return features

def calculate_cosine_similarity(features1, features2):
    return torch.nn.functional.cosine_similarity(features1, features2)

def delete_similar_images(image_files, threshold=0.91):
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")

    features_list = []
    image_paths = []

    for image_file in image_files:
        image = load_image(image_file)
        features = get_image_features(image, model, processor)
        features_list.append(features)
        image_paths.append(image_file)

    deleted_files = []
    for i in range(len(features_list)):
        if features_list[i] is None:
            continue
        for j in range(i + 1, len(features_list)):
            if features_list[j] is None:
                continue
            similarity = calculate_cosine_similarity(features_list[i], features_list[j]).item()
            if similarity > threshold:
                print(f"Deleting {image_paths[j]} due to similarity with {image_paths[i]} ({similarity*100:.2f}%)")
                os.remove(image_paths[j])
                deleted_files.append(image_paths[j])
                features_list[j] = None  # Mark as deleted

    return deleted_files

def get_all_image_files(directory):
    image_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".png", ".jpg", ".jpeg")):
                image_files.append(os.path.join(root, file))
    return image_files

def process_images_in_directory(directory):
    image_files = get_all_image_files(directory)
    deleted_files = delete_similar_images(image_files)
    print(f"Deleted {len(deleted_files)} files")

if __name__ == "__main__":
    current_directory = os.getcwd()
    process_images_in_directory(current_directory)
