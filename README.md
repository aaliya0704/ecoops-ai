# 🌱 EcoOps AI - Enterprise Sustainability Portal

EcoOps AI is an **intelligent, context-aware green computing traffic controller** built to solve two critical B2B problems: automating compliance with strict corporate sustainability laws (Scope 3 Emissions) and cutting cloud computing bills by up to 50%.

---

## 🚀 The Real-World Solution
Large enterprises spend millions of dollars running non-urgent software scripts, analytics pipelines, and data training workflows during peak hours when the local electricity grid relies on burning coal or gas. 

**EcoOps AI solves this by automatically intercepting and rescheduling non-urgent software tasks to run during hours when regional renewable energy (solar/wind) is flooding the grid.**

### Core System Features:
1. **Predictive Analytics Brain (`brain.py`):** Trains a Machine Learning `RandomForestRegressor` on historical grid logs to forecast the cleanest and cheapest hours of the day.
2. **Context-Aware LLM Evaluator (`classifier.py`):** Uses an LLM Agent (`gpt-4o-mini`) to read code deployment scripts in plain English and automatically decide if a task is safe to delay or must run instantly to save user experience.
3. **Data Ingestion Core (`main.py`):** A robust asynchronous `FastAPI` service providing clean data pipelines for cloud infrastructure logs.
4. **Enterprise Portal (`dashboard.py`):** An interactive web dashboard built with `Streamlit` to showcase monetary savings and immediate carbon drops.

---

## 🛠️ The Tech Stack
* **Language:** Python 3.11+
* **Backend Framework:** FastAPI, Uvicorn
* **Machine Learning Engine:** Scikit-Learn, NumPy, Pandas
* **AI & Language Processing:** OpenAI API (`gpt-4o-mini`), Python-Dotenv
* **User Interface Layout:** Streamlit

---

## 💻 Installation & Setup

Follow these quick steps to get the entire architecture running locally on your computer:

### 1. Clone & Set Up the Workspace Environment
```bash
# Clone this repository (replace with your repo URL later)
git clone https://github.com
cd ecoops-ai

# Make sure you install the precise required library list
pip install -r requirements.txt
```

### 2. Configure Your Secret System Keys
Create a local `.env` file in the root folder to securely hold your keys (this file is hidden from public git uploads):
```text
OPENAI_API_KEY=your_actual_secret_api_key_here
```

### 3. Launch the Application Servers
Open two side-by-side terminals inside your code editor:

**Terminal 1 (Turn on the Data Engine Web Server):**
```bash
uvicorn main:app --reload
```

**Terminal 2 (Turn on the Visual Management Portal):**
```bash
streamlit run dashboard.py
```

Open your web browser and navigate to `http://localhost:8501` to use the fully operational application!
