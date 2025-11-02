#First, you need to install the deepface library using this command on your terminal:
# python -m pip install deepface

# We REMOVED 'from deepface import DeepFace' from here.
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def analyze_emotion(image_path):
    """
    Analyzes the emotion from an image file.
    
    Args:
        image_path (str): The path to the image file.
        
    Returns:
        str: The dominant emotion, or an error message.
    """
    
    # --- THIS IS THE FIX ---
    # We moved the import statement HERE, inside the function.
    # Now, DeepFace (and TensorFlow) will only load when 
    # this function is called, not when the app starts.
    from deepface import DeepFace
    
    try:
        logging.info(f"Analyzing image at: {image_path}")
        
        
        analysis_results = DeepFace.analyze(
            img_path=image_path,
            actions=['emotion'],
            detector_backend='retinaface',  # This is fine to use
            enforce_detection=False  # Don't crash if no face is found
        )
        
        # DeepFace returns a list of dictionaries, one for each face.
        # We'll just use the first face found.
        if not analysis_results or len(analysis_results) == 0:
            logging.warning("No face detected in the image.")
            return "No face detected"
            
        first_face = analysis_results[0]
        dominant_emotion = first_face['dominant_emotion']
        
        logging.info(f"Dominant emotion: {dominant_emotion}")
        return dominant_emotion.capitalize()

    except Exception as e:
        # Catch any other errors (e.g., file not found, corrupted image)
        logging.error(f"Error during emotion analysis: {e}")
        return "Analysis error"