import streamlit as st
import pandas as pd
import numpy as np

def handle_outliers(df):
    st.subheader("📈 Handle Outliers")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_cols:
        st.warning("No numeric columns found")
        return df
    
    col = st.selectbox("Select column", numeric_cols)
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers_count = ((df[col] < lower) | (df[col] > upper)).sum()
    
    st.metric("Outliers Detected", outliers_count)
    st.write(f"Bounds: [{lower:.2f}, {upper:.2f}]")
    
    action = st.radio("Action", ["Remove", "Cap at bounds", "Replace with median"])
    
    if action == "Remove" and st.button("Apply"):
        initial = len(df)
        df = df[(df[col] >= lower) & (df[col] <= upper)]
        st.success(f"✅ Removed {initial - len(df)} outliers")
        st.subheader("📋 Updated Dataset:")
        st.dataframe(df, use_container_width=True)
    
    elif action == "Cap at bounds" and st.button("Apply"):
        df[col] = df[col].clip(lower=lower, upper=upper)
        st.success("✅ Outliers capped")
        st.subheader("📋 Updated Dataset:")
        st.dataframe(df, use_container_width=True)
    
    elif action == "Replace with median" and st.button("Apply"):
        median = df[col].median()
        df.loc[(df[col] < lower) | (df[col] > upper), col] = median
        st.success("✅ Outliers replaced")
        st.subheader("📋 Updated Dataset:")
        st.dataframe(df, use_container_width=True)
    
    return df
