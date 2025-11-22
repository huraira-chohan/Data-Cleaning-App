import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer


@st.cache_data
def apply_knn_imputer(df_serializable, n_neighbors=5):
    # KNNImputer expects numeric numpy array; df_serializable should be a dataframe or values
    imputer = KNNImputer(n_neighbors=n_neighbors)
    cols = df_serializable.columns
    transformed = imputer.fit_transform(df_serializable)
    return pd.DataFrame(transformed, columns=cols)

def handle_missing_values(df):
    st.subheader("⚠️ Handle Missing Values")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Missing Values Summary:**")
        missing_data = pd.DataFrame({
            'Column': df.columns,
            'Missing Count': df.isnull().sum().values,
            'Missing %': (df.isnull().sum().values / len(df) * 100).round(2)
        })
        missing_data = missing_data[missing_data['Missing Count'] > 0].sort_values('Missing %', ascending=False)
        
        if len(missing_data) > 0:
            st.dataframe(missing_data, use_container_width=True)
        else:
            st.success("✅ No missing values found!")
            return df
    
    with col2:
        st.write("**Visualization:**")
        missing_pct = (df.isnull().sum() / len(df) * 100)
        missing_pct = missing_pct[missing_pct > 0].sort_values(ascending=False)
        if len(missing_pct) > 0:
            st.bar_chart(missing_pct)
    
    st.markdown("---")
    strategy = st.radio("Select Strategy", ["Drop rows", "Drop columns", "Fill with mean", "Fill with median", "Fill with mode", "KNN Imputation", "Forward fill", "Backward fill", "Fill with custom value"])
    
    if strategy == "Drop rows":
        subset = st.multiselect("Select columns to check", df.columns)
        if subset and st.button("Drop rows"):
            initial = len(df)
            df = df.dropna(subset=subset)
            st.success(f"✅ Removed {initial - len(df)} rows")
            st.subheader("📋 Updated Dataset:")
            st.dataframe(df, use_container_width=True)
    
    elif strategy == "Drop columns":
        threshold = st.slider("Drop columns with missing % above:", 0, 100, 50)
        if st.button("Drop columns"):
            missing_pct = (df.isnull().sum() / len(df) * 100)
            cols_to_drop = missing_pct[missing_pct > threshold].index.tolist()
            if cols_to_drop:
                df = df.drop(columns=cols_to_drop)
                st.success(f"✅ Dropped: {', '.join(cols_to_drop)}")
                st.subheader("📋 Updated Dataset:")
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No columns meet threshold")
    
    elif strategy == "Fill with mean":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            selected_cols = st.multiselect("Select columns", numeric_cols)
            if selected_cols and st.button("Fill"):
                from sklearn.impute import SimpleImputer
                imputer = SimpleImputer(strategy='mean')
                df[selected_cols] = imputer.fit_transform(df[selected_cols])
                st.success("✅ Filled with mean")
                st.subheader("📋 Updated Dataset:")
                st.dataframe(df, use_container_width=True)
    
    elif strategy == "Fill with median":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            selected_cols = st.multiselect("Select columns", numeric_cols)
            if selected_cols and st.button("Fill"):
                from sklearn.impute import SimpleImputer
                imputer = SimpleImputer(strategy='median')
                df[selected_cols] = imputer.fit_transform(df[selected_cols])
                st.success("✅ Filled with median")
                st.subheader("📋 Updated Dataset:")
                st.dataframe(df, use_container_width=True)
    
    elif strategy == "Fill with mode":
        selected_cols = st.multiselect("Select columns", df.columns)
        if selected_cols and st.button("Fill"):
            for col in selected_cols:
                mode_val = df[col].mode()[0] if not df[col].mode().empty else 0
                df[col].fillna(mode_val, inplace=True)
            st.success("✅ Filled with mode")
            st.subheader("📋 Updated Dataset:")
            st.dataframe(df, use_container_width=True)

    elif strategy == "KNN Imputation":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            n_neighbors = st.slider("Number of neighbors", 1, 10, 5)
            if st.button("Apply KNN Imputation"):
                # apply only on numeric columns
                numeric_df = df[numeric_cols]
                imputed = apply_knn_imputer(numeric_df, n_neighbors=n_neighbors)
                df[numeric_cols] = imputed
                st.success("✅ KNN Imputation applied")
                st.subheader("📋 Updated Dataset:")
                st.dataframe(df, use_container_width=True)

    elif strategy == "Forward fill":
        if st.button("Apply forward fill"):
            df = df.ffill()
            st.success("✅ Forward fill applied")
            st.subheader("📋 Updated Dataset:")
            st.dataframe(df, use_container_width=True)
    
    elif strategy == "Backward fill":
        if st.button("Apply backward fill"):
            df = df.bfill()
            st.success("✅ Backward fill applied")
            st.subheader("📋 Updated Dataset:")
            st.dataframe(df, use_container_width=True)
    
    elif strategy == "Fill with custom value":
        selected_cols = st.multiselect("Select columns", df.columns)
        if selected_cols:
            fill_value = st.text_input("Enter fill value")
            if fill_value and st.button("Fill"):
                errors = []
                # tokens considered null-like
                null_strings = ['None', 'none', 'NONE', 'null', 'NULL', 'NaN', 'nan', 'NA', 'N/A', '?', '??']
                for col in selected_cols:
                    try:
                        if df[col].dtype.kind in ('i', 'u', 'f'):
                            # try parse numeric
                            parsed = pd.to_numeric(fill_value, errors='coerce')
                            if pd.isna(parsed):
                                # treat explicit null-like strings as NaN
                                if str(fill_value) in null_strings:
                                    df[col].fillna(np.nan, inplace=True)
                                else:
                                    errors.append(f"Column '{col}': fill value not numeric")
                                    continue
                            else:
                                df[col].fillna(parsed, inplace=True)
                        else:
                            # for non-numeric columns, allow setting to NaN if user entered a null token
                            if str(fill_value) in null_strings:
                                df[col].fillna(np.nan, inplace=True)
                            else:
                                df[col].fillna(fill_value, inplace=True)
                    except Exception as e:
                        errors.append(f"Column '{col}': {e}")
                if errors:
                    for e in errors:
                        st.error(e)
                else:
                    st.success("✅ Filled with custom value")
                st.subheader("📋 Updated Dataset:")
                st.dataframe(df, use_container_width=True)
    
    return df
