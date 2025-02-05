# import os
# import torch
# import whisper
# from torchvision import models, transforms

# Load Whisper model
# whisper_model = whisper.load_model("turbo")

# # Load the trained classification model
# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# classification_model = models.resnet18(pretrained=False)
# num_features = classification_model.fc.in_features
# classification_model.fc = torch.nn.Linear(num_features, 2)  # Assuming 2 classes
# model_path = os.path.join(os.path.dirname(__file__), "../../saved_models/model_weights.pth")
# classification_model.load_state_dict(torch.load(model_path, map_location=device))
# classification_model = classification_model.to(device)
# classification_model.eval()

# # Define image transformations
# data_transforms = transforms.Compose([
#     transforms.Resize(256),
#     transforms.CenterCrop(224),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
# ])

from groq import Groq
async def whisper_transcribe(filename: str):
    # Initialize the Groq client
    client = Groq()

    # Open the audio file
    with open(filename, "rb") as file:
        # Create a transcription of the audio file
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),  # Required audio file
            model="whisper-large-v3-turbo",  # Required model to use for transcription
            prompt="Specify context or spelling",  # Optional
            response_format="json",  # Optional
            language="en",  # Optional
            temperature=0.0  # Optional
        )
        # Return the transcription text
        return transcription.text