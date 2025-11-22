import streamlit as st
import pandas as pd
import numpy as np

def exploratory_analysis(df):
    st.subheader("📊 Exploratory Data Analysis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", df.shape[0])
    with col2:
        st.metric("Columns", df.shape[1])
    with col3:
        st.metric("Numeric Cols", len(df.select_dtypes(include=[np.number]).columns))
    
    st.markdown("---")
    st.write("**Statistical Summary:**")
    st.dataframe(df.describe().T, use_container_width=True)
