import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import logging

# --- Import our custom model function ---
from model import analyze_emotion

# --- Initialization ---
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# --- Database Configuration ---
# Set the data directory path (Render provides this as an environment variable)
DATA_DIR = os.environ.get('RENDER_DATA_DIR', os.getcwd()) 
DB_PATH = os.path.join(DATA_DIR, 'database.db')

# Update the database URI to use the new path
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'

# Configure a folder to store user uploads
app.config['UPLOAD_FOLDER'] = 'static/uploads'
# Initialize the database
db = SQLAlchemy(app)

# --- Database Model Definition ---
class Log(db.Model):
    """
    This class defines the database table for logging analyses.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(200), nullable=False)
    result = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Log {self.id}: {self.name} - {self.result}>'


# --- Web Routes ---

@app.route('/')
def index():
    """Renders the homepage (index.html)."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Handles the file upload, runs analysis, and saves to DB.
    """
    
    # 1. Get data from the form
    if 'image_file' not in request.files:
        logging.error("No file part in request")
        return redirect(request.url)
        
    file = request.files['image_file']
    user_name = request.form.get('user_name', 'Anonymous') # Get name, default to 'Anonymous'

    if file.filename == '':
        logging.warning("No selected file")
        return redirect(request.url)

    if file:
        # 2. Save the uploaded file
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(image_path)
            logging.info(f"File saved to {image_path}")
        except Exception as e:
            logging.error(f"Error saving file: {e}")
            return "Error saving file.", 500

        # 3. Call the model to analyze the image
        dominant_emotion = analyze_emotion(image_path)
        
        # 4. Save the result to the database
        try:
            new_log = Log(name=user_name, image_filename=filename, result=dominant_emotion)
            db.session.add(new_log)
            db.session.commit()
            logging.info(f"Saved analysis to database for user: {user_name}")
        except Exception as e:
            logging.error(f"Error saving to database: {e}")
            # Don't stop the user if DB fails, just log it
            db.session.rollback() 

        # 5. Render the result page
        return render_template('result.html', 
                               emotion_result=dominant_emotion,
                               # We pass the path relative to the 'static' folder
                               image_filename=f'uploads/{filename}')
            
    return "An unexpected error occurred."


# --- Run the App ---
if __name__ == '__main__':
    # Create the 'static/uploads' folder if it doesn't exist
    upload_dir = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)