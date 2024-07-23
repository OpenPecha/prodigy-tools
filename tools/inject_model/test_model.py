import onnxruntime
import numpy as np
from PIL import Image
from pathlib import Path

def process_output(output):
    # Apply softmax to the output
    probabilities = np.exp(output) / np.sum(np.exp(output), axis=1)

    # Get the predicted label
    predicted_label = np.argmax(probabilities)

    return predicted_label

# Load and preprocess the image
def load_image(image_path):
    image = Image.open(image_path)
    return image


# Load the ONNX model
def load_model(model_path):
    model = onnxruntime.InferenceSession(model_path)
    return model

def predict_images(model, image_paths):
    for image_path in image_paths:
        image = load_image(image_path)
        input_data = np.array(image, dtype=np.float32)
        output = model.run(None, {'input': input_data})
        predictions = process_output(output)
        print(predictions)

if __name__ == "__main__":
    image_paths = Path(f"./tools/inject_model/LA_images/").iterdir()
    model_path = "./LA_TextArea_v1_quant.onnx"
    model = load_model(model_path)
    predict_images(model, image_paths)