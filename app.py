import streamlit as st
import pandas as pd
import numpy as np
from modules.data_loader import load_data
from modules.missing_values import handle_missing_values
from modules.duplicates import handle_duplicates
from modules.outliers import handle_outliers
from modules.data_types import fix_data_types
from modules.text_cleaning import handle_text_encoded_values, clean_text_values
from modules.feature_engineering import engineer_features
from modules.data_export import export_data
from modules.eda import exploratory_analysis
from modules.auth import login_form
from modules.logger import get_logger

st.set_page_config(page_title="Data Cleaning App", page_icon="🧹", layout="wide")

st.title("🧹 Data Cleaning Application")
st.markdown("**A comprehensive tool for data scientists and students to clean and prepare messy datasets**")

logger = get_logger('data-clean-app')
logger.info('Starting Data Cleaning App')

# Authentication
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state.get('logged_in'):
    try:
        logged = login_form()
    except Exception as e:
        logger.exception(f"Login flow raised an exception: {e}")
        st.sidebar.error("Authentication subsystem failed. Check logs for details.")
        st.stop()

    if not logged:
        st.info('Please log in via the sidebar to continue')
        st.stop()

if 'df' not in st.session_state:
    st.session_state.df = None
if 'df_original' not in st.session_state:
    st.session_state.df_original = None

tabs = st.tabs(["📤 Load Data", "📊 EDA", "🔤 Text Cleaning", "⚠️ Missing Values", "🔄 Duplicates", "📈 Outliers", "🏷️ Data Types", "⚡ Features", "💾 Export"])

with tabs[0]:
    st.session_state.df, st.session_state.df_original = load_data()

with tabs[1]:
    if st.session_state.df is not None:
        exploratory_analysis(st.session_state.df)
    else:
        st.warning("Load data first")

with tabs[2]:
    if st.session_state.df is not None:
        choice = st.radio("Text Operation", ["Text-encoded numbers", "Clean text values"])
        if choice == "Text-encoded numbers":
            st.session_state.df = handle_text_encoded_values(st.session_state.df)
        else:
            st.session_state.df = clean_text_values(st.session_state.df)
    else:
        st.warning("Load data first")

with tabs[3]:
    if st.session_state.df is not None:
        st.session_state.df = handle_missing_values(st.session_state.df)
    else:
        st.warning("Load data first")

with tabs[4]:
    if st.session_state.df is not None:
        st.session_state.df = handle_duplicates(st.session_state.df)
    else:
        st.warning("Load data first")

with tabs[5]:
    if st.session_state.df is not None:
        st.session_state.df = handle_outliers(st.session_state.df)
    else:
        st.warning("Load data first")

with tabs[6]:
    if st.session_state.df is not None:
        st.session_state.df = fix_data_types(st.session_state.df)
    else:
        st.warning("Load data first")

with tabs[7]:
    if st.session_state.df is not None:
        st.session_state.df = engineer_features(st.session_state.df)
    else:
        st.warning("Load data first")

with tabs[8]:
    if st.session_state.df is not None:
        export_data(st.session_state.df, st.session_state.df_original)
    else:
        st.warning("Load data first")
