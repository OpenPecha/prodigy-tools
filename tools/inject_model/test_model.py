import tensorflow as tf
from prodigy.components.loaders import Images
from prodigy.util import b64_uri_to_bytes


def get_prediction(source_dir):
    stream = Images(source_dir)
    custom_model = load_your_custom_model()
    for eg in stream:
        image_bytes = b64_uri_to_bytes(eg["image"])
        predictions = custom_model(image_bytes)
        print(predictions)
        return predictions


def load_your_custom_model():
    model = tf.keras.models.load_model('./LA_MixModel_v1.h5')
    return model


if __name__ == "__main__":
    prediction = get_prediction("./tools/inject_model/LA_images")