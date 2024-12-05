import numpy as np
import cv2
from tensorflow.keras.models import load_model

# Load the model once when the server starts
model = load_model('translator/model/mangyanscript_model.keras')

# Map of predictions to Mangyan syllables
SYLLABLE_MAP = {
   
    0: 'a', 1: 'ba', 2: 'bi', 3: 'bu', 4: 'da', 5: 'di', 6: 'du',
    7: 'ga', 8: 'gi', 9: 'gu', 10: 'ha', 11: 'hi', 12: 'hu',
    13: 'i', 14: 'ka', 15: 'ki', 16: 'ku', 17: 'la', 18: 'li',
    19: 'lu', 20: 'ma', 21: 'mi', 22: 'mu', 23: 'na', 24: 'nga',
    25: 'ngi', 26: 'ngu', 27: 'ni', 28: 'nu', 29: 'pa', 30: 'pi',
    31: 'pu', 32: 'ra', 33: 'ri', 34: 'ru', 35: 'sa', 36: 'si',
    37: 'su', 38: 'ta', 39: 'ti', 40: 'tu', 41: 'u', 42: 'wa',
    43: 'wi', 44: 'wu', 45: 'ya', 46: 'yi', 47: 'yu'
}

def preprocess_image(image_path):
    """
    Preprocesses an image to make it compatible with the model input.
    :param image_path: Path to the input image.
    :return: Preprocessed image ready for model prediction.
    """
    # Read the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise ValueError("Error reading the image. Please check the file path.")

    # Resize the image to 64x64
    image_resized = cv2.resize(image, (64, 64))

    # Normalize pixel values to the range [0, 1]
    image_normalized = image_resized / 255.0

    # Expand dimensions to match model input (1, 64, 64, 1)
    image_reshaped = np.expand_dims(image_normalized, axis=-1)

    # Convert grayscale image to 3-channel RGB equivalent
    image_rgb = np.repeat(image_reshaped, 3, axis=-1)

    # Add a batch dimension (1, 64, 64, 3)
    preprocessed_image = np.expand_dims(image_rgb, axis=0)

    return preprocessed_image


def predict_translation(image_path):
    """
    Predicts the translation of an image containing Mangyan script.
    :param image_path: Path to the input image.
    :return: Translated text.
    """
    try:
        # Preprocess the image
        preprocessed_image = preprocess_image(image_path)

        # Make a prediction
        predictions = model.predict(preprocessed_image)
        predicted_class = np.argmax(predictions)

        # Map the predicted class to a Mangyan syllable
        translated_syllable = SYLLABLE_MAP.get(predicted_class, "Unknown")

        return translated_syllable

    except Exception as e:
        return f"Prediction error: {str(e)}"