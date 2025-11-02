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
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['UPLOAD_FOLDER'] = 'static/uploads' # We will create this folder
db = SQLAlchemy(app)

# --- Database Model Definition ---
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(200), nullable=False)
    result = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Log {self.id}: {self.name} - {self.result}>'

# -----------------------------------------------------------------
# --- THIS IS THE FIX ---
# We move the setup code here, to the top level of the script.
# This code will now run when Render starts, BEFORE any web requests.
# -----------------------------------------------------------------
logging.info("Checking for upload directory and database tables...")

# 1. Create the upload folder if it doesn't exist
upload_dir = app.config['UPLOAD_FOLDER']
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)
    logging.info(f"Created directory: {upload_dir}")

# 2. Create the database tables
# We need to be in an 'app_context' to do database operations
with app.app_context():
    db.create_all()
    logging.info("Database tables checked/created.")

logging.info("Application setup complete. Starting web routes.")
# -----------------------------------------------------------------
# --- END OF FIX ---
# -----------------------------------------------------------------


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
    user_name = request.form.get('user_name', 'Anonymous') 

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
            db.session.rollback() 

        # 5. Render the result page
        return render_template('result.html', 
                               emotion_result=dominant_emotion,
                               image_filename=f'uploads/{filename}')
            
    return "An unexpected error occurred."


# -----------------------------------------------------------------
# --- NEW PAGE FOR VIEWING LOGS ---
# -----------------------------------------------------------------
@app.route('/view-logs-secret')
def view_logs():
    """
    A secret page to view all database logs.
    """
    try:
        # Query the database to get all log entries, ordered by newest first
        all_logs = Log.query.order_by(Log.id.desc()).all()
        
        # Pass the log data to a new HTML template
        return render_template('logs.html', logs=all_logs)
    
    except Exception as e:
        return f"An error occurred trying to read the database: {e}"
# -----------------------------------------------------------------
# --- END OF NEW PAGE ---
# -----------------------------------------------------------------


# --- Run the App (for local testing) ---
if __name__ == '__main__':
    # This block is now only for running the app locally
    app.run(debug=True)