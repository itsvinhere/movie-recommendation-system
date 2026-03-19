# 🎬 Movie Recommendation System (ML + Flask)

## 📌 Project Overview

The Movie Recommendation System is a full-stack web application that suggests movies to users based on their preferences, interests, and mood. The system uses machine learning techniques along with a Flask-based backend to deliver personalised movie recommendations.

This project is designed to simulate real-world recommendation engines like Netflix and Amazon Prime by combining data processing, machine learning models, and a dynamic web interface.

---

## 🚀 Features

### 🔐 User Authentication

* Secure login and registration system
* User session management
* Personalised recommendations for each user

### 🎯 Movie Recommendation Engine

* Content-based filtering using movie metadata
* Suggests movies based on user-selected preferences or mood
* Fast and efficient recommendation generation

### 🎭 Mood-Based Suggestions

* Users can select their current mood (happy, sad, action, etc.)
* System maps mood to relevant movie genres
* Enhances user experience with contextual recommendations

### 🎥 Movie Details Page

* Displays:

  * Movie title
  * Overview / description
  * IMDb rating
  * Genre and release year
* Embedded YouTube trailer for each movie

### 🌐 Responsive User Interface

* Netflix-inspired UI
* Clean and modern layout
* Dynamic content rendering using templates

---

## 🛠️ Tech Stack

### 🔹 Backend

* Python
* Flask (Web Framework)

### 🔹 Machine Learning

* Pandas
* NumPy
* Scikit-learn

### 🔹 Frontend

* HTML
* CSS
* JavaScript

### 🔹 Database

* SQLite (can be upgraded to PostgreSQL/MySQL)

---

## 🧠 How It Works

1. **Data Collection**

   * Movie dataset is loaded containing features like title, genre, keywords, and overview

2. **Data Preprocessing**

   * Text data is cleaned and transformed
   * Features are combined into a single representation

3. **Feature Extraction**

   * CountVectorizer / TF-IDF is used to convert text into numerical vectors

4. **Similarity Calculation**

   * Cosine similarity is computed between movies

5. **Recommendation Generation**

   * Based on user input, similar movies are suggested

6. **Backend Processing**

   * Flask handles API routes and user requests

7. **Frontend Rendering**

   * Templates display movie results dynamically

---

## 📂 Project Structure

```
movie-recommendation-system/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
├── .gitignore             # Ignored files
│
├── static/                # CSS, JS, images
├── templates/             # HTML templates
├── models/                # ML models
├── database/              # Database files
└── utils/                 # Helper functions
```

---

## ▶️ How to Run the Project

### 🔹 1. Clone Repository

```bash
git clone https://github.com/your-username/movie-recommendation-system.git
cd movie-recommendation-system
```

### 🔹 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔹 3. Run Application

```bash
python app.py
```

### 🔹 4. Open in Browser

```
http://127.0.0.1:5000
```

---

## 📸 Screenshots

(Add screenshots here for better presentation)

---

## 📈 Future Enhancements

* Deep learning-based recommendation system
* User watch history tracking
* Real-time recommendation updates
* Deployment on cloud platforms (AWS, Render, Heroku)
* Integration with external APIs (TMDB, IMDb)

---

## 💼 Use Cases

* Learning full-stack ML integration
* Portfolio project for placements
* Understanding recommendation systems
* Real-world application development

---

## ⚠️ Limitations

* Limited dataset size
* Basic recommendation algorithm
* No real-time user behaviour tracking

---

## 👨‍💻 Author

Vin

---

## ⭐ Acknowledgements

* Open-source datasets
* Scikit-learn documentation
* Flask community

---

## 📌 Conclusion

This project demonstrates the integration of machine learning with web development to build an intelligent recommendation system. It provides a strong foundation for developing advanced AI-powered applications and showcases practical implementation skills required in the industry.
