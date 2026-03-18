import streamlit as st
import pandas as pd
import duckdb
import google.generativeai as genai
import datetime
import matplotlib.pyplot as plt
from PIL import Image
import pdfplumber

# ----------------------------
# Gemini API Setup
# ----------------------------

genai.configure(api_key="YOUR_GEMINI_API")
model = genai.GenerativeModel("gemini-2.5-flash")

# ----------------------------
# Page Config
# ----------------------------

st.set_page_config(page_title="AI Universal Assistant", layout="wide")

st.title("AI Universal Assistant")

today = datetime.date.today()

# ----------------------------
# Session State
# ----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "datasets" not in st.session_state:
    st.session_state.datasets = {}

# ----------------------------
# File Upload Section
# ----------------------------

st.markdown("### Attach Files")

col1, col2, col3 = st.columns(3)

with col1:
    excel_file = st.file_uploader("Upload Excel", type=["xlsx"])

with col2:
    csv_file = st.file_uploader("Upload CSV", type=["csv"])

with col3:
    image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

pdf_file = st.file_uploader("Upload PDF", type=["pdf"])

# ----------------------------
# Excel Processing
# ----------------------------

if excel_file:

    xls = pd.ExcelFile(excel_file)
    sheet = st.selectbox("Select Sheet", xls.sheet_names)

    df = pd.read_excel(xls, sheet_name=sheet)

    st.session_state.datasets["data"] = df

    st.subheader("Dataset Preview")
    st.dataframe(df.head())


# ----------------------------
# CSV Processing
# ----------------------------

if csv_file:

    df = pd.read_csv(csv_file)

    st.session_state.datasets["data"] = df

    st.subheader("Dataset Preview")
    st.dataframe(df.head())


# ----------------------------
# Image Processing
# ----------------------------

if image_file:

    img = Image.open(image_file)

    with st.chat_message("user"):
        st.image(img, caption="Uploaded Image")

    st.session_state.messages.append(
        {"role": "user", "content": "User uploaded an image"}
    )


# ----------------------------
# PDF Processing
# ----------------------------

if pdf_file:

    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    st.session_state.datasets["pdf_text"] = text

    st.success("PDF loaded successfully")


# ----------------------------
# Show Chat History
# ----------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# ----------------------------
# Chat Input
# ----------------------------

question = st.chat_input("Ask anything...")

if question:

    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.write(question)

    datasets = st.session_state.datasets

    # ----------------------------
    # Prepare Context
    # ----------------------------

    dataset_info = ""

    if "data" in datasets:

        df = datasets["data"]

        dataset_info = f"""
Dataset Columns:
{list(df.columns)}

Sample Rows:
{df.head().to_string()}
"""

    if "pdf_text" in datasets:

        dataset_info += f"""
PDF Content:
{datasets["pdf_text"][:2000]}
"""

    # ----------------------------
    # Prompt
    # ----------------------------

    prompt = f"""
You are an advanced AI assistant.

Today's date: {today}

Conversation history:
{st.session_state.messages[-5:]}

{dataset_info}

User Question:
{question}

Decide the best tool.

Return EXACT format:

TYPE: SQL / CHART / CLEAN_DATA / CODE / PDF_ANALYSIS / GENERAL

SQL:
<query or NONE>

CHART:
bar / line / scatter / pie / none

ANSWER:
<final answer>
"""

    # ----------------------------
    # Gemini Call
    # ----------------------------

    try:

        response = model.generate_content(prompt)

        text = response.text

    except:

        with st.chat_message("assistant"):
            st.error("API error")

        st.stop()

    # ----------------------------
    # Parse Response
    # ----------------------------

    try:

        type_val = text.split("TYPE:")[1].split("SQL:")[0].strip()

        sql = text.split("SQL:")[1].split("CHART:")[0].strip()

        chart = text.split("CHART:")[1].split("ANSWER:")[0].strip().lower()

        answer = text.split("ANSWER:")[1].strip()

    except:

        type_val = "GENERAL"

        answer = text

    # ----------------------------
    # Assistant Response
    # ----------------------------

    with st.chat_message("assistant"):

        # ----------------------------
        # SQL Query
        # ----------------------------

        if type_val == "SQL" and "data" in datasets:

            df = datasets["data"]

            try:

                con = duckdb.connect()

                con.register("data", df)

                result = con.execute(sql).fetchdf()

                st.write(answer)

                st.dataframe(result)

            except Exception as e:

                st.error(str(e))


        # ----------------------------
        # Chart
        # ----------------------------

        elif type_val == "CHART" and "data" in datasets:

            df = datasets["data"]

            try:

                con = duckdb.connect()

                con.register("data", df)

                result = con.execute(sql).fetchdf()

                st.write(answer)

                st.dataframe(result)

                if chart == "bar":
                    st.bar_chart(result)

                elif chart == "line":
                    st.line_chart(result)

                elif chart == "scatter":
                    st.scatter_chart(result)

                elif chart == "area":
                    st.area_chart(result)

            except Exception as e:

                st.error(str(e))


        # ----------------------------
        # Data Cleaning
        # ----------------------------

        elif type_val == "CLEAN_DATA" and "data" in datasets:

            df = datasets["data"]

            cleaned = df.dropna()

            st.write("Cleaned dataset (removed nulls)")

            st.dataframe(cleaned)

            st.write("Summary")

            st.write(cleaned.describe())


        # ----------------------------
        # Code Generation
        # ----------------------------

        elif type_val == "CODE":

            st.write("Generated Code")

            st.code(answer)


        # ----------------------------
        # PDF Analysis
        # ----------------------------

        elif type_val == "PDF_ANALYSIS":

            st.write(answer)


        # ----------------------------
        # General Response
        # ----------------------------

        else:

            st.write(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )