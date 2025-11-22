import streamlit as st
import pandas as pd
import numpy as np

def engineer_features(df):
    st.subheader("⚡ Feature Engineering")
    
    operation = st.radio("Select Operation", ["Create new column", "Normalization", "Standardization"])
    
    if operation == "Create new column":
        col1, col2 = st.columns(2)
        with col1:
            new_col_name = st.text_input("New column name")
            col_a = st.selectbox("First column", df.columns)
        with col2:
            operation_type = st.selectbox("Operation", ["Add", "Subtract", "Multiply", "Divide"])
            col_b = st.selectbox("Second column", df.columns)
        
        if new_col_name and st.button("Create"):
            try:
                if operation_type == "Add":
                    df[new_col_name] = df[col_a] + df[col_b]
                elif operation_type == "Subtract":
                    df[new_col_name] = df[col_a] - df[col_b]
                elif operation_type == "Multiply":
                    df[new_col_name] = df[col_a] * df[col_b]
                elif operation_type == "Divide":
                    df[new_col_name] = df[col_a] / df[col_b]
                
                st.success(f"✅ Column created")
                st.subheader("📋 Updated Dataset:")
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    elif operation == "Normalization":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        selected_cols = st.multiselect("Select columns", numeric_cols)
        if selected_cols and st.button("Apply"):
            for col in selected_cols:
                df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
            st.success("✅ Normalization applied")
            st.subheader("📋 Updated Dataset:")
            st.dataframe(df, use_container_width=True)
    
    elif operation == "Standardization":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        selected_cols = st.multiselect("Select columns", numeric_cols)
        if selected_cols and st.button("Apply"):
            for col in selected_cols:
                df[col] = (df[col] - df[col].mean()) / df[col].std()
            st.success("✅ Standardization applied")
            st.subheader("📋 Updated Dataset:")
            st.dataframe(df, use_container_width=True)
    
    return df
