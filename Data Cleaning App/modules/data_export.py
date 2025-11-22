import streamlit as st
import pandas as pd
import io

def export_data(df, df_original):
    st.subheader("💾 Export Cleaned Data")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Original Rows", df_original.shape[0])
        st.metric("Cleaned Rows", df.shape[0])
    with col2:
        st.metric("Original Cols", df_original.shape[1])
        st.metric("Cleaned Cols", df.shape[1])
    with col3:
        st.metric("Rows Removed", df_original.shape[0] - df.shape[0])
    
    st.markdown("---")
    st.write("**Cleaned Data Preview:**")
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    export_format = st.radio("Select format", ["CSV", "Excel"], horizontal=True)
    filename = st.text_input("Filename (without extension):", "cleaned_data")
    
    # Provide download buttons directly (no intermediate press required)
    if export_format == "CSV":
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="Download CSV", data=csv_bytes, file_name=f"{filename}.csv", mime="text/csv")
    elif export_format == "Excel":
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Cleaned')
            if df_original is not None:
                try:
                    df_original.to_excel(writer, index=False, sheet_name='Original')
                except Exception:
                    # ignore writing original if it fails
                    pass
        st.download_button(label="Download Excel", data=buffer.getvalue(), file_name=f"{filename}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
