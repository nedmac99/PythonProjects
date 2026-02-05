# 🐍 Python Projects Portfolio

A comprehensive collection of Python projects demonstrating proficiency in **Machine Learning**, **Data Science**, **Computer Vision**, **Web Development**, and **Desktop Application Development**.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?logo=scikit-learn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Deep%20Learning-ff6f00?logo=tensorflow&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b?logo=streamlit&logoColor=white)
![Django](https://img.shields.io/badge/Django-Web%20Dev-092E20?logo=django&logoColor=white)

---

## 📂 Project Directory

| Project | Description | Technologies |
|---------|-------------|--------------|
| [🧠 machine_learning_projects](#-machine-learning-projects) | Classification & regression models | Scikit-Learn, Pandas, NumPy |
| [📊 data_science_dashboard](#-data-science-dashboard) | Interactive ML performance dashboard | Streamlit, Plotly, Pandas |
| [📈 stock_market_dashboard](#-stock-market-dashboard) | Real-time stock analytics | Streamlit, yFinance, Plotly |
| [👤 facial_recognition](#-facial-recognition) | Real-time face detection & identification | TensorFlow, DeepFace, OpenCV |
| [🏥 o2_inventory](#-oxygen-concentrator-inventory-system) | Healthcare inventory management | OOP, CSV, Unit Testing |
| [⚖️ weighted_output_tracker](#%EF%B8%8F-weighted-output-tracker) | Productivity tracking desktop app | Tkinter, PyInstaller |

---

## 🧠 Machine Learning Projects

**Location:** `machine_learning_projects/`

A collection of ML classification and regression models demonstrating end-to-end data science workflows.

### Projects Included:

| Project | Type | Algorithms | Key Concepts |
|---------|------|------------|--------------|
| **Titanic Survival Classifier** | Classification | Logistic Regression, Decision Tree, Random Forest | Feature engineering, confusion matrix, classification reports |
| **House Price Predictor** | Regression | Random Forest, Gradient Boosting, Linear Regression | RMSE evaluation, feature correlation, hyperparameter tuning |
| **Spam Email Classifier** | Classification | Random Forest with TF-IDF | Text vectorization, precision/recall tradeoffs, threshold tuning |
| **Iris Species Classifier** | Classification | Logistic Regression, Decision Tree | Train/test splitting, accuracy scoring |

### Technologies:
- **Scikit-Learn** - Model training and evaluation
- **Pandas & NumPy** - Data manipulation
- **Matplotlib & Seaborn** - Data visualization

---

## 📊 Data Science Dashboard

**Location:** `data_science_dashboard/`

An interactive **Streamlit** dashboard for visualizing and comparing machine learning model performance metrics.

### Features:
- 📁 CSV file upload for custom datasets
- 🎛️ Dynamic model filtering via sidebar controls
- 📊 Grouped bar charts comparing Accuracy, Precision, Recall, F1, and AUC
- 🔵 Precision vs. Recall scatter plots with F1-weighted bubble sizes
- 🔥 Correlation heatmaps for metric analysis
- ⏱️ Training time comparisons

### Tech Stack:
```
Streamlit | Plotly | Pandas | Scikit-Learn
```

### Run Locally:
```bash
cd data_science_dashboard
pip install -r requirements.txt
streamlit run final_app.py
```

---

## 📈 Stock Market Dashboard

**Location:** `stock_market_dashboard/`

A real-time stock analytics dashboard with interactive charts and multi-ticker comparison.

### Features:
- 📉 Candlestick charts with OHLC data
- 🌙 Dark mode toggle
- 📅 Date range filtering
- 📊 Multi-ticker comparison (AAPL, MSFT, SPY, etc.)
- 🔄 Live data from Yahoo Finance API

### Tech Stack:
```
Streamlit | yFinance | Plotly | Pandas
```

### Run Locally:
```bash
cd stock_market_dashboard
pip install -r requirements.txt
streamlit run stock_dashboard.py
```

---

## 👤 Facial Recognition

**Location:** `facial_recognition/`

A real-time facial recognition system using deep learning for face detection and identification.

### Features:
- 🎥 Real-time webcam face detection
- 🔍 Face embedding extraction using VGG-Face model
- 📐 Cosine similarity matching for identity verification
- 👥 Multi-face tracking with bounding box IoU calculations
- 🌐 Streamlit web interface with WebRTC support

### Tech Stack:
```
TensorFlow | Keras | DeepFace | MTCNN | OpenCV | Streamlit | SciPy
```

### Run Locally:
```bash
cd facial_recognition
pip install -r requirements.txt
streamlit run app_face.py
```

---

## 🏥 Oxygen Concentrator Inventory System

**Location:** `o2_inventory/`

A comprehensive inventory management system for healthcare equipment using object-oriented programming.

### Features:
- 📦 Manage Home, Portable, and Pediatric concentrator units
- 🔧 Track repair status and warranty types
- 💰 Automated revenue calculation based on model and warranty
- 💾 CSV persistence for data storage
- ✅ Input validation with business rules
- 🧪 Unit testing with pytest

### Class Hierarchy:
```
Concentrator (Base)
├── HomeConcentrator (+ noise_level)
├── PortableConcentrator (+ battery_level)
└── PediatricConcentrator (+ age, flow_rate ≤ 2L)
```

### Run Locally:
```bash
cd o2_inventory
python o2_concentrator_inventory_system.py
```

---

## ⚖️ Weighted Output Tracker

**Location:** `weighted_output_tracker/`

A productivity tracking desktop application with both CLI and GUI interfaces.

### Features:
- 📊 Weighted scoring system for different unit types
- 🖥️ Tkinter GUI for easy interaction
- 📁 CSV data persistence
- 📈 Daily progress tracking
- 📦 Standalone Windows executable via PyInstaller

### Tech Stack:
```
Python | Tkinter | CSV | PyInstaller
```

### Run Locally:
```bash
cd weighted_output_tracker
python weight_output_gui.py
```

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
