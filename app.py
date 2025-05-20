import streamlit as st
import pandas as pd

# Function to clean LinkedIn URLs
def clean_url(url):
    # Remove the https://www. part if it exists
    if url.startswith('https://www.'):
        url = url.replace('https://www.', '')
    
    # Remove any trailing slash (if present)
    if url.endswith('/'):
        url = url[:-1]
    
    return url

# Streamlit interface
st.title("🔗 LinkedIn URL Cleaner and Data Mapper")

file_a = st.file_uploader("Upload File A (CSV with LinkedIn URLs)", type=["csv"])
file_b = st.file_uploader("Upload File B (CSV with URLs to match)", type=["csv"])

if file_a and file_b:
    # Load the files
    df_a = pd.read_csv(file_a)
    df_b = pd.read_csv(file_b)
    
    # Assume the URLs are in a column named 'profile_url' in File A and 'start_url' in File B
    df_a['cleaned_url'] = df_a['profile_url'].apply(clean_url)
    df_b['cleaned_url'] = df_b['start_url'].apply(clean_url)

    st.subheader("Cleaned URLs in File A")
    st.write(df_a[['profile_url', 'cleaned_url']])

    st.subheader("Cleaned URLs in File B")
    st.write(df_b[['start_url', 'cleaned_url']])

    # Matching data using cleaned URLs (like VLOOKUP)
    merged = pd.merge(df_a, df_b, left_on='cleaned_url', right_on='cleaned_url', how='inner')
    
    st.subheader("Merged Data (based on cleaned URLs)")
    st.write(merged)

    # Option to download the merged data
    csv = merged.to_csv(index=False).encode('utf-8')
    st.download_button("Download Merged Data", csv, "merged_data.csv", "text/csv")
