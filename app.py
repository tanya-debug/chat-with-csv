import streamlit as st
import pandas as pd
import ollama
import json
import re
import matplotlib.pyplot as plt

st.set_page_config(page_title="Chat with CSV (Structured + Charts)", layout="wide")
st.title("📊 Chat with CSV")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Preview of Data")
    st.dataframe(df.head())

    user_question = st.text_input("Ask a question (e.g., 'What is the maximum salary?'):") 

    if user_question:
        csv_info = df.head(10).to_csv(index=False)

        prompt = f"""
You are a professional data analyst.
Rules:
1. Always respond in a polite, full-sentence, professional tone.
2. If asked for maximum/minimum values, do not just state numbers—explain which row/individual has that value.
3. If showing a table:
   - Start with a short explanation: "The following table summarizes ..."
4. If showing a graph:
   - Start with: "This graph visualizes ..."
5. Return ONLY valid JSON.

Format:
- If only a textual answer:
  {{"chart_needed": false, "response": "<professional answer>"}}

- If a chart is needed:
  {{"chart_needed": true, "chart_type": "<bar|line|pie|scatter>", "x": "<column>", "y": "<column>", "text_answer": "<professional explanation about the chart>"}}

Data sample:
{csv_info}

Question: {user_question}
"""
        with st.spinner("Thinking..."):
            try:
                response = ollama.chat(
                    model="phi3:mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                llm_response = response["message"]["content"].strip()

                # --- Extract JSON block ---
                json_match = re.search(r"\{.*\}", llm_response, re.DOTALL)
                if json_match:
                    clean_json = json_match.group().replace("'", '"')

                    try:
                        parsed = json.loads(clean_json)

                        if parsed.get("chart_needed"):
                            chart_type = parsed.get("chart_type", "bar")
                            x_col = parsed.get("x")
                            y_col = parsed.get("y")

                            if x_col not in df.columns or y_col not in df.columns:
                                st.error("Model suggested columns not found in CSV.")
                            else:
                                st.info(parsed.get("text_answer", "Here's a chart."))

                                # Small chart
                                fig, ax = plt.subplots(figsize=(3, 2), dpi=100)

                                if chart_type == "bar":
                                    ax.bar(df[x_col], df[y_col])
                                elif chart_type == "line":
                                    ax.plot(df[x_col], df[y_col])
                                elif chart_type == "pie":
                                    ax.pie(df[y_col], labels=df[x_col], autopct='%1.1f%%')
                                elif chart_type == "scatter":
                                    ax.scatter(df[x_col], df[y_col])

                                ax.set_xlabel(x_col)
                                ax.set_ylabel(y_col)
                                plt.xticks(rotation=45)
                                st.pyplot(fig, use_container_width=False)

                        else:
                            # ✅ Show professional full-sentence response
                            st.success(parsed.get("response", "No answer."))

                    except Exception as e:
                        st.error(f"JSON parse error: {e}")
                        st.text("RAW MODEL RESPONSE ↓")
                        st.markdown(llm_response)
                else:
                    st.warning("No valid JSON found. Showing raw output:")
                    st.markdown(llm_response)

            except Exception as e:
                st.error(f"Error: {str(e)}")

else:
    st.info("Please upload a CSV file to start.")
