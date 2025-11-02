# Human Emotion Detection Web App 😡😭😊

**Author:** OBI IKECHUKWU
**Student ID:** 23CE034397
**Program:** Computer Science

---

## 🚀 Live Demo

You can access the live, deployed application here:

**[https://emotion-detection-app-htbi.onrender.com](https://emotion-detection-app-htbi.onrender.com)**

*(Note: The app is hosted on Render's free tier. The first load may take 30-60 seconds for the server to "wake up".)*

---

## 📄 Project Overview

This project is a full-stack web application that detects the dominant human emotion from an uploaded image. It is built with a Flask back-end, a pre-trained `deepface` AI model, and a persistent PostgreSQL database hosted on Neon.

Users can enter their name and upload an image of a face. The back-end analyzes the image, identifies the emotion, and displays the result. Every analysis is logged to a permanent cloud database.

## ✨ Key Features

* **Image Upload:** A simple, user-friendly interface to upload a name and an image file.
* **AI-Powered Emotion Detection:** Uses the `deepface` library to analyze the image and classify the emotion into one of seven categories: **angry, disgust, fear, happy, sad, surprise, or neutral**.
* **Persistent Database:** All analysis results (user's name, image filename, and detected emotion) are saved to a cloud-hosted PostgreSQL database (Neon), which is not erased on server restarts.
* **Admin Log Viewer:** A secret web page is available to view all entries in the database log, allowing for easy review and verification.

---

## 🔧 Technology Stack

This project integrates several technologies to create a full-stack application:

* **Back-end:**
    * **Python 3.10**
    * **Flask:** A lightweight web framework for routing and handling requests.
    * **Gunicorn:** A production-grade WSGI server to run the Flask app.
* **Machine Learning:**
    * **DeepFace:** A pre-trained, open-source library for facial analysis.
    * **TensorFlow:** The underlying deep learning framework used by `deepface`.
    * **OpenCV (opencv-python):** Used as the face detector backend to save memory on the free-tier server.
* **Database:**
    * **PostgreSQL (hosted on Neon):** A free, persistent cloud database.
    * **Flask-SQLAlchemy:** An ORM (Object-Relational Mapper) to interact with the database using Python.
    * **psycopg2-binary:** A Python driver to connect to PostgreSQL.
* **Front-end:**
    * **HTML5**
    * **CSS3** (minimal styling)
    * **Jinja2:** A templating engine used by Flask.
* **Deployment:**
    * **Render:** A cloud platform for hosting the web application.
    * **Git & GitHub:** For version control and CI/CD (auto-deployment on push).

---

## 📁 Project Structure

The project is organized according to standard Flask application conventions:
OBI_IKECHUKWU_23CE034397_EMOTION_DETECTION_WEB_APP/ │ ├── app.py # Main Flask server, routes, & database setup ├── model.py # Contains the analyze_emotion() function ├── requirements.txt # List of all Python packages for deployment ├── .gitignore # Tells Git which files to ignore (e.g., venv) │ ├── static/ │ └── uploads/ # Stores temporary uploaded images │ └── templates/ ├── index.html # Homepage (upload form) ├── result.html # Page to display the analysis result └── logs.html # Secret page to view the database logs

---

## ⚙️ How to Run Locally

To run this project on your local machine, follow these steps:

1.  **Prerequisites:**
    * Python 3.10 or higher
    * Git

2.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[Your-Username]/OBI_IKECHUKWU_23CE034397_EMOTION_DETECTION_WEB_APP.git
    cd OBI_IKECHUKWU_23CE034397_EMOTION_DETECTION_WEB_APP
    ```

3.  **Create a Virtual Environment:**
    ```bash
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    
    # On Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Application:**
    ```bash
    python app.py
    ```
    *The app will automatically create and use a local `database.db` (SQLite) file for testing.*

6.  **Access the App:**
    Open your web browser and go to `http://127.0.0.1:5000`.

---

## 📋 How to Use

### 1. Analyze an Image
1.  Navigate to the homepage.
2.  Enter your name in the "Your Name" field.
3.  Click "Choose File" and select a `.jpg` or `.png` image of a face.
4.  Click "Analyze Emotion".
5.  The app will process the image and display the dominant emotion on the result page.

### 2. View the Database Logs
To view the log of all analyses, navigate to the secret admin page (add this to your main URL):

`/view-logs-secret`

**Example:** `https://emotion-detection-app-htbi.onrender.com/view-logs-secret`
