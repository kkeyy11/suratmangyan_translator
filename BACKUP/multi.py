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

def preprocess_image(image):
    """
    Preprocesses an image to make it compatible with the model input.
    :param image: Grayscale image to preprocess.
    :return: Preprocessed image ready for model prediction.
    """
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

def segment_image(image_path):
    """
    Segments the image into individual characters based on contours.
    :param image_path: Path to the input image.
    :return: List of segmented character images.
    """
    # Read the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise ValueError("Error reading the image. Please check the file path.")

    # Apply thresholding to get binary image
    _, binary_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)

    # Find contours (individual characters)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours from left to right (assuming the text is horizontal)
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])

    # Check if there are multiple contours
    if len(contours) > 1:
        segmented_images = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 5 and h > 5:  # Filter out noise (small areas)
                char_image = image[y:y + h, x:x + w]  # Crop the character region
                segmented_images.append(char_image)
        return segmented_images
    else:
        # If only one contour is found, return the entire image as a single character
        return [image]

def predict_translation(image_path):
    """
    Predicts the translation of an image containing Mangyan script, with segmentation for multi-syllable words.
    :param image_path: Path to the input image.
    :return: Translated text.
    """
    try:
        # Segment the image into individual characters
        segmented_images = segment_image(image_path)

        translated_text = []

        # Process each segmented character
        for char_image in segmented_images:
            # Preprocess the character image
            preprocessed_image = preprocess_image(char_image)

            # Make a prediction for this character
            predictions = model.predict(preprocessed_image)
            predicted_class = np.argmax(predictions)

            # Map the predicted class to a Mangyan syllable
            translated_syllable = SYLLABLE_MAP.get(predicted_class, "Unknown")
            translated_text.append(translated_syllable)

        # Join the translated syllables to form the complete word or phrase
        return ''.join(translated_text)

    except Exception as e:
        return f"Prediction error: {str(e)}"
