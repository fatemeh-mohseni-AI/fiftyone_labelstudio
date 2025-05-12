import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from ...backend.services.dataset_service import DatasetAnalyzer

def show_dashboard():
    st.title("🔍 Dataset Analysis Dashboard")
    
    analyzer = DatasetAnalyzer()
    config = analyzer.config
    
    # Dataset Overview
    st.header("📊 Dataset Overview")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dataset Location")
        st.code(f"Root Path: {config.dataset_path}")
        st.code(f"Available Splits: {', '.join(config.splits)}")
    
    with col2:
        st.subheader("Classes")
        st.write(f"Number of Classes: {config.nc}")
        st.write("Class Names:")
        st.write(", ".join(config.classes))
    
    # Count labels and create summary
    class_counts, total_images = analyzer.count_labels_per_class()
    
    st.header("📈 Label Distribution")
    
    # Convert to DataFrame for better display
    df = pd.DataFrame(list(class_counts.items()), columns=['Class', 'Count'])
    df = df.sort_values('Count', ascending=False)
    
    # Display as table
    st.subheader("Label Counts per Class")
    st.dataframe(df)
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(df['Class'], df['Count'])
    plt.xticks(rotation=45, ha='right')
    plt.title("Distribution of Labels Across Classes")
    plt.tight_layout()
    st.pyplot(fig) 