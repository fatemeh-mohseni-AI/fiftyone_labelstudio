import streamlit as st
import fiftyone as fo
import matplotlib.pyplot as plt
import os
import cv2
import pandas as pd
from fiftyone import Sample
from fiftyone.core.labels import Polyline, Polylines
from collections import Counter
import glob

# ---- config ----
dataset_name = "v5_2"
dataset_root = "/dataset1"
splits = ["train", "valid", "test"]
classes = [
    'Chicken_dead', 'Chicken_healthy', 'Chicken_newcastle', 'Chicken_sick',
    'Ground', 'Hall_feeding', 'Hall_line', 'Hall_watering',
    'Manure_sick', 'bad_area'
]

def count_labels_per_class(dataset_root, splits, classes):
    """Count labels for each class across all splits"""
    class_counts = {cls: 0 for cls in classes}
    total_images = 0
    
    for split in splits:
        labels_dir = os.path.join(dataset_root, split, "labels")
        if not os.path.exists(labels_dir):
            continue
            
        txt_files = glob.glob(os.path.join(labels_dir, "*.txt"))
        total_images += len(txt_files)
        
        for txt_file in txt_files:
            with open(txt_file, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 1:
                        class_id = int(parts[0])
                        if 0 <= class_id < len(classes):
                            class_counts[classes[class_id]] += 1
    
    return class_counts, total_images

def main():
    st.set_page_config(layout="wide", page_title="Dataset Analyzer")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Analysis Tools"])
    
    if page == "Dashboard":
        show_dashboard()
    else:
        show_analysis_tools()

def show_dashboard():
    st.title("🔍 Dataset Analysis Dashboard")
    
    # Dataset Overview
    st.header("📊 Dataset Overview")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dataset Location")
        st.code(f"Root Path: {dataset_root}")
        st.code(f"Available Splits: {', '.join(splits)}")
    
    with col2:
        st.subheader("Classes")
        st.write(f"Number of Classes: {len(classes)}")
        st.write("Class Names:")
        st.write(", ".join(classes))
    
    # Count labels and create summary
    class_counts, total_images = count_labels_per_class(dataset_root, splits, classes)
    
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
    
    # Summary metrics
    st.header("📑 Summary Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Images", total_images)
    with col2:
        st.metric("Total Labels", sum(class_counts.values()))
    with col3:
        st.metric("Average Labels per Image", round(sum(class_counts.values()) / total_images, 2))

def show_analysis_tools():
    st.title("🛠️ Analysis Tools")
    st.write("Select a tool to analyze your dataset:")
    
    if st.button("Count Labels per Class"):
        class_counts, total_images = count_labels_per_class(dataset_root, splits, classes)
        
        # Display results
        st.subheader("Label Distribution Analysis")
        df = pd.DataFrame(list(class_counts.items()), columns=['Class', 'Count'])
        df = df.sort_values('Count', ascending=False)
        st.dataframe(df)
        
        # Visualization
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(df['Class'], df['Count'])
        plt.xticks(rotation=45, ha='right')
        plt.title("Distribution of Labels Across Classes")
        plt.tight_layout()
        st.pyplot(fig)

if __name__ == "__main__":
    main()

