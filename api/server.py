# import os
# from datetime import datetime, timedelta

# import pytz
# import torch
# import torchvision.transforms.v2 as T
# from dotenv import load_dotenv
# from flask import Flask, request
# from torchvision.io import decode_image
# from vercel.blob import BlobClient, ListBlobItem

# env_path = os.path.join(os.getcwd(), ".env.local")
# model_path = os.path.join(os.getcwd(), "model.pth")
# load_dotenv(env_path)

# model = torch.load(model_path, weights_only=False)
# model.eval()

# app = Flask(__name__)

# blob_client = BlobClient()


# def predict_images_class(images_bytes: list[bytes]):
#     images = [
#         decode_image(torch.tensor(bytearray(image_bytes), dtype=torch.uint8))
#         for image_bytes in images_bytes
#     ]
#     preprocess = T.Compose(
#         [T.Resize(227), T.CenterCrop(227), T.ToDtype(torch.float32, scale=True)]
#     )
#     images = [preprocess(image) for image in images]
#     images = torch.stack(images)
#     preds = model(images)
#     predicted_classes = torch.argmax(preds, dim=1)
#     return predicted_classes


# def transform_predictions(predicted_classes: torch.Tensor) -> list[dict]:
#     results = []
#     for predicted_class in predicted_classes:
#         if predicted_class == 0:
#             class_name = "adidas"
#         elif predicted_class == 1:
#             class_name = "converse"
#         else:
#             class_name = "nike"
#         results.append(
#             {
#                 "predicted_class": predicted_class.item(),
#                 "class_name": class_name,
#             }
#         )
#     return results


# def list_images() -> list[ListBlobItem]:
#     blobs = blob_client.list_objects(mode="folded")
#     first_folder = blobs.folders[0]
#     sub = blob_client.list_objects(prefix=first_folder, mode="folded")
#     return sub.blobs


# @app.route("/api/products/refund", methods=["GET"])
# def refund():
#     images = list_images()
#     filtered_images: list[ListBlobItem] = []
#     for image in images:
#         if image.size > 0 and image.uploaded_at >= (
#             datetime.now(pytz.utc) - timedelta(days=1)
#         ):
#             filtered_images.append(image)
#     results = [blob_client.get(img.download_url) for img in filtered_images]
#     predicted_classes = predict_images_class(results)
#     transformed_predictions = transform_predictions(predicted_classes)
#     for i, img in enumerate(filtered_images):
#         transformed_predictions[i]["pathname"] = img.pathname
#         transformed_predictions[i]["download_url"] = img.download_url
#         transformed_predictions[i]["size"] = img.size
#         transformed_predictions[i]["uploaded_at"] = img.uploaded_at.isoformat()
#     return {"predictions": transformed_predictions}


# @app.route("/api/model/predict", methods=["POST"])
# def predict():
#     if "image" not in request.files:
#         return {"error": "No image provided"}, 400
#     image_file = request.files["image"]
#     image_bytes = image_file.read()
#     image = decode_image(torch.tensor(bytearray(image_bytes), dtype=torch.uint8))
#     preprocess = T.Compose(
#         [T.Resize(227), T.CenterCrop(227), T.ToDtype(torch.float32, scale=True)]
#     )
#     image = preprocess(image)
#     preds = model(image.unsqueeze(0))
#     predicted_class = torch.argmax(preds, dim=1).item()
#     if predicted_class == 0:
#         class_name = "adidas"
#     elif predicted_class == 1:
#         class_name = "converse"
#     else:
#         class_name = "nike"
#     return {
#         "predictions": preds.detach().numpy().tolist(),
#         "predicted_class": predicted_class,
#         "class_name": class_name,
#     }
