import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from ...backend.services.dataset_service import DatasetAnalyzer
from ...backend.config.config import get_config, DatasetType
from .dashboard import show_dataset_selector
import numpy as np

def show_analysis_tools():
    st.title("🛠️ Analysis Tools")
    
    # Show dataset selector in sidebar
    if not show_dataset_selector():
        return
    
    try:
        analyzer = DatasetAnalyzer()
        dataset_config = analyzer.dataset_config
        
        tool = st.selectbox(
            "Select Analysis Tool",
            ["Label Distribution", "Image Quality Analysis"]
        )
        
        if tool == "Label Distribution":
            show_label_distribution(analyzer)
        else:
            show_image_quality_analysis(analyzer)
            
    except ValueError as e:
        st.error(f"Error: {str(e)}")
        st.info("Please select a dataset from the sidebar to continue.")

def show_label_distribution(analyzer):
    class_counts, total_images = analyzer.count_labels_per_class()
    
    st.subheader("Label Distribution Analysis")
    
    # Show summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Images", total_images)
    with col2:
        total_labels = sum(class_counts.values())
        st.metric("Total Labels", total_labels)
    with col3:
        avg_labels = total_labels / total_images if total_images > 0 else 0
        st.metric("Average Labels per Image", f"{avg_labels:.2f}")
    
    # Create DataFrame
    df = pd.DataFrame(list(class_counts.items()), columns=['Class', 'Count'])
    df = df.sort_values('Count', ascending=False)
    
    # Add percentage column
    total = df['Count'].sum()
    df['Percentage'] = (df['Count'] / total * 100).round(2)
    
    # Display as table
    st.dataframe(df)
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(df['Class'], df['Count'])
    plt.xticks(rotation=45, ha='right')
    plt.title("Distribution of Labels Across Classes")
    plt.tight_layout()
    st.pyplot(fig)
    
    # Create pie chart
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.pie(df['Count'], labels=df['Class'], autopct='%1.1f%%')
    plt.title("Class Distribution (Percentage)")
    st.pyplot(fig)

def show_image_quality_analysis(analyzer):
    split = st.selectbox("Select Split", analyzer.dataset_config.splits)
    results = analyzer.analyze_image_quality(split)
    
    if not results:
        st.warning(f"No images found in {split} split")
        return
        
    df = pd.DataFrame(results)
    
    st.subheader("Image Quality Metrics")
    
    # Summary statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Blur Analysis")
        blur_stats = {
            "Mean Blur Score": df['blur_score'].mean(),
            "Min Blur Score": df['blur_score'].min(),
            "Max Blur Score": df['blur_score'].max()
        }
        st.write(pd.Series(blur_stats))
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.hist(df['blur_score'], bins=50)
        ax.set_xlabel("Blur Score (higher is better)")
        ax.set_ylabel("Count")
        st.pyplot(fig)
        
        # Show most blurry images
        st.write("Most Blurry Images:")
        blurry_df = df.nsmallest(5, 'blur_score')[['image', 'blur_score']]
        st.dataframe(blurry_df)
    
    with col2:
        st.write("### Brightness Analysis")
        brightness_stats = {
            "Mean Brightness": df['brightness'].mean(),
            "Min Brightness": df['brightness'].min(),
            "Max Brightness": df['brightness'].max()
        }
        st.write(pd.Series(brightness_stats))
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.hist(df['brightness'], bins=50)
        ax.set_xlabel("Brightness Value")
        ax.set_ylabel("Count")
        st.pyplot(fig)
        
        # Show extreme brightness images
        st.write("Extreme Brightness Images:")
        extreme_df = pd.concat([
            df.nsmallest(3, 'brightness')[['image', 'brightness']],
            df.nlargest(3, 'brightness')[['image', 'brightness']]
        ])
        st.dataframe(extreme_df)
    
    # Label Size Analysis
    st.write("### Label Size Analysis")
    all_sizes = [size for sizes in df['label_sizes'] for size in sizes]
    
    if all_sizes:
        size_stats = {
            "Mean Label Size": np.mean(all_sizes),
            "Min Label Size": np.min(all_sizes),
            "Max Label Size": np.max(all_sizes)
        }
        st.write(pd.Series(size_stats))
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.hist(all_sizes, bins=50)
        ax.set_xlabel("Relative Label Size")
        ax.set_ylabel("Count")
        st.pyplot(fig)
        
        # Show images with extreme label sizes
        st.write("Images with Extreme Label Sizes:")
        df['max_label_size'] = df['label_sizes'].apply(lambda x: max(x) if x else 0)
        extreme_df = pd.concat([
            df.nsmallest(3, 'max_label_size')[['image', 'max_label_size']],
            df.nlargest(3, 'max_label_size')[['image', 'max_label_size']]
        ])
        st.dataframe(extreme_df) 