import streamlit as st
#import pandas as pd
import plotly.express as px

conn = st.connection("snowflake")

st.title("Bill's Biggest Loser Competition")

# Form for entry
with st.sidebar:
    st.header("Check-in")
    with st.form("entry_form", clear_on_submit=True):
        name = st.selectbox("Name", ["Mr. Mitchell", "Corey", "Charlie"])
        wt = st.number_input("Weight", min_value=100.0, step=0.1)
        if st.form_submit_button("Submit"):
            with conn.session() as s:
                s.sql(f"INSERT INTO check_ins (participant_name, weight) VALUES ('{name}', {wt})").collect()
            st.success("Recorded!")

# Visualization
data = conn.query("SELECT * FROM weight_loss_db.competition.check_ins")
if not data.empty:
    fig = px.line(data, x="ENTRY_DATE", y="WEIGHT", color="PARTICIPANT_NAME")
    st.plotly_chart(fig)