import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from ...backend.services.dataset_service import DatasetAnalyzer

def show_analysis_tools():
    st.title("🛠️ Analysis Tools")
    
    analyzer = DatasetAnalyzer()
    
    tool = st.selectbox(
        "Select Analysis Tool",
        ["Label Distribution", "Image Quality Analysis"]
    )
    
    if tool == "Label Distribution":
        show_label_distribution(analyzer)
    else:
        show_image_quality_analysis(analyzer)

def show_label_distribution(analyzer):
    class_counts, total_images = analyzer.count_labels_per_class()
    
    st.subheader("Label Distribution Analysis")
    df = pd.DataFrame(list(class_counts.items()), columns=['Class', 'Count'])
    df = df.sort_values('Count', ascending=False)
    st.dataframe(df)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(df['Class'], df['Count'])
    plt.xticks(rotation=45, ha='right')
    plt.title("Distribution of Labels Across Classes")
    plt.tight_layout()
    st.pyplot(fig)

def show_image_quality_analysis(analyzer):
    split = st.selectbox("Select Split", analyzer.config.splits)
    results = analyzer.analyze_image_quality(split)
    
    if not results:
        st.warning(f"No images found in {split} split")
        return
        
    df = pd.DataFrame(results)
    
    st.subheader("Image Quality Metrics")
    
    # Blur Analysis
    st.write("### Blur Analysis")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(df['blur_score'], bins=50)
    ax.set_xlabel("Blur Score (higher is better)")
    ax.set_ylabel("Count")
    st.pyplot(fig)
    
    # Brightness Analysis
    st.write("### Brightness Analysis")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(df['brightness'], bins=50)
    ax.set_xlabel("Brightness Value")
    ax.set_ylabel("Count")
    st.pyplot(fig)
    
    # Label Size Analysis
    st.write("### Label Size Analysis")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist([size for sizes in df['label_sizes'] for size in sizes], bins=50)
    ax.set_xlabel("Relative Label Size")
    ax.set_ylabel("Count")
    st.pyplot(fig) 