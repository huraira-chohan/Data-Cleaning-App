import streamlit as st
import pandas as pd
import numpy as np

def fix_data_types(df):
    st.subheader("🏷️ Fix Data Types")
    
    st.write("**Current Data Types:**")
    st.dataframe(pd.DataFrame({'Column': df.columns, 'Type': df.dtypes.values}), use_container_width=True)
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        selected_col = st.selectbox("Select column", df.columns)
        new_type = st.selectbox("Convert to", ["int", "float", "string", "category"])
    
    with col2:
        st.write(".")
        st.write(".")
        if st.button("Convert"):
            try:
                if new_type == "int":
                    # Use safe coercion to nullable integer dtype
                    orig_non_na = df[selected_col].notna().sum()
                    coerced = pd.to_numeric(df[selected_col], errors='coerce')
                    non_na_after = coerced.notna().sum()
                    coerced_count = orig_non_na - non_na_after
                    df[selected_col] = coerced.astype('Int64')
                    st.info(f"Coerced {coerced_count} non-numeric values to <NA>")
                elif new_type == "float":
                    coerced = pd.to_numeric(df[selected_col], errors='coerce')
                    coerced_count = df[selected_col].notna().sum() - coerced.notna().sum()
                    df[selected_col] = coerced.astype('float64')
                    st.info(f"Coerced {coerced_count} non-numeric values to NaN")
                elif new_type == "string":
                    df[selected_col] = df[selected_col].astype('string')
                elif new_type == "category":
                    card = df[selected_col].nunique(dropna=True)
                    if card > 1000:
                        st.warning(f"Column has high cardinality ({card}); categories may use a lot of memory")
                    df[selected_col] = df[selected_col].astype('category')

                st.success(f"✅ Converted to {new_type}")
                st.subheader("📋 Updated Dataset:")
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    return df
