import streamlit as st
import pandas as pd

def handle_duplicates(df):
    st.subheader("🔄 Handle Duplicates")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Duplicates", df.duplicated().sum())
        if df.duplicated().sum() > 0:
            st.write("**Sample Duplicates:**")
            st.dataframe(df[df.duplicated(keep=False)].head(10), use_container_width=True)
    
    with col2:
        st.write("**Duplicates by Column:**")
        dup_by_col = pd.DataFrame({'Column': df.columns, 'Duplicates': [df[col].duplicated().sum() for col in df.columns]})
        dup_by_col = dup_by_col[dup_by_col['Duplicates'] > 0]
        if len(dup_by_col) > 0:
            st.dataframe(dup_by_col, use_container_width=True)
        else:
            st.info("No duplicates in individual columns")
    
    st.markdown("---")
    strategy = st.radio("Select Strategy", ["Remove all", "By columns", "Keep first/last"])
    
    if strategy == "Remove all":
        if st.button("Remove duplicates"):
            initial = len(df)
            df = df.drop_duplicates()
            st.success(f"✅ Removed {initial - len(df)} duplicates")
            st.subheader("📋 Updated Dataset:")
            st.dataframe(df, use_container_width=True)
    
    elif strategy == "By columns":
        selected_cols = st.multiselect("Select columns", df.columns)
        if selected_cols and st.button("Remove"):
            initial = len(df)
            df = df.drop_duplicates(subset=selected_cols)
            st.success(f"✅ Removed {initial - len(df)} duplicates")
            st.subheader("📋 Updated Dataset:")
            st.dataframe(df, use_container_width=True)
    
    elif strategy == "Keep first/last":
        keep_opt = st.radio("Keep", ["first", "last"])
        if st.button("Remove"):
            initial = len(df)
            df = df.drop_duplicates(keep=keep_opt)
            st.success(f"✅ Removed {initial - len(df)} duplicates")
            st.subheader("📋 Updated Dataset:")
            st.dataframe(df, use_container_width=True)
    
    return df
