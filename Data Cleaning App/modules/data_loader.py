import streamlit as st
import pandas as pd
import io
from modules.logger import get_logger

logger = get_logger('data_loader')

def load_data():
    st.subheader("📂 Upload Your Dataset")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["csv", "xlsx", "xls", "json"],
        help="Supported formats: CSV, Excel, JSON"
    )
    
    df = None
    df_original = None
    
    MAX_BYTES = 50 * 1024 * 1024  # 50 MB
    if uploaded_file is not None:
        # basic size validation
        try:
            size = uploaded_file.size
        except Exception:
            size = None
        if size and size > MAX_BYTES:
            st.error(f"File too large ({size / (1024**2):.1f} MB). Max allowed is {MAX_BYTES / (1024**2):.0f} MB")
            return None, None
        try:
            na_values = ['None', 'none', 'NONE', 'null', 'NULL', 'NaN', 'nan', '??', '?', 'NA', 'N/A', '']
            
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, na_values=na_values, keep_default_na=True)
            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.json'):
                df = pd.read_json(uploaded_file)
            
            df_original = df.copy()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Rows", df.shape[0])
            with col2:
                st.metric("Columns", df.shape[1])
            with col3:
                st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            with col4:
                st.metric("Duplicates", df.duplicated().sum())
            
            st.success("✅ Data loaded successfully!")
            logger.info(f"Loaded file {uploaded_file.name} ({size if size else 'unknown size'})")
            st.subheader("📋 Data Preview")
            st.dataframe(df, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            return None, None
    else:
        st.info("👆 Upload a CSV, Excel, or JSON file to get started")
    
    return df, df_original
