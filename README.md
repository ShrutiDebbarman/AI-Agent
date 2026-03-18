# 🤖 AI Data Agent

An intelligent AI-powered data assistant that allows users to query datasets using natural language and get insights instantly.

---

## 🚀 Features

- 💬 Ask questions in plain English
- 🧠 Converts natural language → SQL queries
- 📊 Works with structured datasets (CSV, Excel, etc.)
- ⚡ Fast query execution using DuckDB
- 🖥️ Interactive UI using Streamlit

---

## 🏗️ Architecture

User Query (Natural Language)
        ↓
LLM (OpenAI / Gemini)
        ↓
SQL Query Generation
        ↓
DuckDB Execution
        ↓
Results Display (Streamlit UI)

---

## 🛠️ Tech Stack

- Python
- DuckDB
- Streamlit
- OpenAI API / Gemini API
- Pandas

---

## 📂 Project Structure


AI-Data-Agent/
│── app.py # Streamlit UI
│── agent.py # LLM + SQL logic
│── db.py # DuckDB connection
│── data/ # Input datasets
│── requirements.txt


---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/AI-Data-Agent.git
cd AI-Data-Agent
pip install -r requirements.txt
🔑 Setup API Key
export OPENAI_API_KEY="your_api_key"

or for Gemini:

genai.configure(api_key="your_api_key")
▶️ Run the Project
streamlit run app.py
💡 Example Queries

"What is total sales by region?"

"Top 5 customers by revenue"

"Average order value per month"

📈 Future Improvements

Support for large datasets (10GB+)

Query validation & error handling

Dashboard visualizations

Multi-database support (Postgres, MySQL)

Role-based access

❗ Challenges Solved

Converting ambiguous natural language into SQL

Preventing incorrect SQL generation

Handling schema understanding dynamically

🧠 Learnings

Prompt engineering for SQL generation

Data pipeline design

LLM limitations and optimization
