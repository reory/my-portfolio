
![Last Commit](https://img.shields.io/github/last-commit/reory/geo-loan-uk-predictor?cacheSeconds=60)
![Repo Size](https://img.shields.io/github/repo-size/reory/geo-loan-uk-predictor?cacheSeconds=60)
![License](https://img.shields.io/badge/License-MIT-green)

![Faker](https://img.shields.io/badge/Faker-Data_Generation-ff69b4?style=flat-square)
![Flet](https://img.shields.io/badge/Flet-UI_Framework-04d9ff?style=flat-square&logo=flutter)
![Folium](https://img.shields.io/badge/Folium-Geospatial-77b829?style=flat-square&logo=leaflet)
![SciPy](https://img.shields.io/badge/SciPy-Mathematics-8caae6?style=flat-square&logo=scipy)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=flat-square&logo=pandas)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=flat-square&logo=mysql&logoColor=white)

A high-performance Python dashboard for visualizing and analyzing loan risk across the United Kingdom. This application uses SciPy for statistical risk modeling, Flet for a modern UI, and MySQL for persistent data storage.

---

# 🚀 Key Features

Nationwide Risk Mapping: Interactive Heatmaps generated with Folium.

Statistical Analysis: Real-time Z-score and DTI (Debt-to-Income) calculations.

Full-Stack CRUD: Add, Delete, and Update borrowers with a safety-first UI.

Secure Architecture: Environment-based credential management.

---

<details>
  <summary>🧮 How the Geo-Loan Engine Works</summary>

The risk engine uses a Three-Step Statistical Pipeline:

HOW THE SciPy MATH WORKS:
* LEVEL THE FIELD: Credit scores (700) and Debt ratios (0.3) are different sizes. 
We use Z-Scores to turn them into 'distance from average' so we can compare them fairly.
* THE SCORE: Risk = (High Debt) - (Good Credit) - (Work Experience).
* THE SQUASH: The result could be any number. We use a 'Sigmoid' function to 
squish that number into a simple 0 to 1 scale (0% to 100% risk).
* THE GRADE: Scores are labeled: 'Safe', 'Caution', or 'High Risk'.

</details>

---

<details>
  <summary>📸Screenshots </summary>

![Screenshot of the dashboard interface](images/dashboard11.webp)
![Screenshot of adding a new loanee](images/dashboard12.webp)
![screenshot of adding a new loanee](images/dashboard13.webp)
![screenshot of new applications entered](images/dashboard14.webp)
![screenshot of the database](images/MySQL_db.webp)

</details>

---

<details>
  <summary>Demo Video</summary>

![Video of the dashboard](demo.mp4)

</details>

---

# 🛠️ Installation & Setup

## Prerequisites
Python 3.10+

MySQL Server (Running locally or hosted)

Virtual Environment (Recommended)

## Database Configuration
Run the following SQL command in your MySQL terminal to prepare the table:
```
CREATE TABLE loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    borrower_name VARCHAR(100),
    amount DECIMAL(15,2),           
    outcode VARCHAR(10),
    is_defaulted TINYINT(1),        
    credit_score INT,
    years_employed INT,
    debt_to_income DECIMAL(5,2),   
    risk_score DECIMAL(5,3) DEFAULT NULL,
    risk_grade VARCHAR(20) DEFAULT NULL
);
```

## Environment Secrets
Create a file named .env in the root directory and add your credentials:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=geoloan_db
```

## Install Dependencies
```Bash
pip install -r requirements.txt
```

---

## Populating Data

Once your database table is created and your .env is configured, you must 
populate the system with synthetic UK borrower data
Note: To reset your data at any time, run TRUNCATE TABLE loans; in your 
MySQL terminal before running the seeder again.

```Bash
python run_seeder.py
```
"After running the seeder, 
your console will confirm 'Successfully inserted 500 records'."

---

# 📂 Project Structure
```
├── main.py                # App entry point & UI Logic
├── run_seeder.py          # IMPORTANT: Database Populater  
├── .env                   # Private credentials (ignored by Git)
├── .gitignore             
├── requirements.txt       # Project dependencies
├── database/
│   ├── connection.py      # Secure MySQL handshake
│   └── queries.py         # SQL CRUD operations
├── models/
│   └── predictor.py       # SciPy Risk Engine
└── ui/
    ├── app_layout.py      # Flet UI Components
    └── map_generator.py   # Folium Map Logic
```

---

## 🚦 How to Run

Ensure your MySQL server is active.
Run the boot sequence:

```Bash
python main.py
```
Click "Launch Analysis" to process the data and open the interactive map.

## 🧪 To run the full test suite
```Bash
python -m pytest
```
## 📄 To view the coverage report
```Bash
python -m pytest --cov=models --cov=database --cov-report=html
```

---

<details>
  <summary>🛠️ The Core Tech Stack</summary>

- **Faker:** * Purpose: A library for generating synthetic data (fake names, addresses, emails).

Usage: Used in your run_seeder.py to create 600+ realistic borrower records instantly so you didn't have to type them in manually.

- **Flet:** * Purpose: A framework that brings Google's Flutter UI to Python.

Usage: This is your Frontend. It handles the window, the buttons, the input forms, and the "Dark Mode" dashboard you see on your screen.

- **Folium:** * Purpose: A library that creates interactive maps using Leaflet.js.

Usage: It takes the coordinates (Latitude/Longitude) and generates that HTML map with the colored dots for your risk zones.

- **SciPy:** * Purpose: A scientific library for complex mathematical algorithms.

Usage: You used it to calculate Z-Scores. It compares a borrower's debt against the average of the whole group to determine if they are "High Risk" or "Safe."

- **Pandas:** * Purpose: The "Swiss Army Knife" of data manipulation.

Usage: It acts as a bridge. It pulls data from MySQL, cleans it up, and passes it to Folium and SciPy in a neat table format (a "DataFrame").

- **MySQL:** * Purpose: A Relational Database Management System (RDBMS).

Usage: Your Persistent Storage. It ensures that if you close the app, your 600 borrowers aren't deleted—they are saved safely in a local database.

</details>

---

<details>
  <summary>🧠 Technical Challenges & Solutions</summary>

* Geospatial Data Integrity: * Challenge: Standardizing messy UK Postcode data for mapping.

* Solution: Implemented a Regular Expression (Regex) validation layer to extract 
"Outcodes," ensuring 100% compatibility with the Folium map engine.

* Statistical Modeling: * Challenge: Creating a dynamic risk rating from static borrower data.

* Solution: Leveraged SciPy's Z-Score functions to normalize multi-variable inputs (DTI, Credit Score), creating a weighted risk algorithm.

* Security & Scalability: * Challenge: Protecting sensitive database credentials in a public repository.

* Solution: Architected a Decoupled Configuration using .env files and python-dotenv, keeping secrets out of Version Control (Git).

* Full-Stack Syncing: * Challenge: Handling high-volume database inserts without UI lag.

* Solution: Built a modular CRUD backend in MySQL and integrated it with an asynchronous Flet frontend for a smooth user experience.

</details>

---

<details>
  <summary>🛣️ Roadmap Features</summary>

 - [ ] User Authentication: Implement a secure Login/Sign-up system with hashed passwords using bcrypt to protect lender data.

 - [ ] Advanced Filtering: Build a sidebar in Flet to filter the map in real-time by Loan Amount, Risk Grade, or specific UK Outcode regions.

 - [ ] Predictive Machine Learning: Move beyond static Z-scores to a trained Scikit-Learn model that predicts loan default probability based on historical UK financial trends.

</details>

---

* **Built by Roy Peters** [![LinkedIn](https://img.shields.io/badge/LinkedIn-Roy%20Peters-blue?logo=linkedin)](https://www.linkedin.com/in/roy-p-74980b382/)