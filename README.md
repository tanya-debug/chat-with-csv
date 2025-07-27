Chat with CSV (Structured + Charts)
---
A Streamlit-based application that lets users upload CSV files, ask natural language questions, and receive AI-generated responses. It can provide both structured text answers and generate simple charts (bar, line, pie, scatter) using a local Ollama model.

Features
---
1. Upload CSV files for analysis
2. Ask natural language questions about the data
3. Receive structured answers or auto-generated charts
4. Uses Ollama (phi3:mini) locally—no external API required

Requirements
-
1. Python 3.9+
2. Ollama installed and running locally
3. Required Python packages:
4. pip install streamlit pandas matplotlib ollama

How to Run
-
1. Clone the repository:
  git clone https://github.com/<your-username>/<repo-name>.git
  cd <repo-name>
2. Make sure Ollama is running and the phi3:mini model is available:
  ollama pull phi3:mini
3. Start the Streamlit app:
  streamlit run app.py
4. Open the URL shown in your terminal (default: http://localhost:8501).
