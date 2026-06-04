<div align="center">
  <h1>🌾 Fasal Saathi</h1>
  <p><em>An Intelligent Agricultural Assistant for Data-Driven Crop Yield Prediction</em></p>
  
  [![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
  [![Framework](https://img.shields.io/badge/UI-Gradio-orange.svg)](https://gradio.app/)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
  [![Hackathon](https://img.shields.io/badge/Smart_India_Hackathon-2023_/_2024-brightgreen.svg)]()
  [![Live Demo](https://img.shields.io/badge/🤗_Hugging_Face-Live_Demo-FF9D00.svg)](https://huggingface.co/spaces/Virat-Ghatge/Fasal_Saathi)
</div>

<hr>

## 📖 About the Project

**Fasal Saathi** (Crop Companion) is a comprehensive, machine-learning-powered platform designed to empower Indian farmers with data-driven agricultural insights. Built for the **Smart India Hackathon**, this project bridges the gap between traditional farming practices and modern AI technology. 

By analyzing local historical data, seasonal trends, input usages (like fertilizers and pesticides), and real-time weather forecasts, Fasal Saathi predicts crop yields with high accuracy and provides actionable recommendations to maximize agricultural output and mitigate risks.

## ✨ Key Features

- **🎯 Multi-Model Prediction Engine:** Utilizes an ensemble of advanced machine learning models (`v1`, `v2`, `v3` including XGBoost and LightGBM) to ensure highly accurate yield predictions.
- **🌤️ Real-Time Weather Integration:** Automatically fetches live weather data and 7-day forecasts for the selected state to inform farming decisions.
- **🌍 Multi-Lingual Support:** Fully accessible user interface with native support for **English, Hindi, and Odia**, ensuring grassroots usability.
- **💡 Smart Recommendations:** Beyond raw numbers, it provides qualitative advice on fertilizer usage, rainfall compensation, and farm size optimization.
- **🖥️ Intuitive UI:** A clean, responsive, and easy-to-use web interface built on Gradio, tailored specifically for non-technical users.

## 🛠️ Tech Stack

- **Frontend / UI:** [Gradio](https://gradio.app/)
- **Backend Core:** Python 3
- **Machine Learning:** Scikit-Learn, XGBoost, LightGBM, Pandas, Numpy
- **External Services:** OpenWeather API / WeatherAPI for live meteorological data

## 📂 Project Architecture

```text
Fasal Saathi/
├── app.py                     # Main Gradio application entry point & UI layout
├── brain.py                   # Core backend logic, recommendation engine & model inference
├── weather.py                 # Weather API integration and data formatting
├── crop_yield.csv             # Primary dataset used for model training
├── pred_model_v1.pkl          # Trained ML Model (Base)
├── pred_model_v2.pkl          # Trained ML Model (Advanced Ensemble)
├── pred_model_v3.pkl          # Trained ML Model (Optimized)
├── WEATHER_SETUP.md           # Documentation for configuring weather API keys
├── .env.example               # Template for environment variables
└── requirements.txt           # Python dependencies and library versions
```

## 🚀 Installation & Setup

Follow these steps to get a local development environment up and running.

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/fasal-saathi.git
cd "fasal-saathi"
```

### 2. Create a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the example environment file and add your actual API keys.
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```
Open the `.env` file and insert your Weather API keys. 

### 5. Setup Weather API
Please refer strictly to the [WEATHER_SETUP.md](WEATHER_SETUP.md) file for detailed instructions on acquiring and configuring your OpenWeather or WeatherAPI keys to ensure the live weather features function correctly.

## 🌐 Live Demo

You can try out the live version of Fasal Saathi without installing anything! It is hosted on Hugging Face Spaces:
👉 **[Fasal Saathi Live Demo](https://huggingface.co/spaces/Virat-Ghatge/Fasal_Saathi)**

## 💻 Local Usage

To start the local development server, simply run:

```bash
python app.py
```

The terminal will output a local URL (typically `http://127.0.0.1:8888`). Open this link in your web browser to interact with the Fasal Saathi platform.

## 🗺️ Future Roadmap

- [ ] **IoT Sensor Integration:** Direct integration with soil moisture and pH sensors for hyper-local predictions.
- [ ] **Live Market Prices:** Fetching real-time mandi (market) prices to advise farmers on the best time to sell.
- [ ] **Expanded Language Support:** Adding more regional languages like Tamil, Telugu, Bengali, and Marathi.
- [ ] **Pest Disease Detection:** A computer vision module to detect crop diseases via smartphone camera uploads.

<div align="center">
  <br>
  <p>Built with ❤️ for the farmers of India.</p>
</div>
