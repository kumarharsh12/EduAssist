# import os
# from PIL import Image
# import subprocess
# import imagehash
# import torch
# from app.models.models import classification_model, data_transforms, device

# def extract_screenshots(video_path: str, screenshots_path: str, fps: float, id: str):
#     subprocess.run([
#         "ffmpeg", "-i", video_path,
#         "-vf", f"fps={fps}",
#         os.path.join(screenshots_path, f"{id}_%04d.png")
#     ], check=True)

# def classify_and_remove_duplicates(screenshots_path: str):
#     hashes = {}
#     for screenshot in os.listdir(screenshots_path):
#         if screenshot.endswith(".png"):
#             image_path = os.path.join(screenshots_path, screenshot)
#             image = Image.open(image_path).convert("RGB")
            
#             # Classification
#             transformed_image = data_transforms(image).unsqueeze(0).to(device)
#             with torch.no_grad():
#                 outputs = classification_model(transformed_image)
#                 _, preds = torch.max(outputs, 1)
#                 if preds.item() == 0:
#                     os.remove(image_path)
#                     continue
            
#             # Duplicate detection if > 95% then remove
#             image_hash = imagehash.phash(image)
#             is_duplicate = False
#             for existing_hash in hashes:
#                 similarity = 1 - (image_hash - existing_hash) / len(image_hash.hash) ** 2
#                 if similarity > 0.95:
#                     os.remove(image_path)
#                     is_duplicate = True
#                     break
#             if not is_duplicate:
#                 hashes[image_hash] = image_path