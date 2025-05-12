import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from ...backend.services.dataset_service import DatasetAnalyzer
from ...backend.config.config import get_config, DatasetType

def show_dataset_selector():
    """Show dataset selection widgets"""
    config_manager = get_config()
    
    # Dataset selection
    available_datasets = list(config_manager.datasets.keys())
    if not available_datasets:
        st.error("No datasets found! Please check your mounted volumes.")
        return False
        
    # Select dataset
    selected_dataset = st.sidebar.selectbox(
        "Select Dataset",
        available_datasets,
        index=available_datasets.index(config_manager.active_dataset) if config_manager.active_dataset else 0
    )
    
    # Get current dataset config
    dataset_config = config_manager.get_dataset(selected_dataset)
    
    # Dataset type selection
    current_type = dataset_config.dataset_type
    selected_type = st.sidebar.selectbox(
        "Dataset Type",
        [DatasetType.BBOX.value, DatasetType.SEGMENT.value],
        index=0 if current_type == DatasetType.BBOX else 1
    )
    
    # Update dataset type if changed
    if selected_type != current_type.value:
        config_manager.set_dataset_type(selected_dataset, DatasetType(selected_type))
    
    # Set as active dataset
    if selected_dataset != config_manager.active_dataset:
        config_manager.set_active_dataset(selected_dataset)
    
    return True

def show_dashboard():
    st.title("🔍 Dataset Analysis Dashboard")
    
    # Show dataset selector in sidebar
    if not show_dataset_selector():
        return
    
    try:
        analyzer = DatasetAnalyzer()
        dataset_config = analyzer.dataset_config
        
        # Dataset Overview
        st.header("📊 Dataset Overview")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Dataset Location")
            st.code(f"Root Path: {dataset_config.dataset_path}")
            st.code(f"Available Splits: {', '.join(dataset_config.splits)}")
        
        with col2:
            st.subheader("Dataset Type")
            st.info(f"Type: {dataset_config.dataset_type.value}")
            st.code(f"Number of Classes: {dataset_config.nc}")
        
        with col3:
            st.subheader("Classes")
            st.write("Class Names:")
            st.write(", ".join(dataset_config.classes))
        
        # Get dataset statistics
        stats = analyzer.get_dataset_stats()
        
        # Show split statistics
        st.header("📈 Dataset Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Images", stats['total_images'])
        with col2:
            st.metric("Total Labels", stats['total_labels'])
        with col3:
            avg_labels = stats['total_labels'] / stats['total_images'] if stats['total_images'] > 0 else 0
            st.metric("Average Labels per Image", f"{avg_labels:.2f}")
        
        # Show split-wise distribution
        st.subheader("Images per Split")
        split_df = pd.DataFrame(
            list(stats['images_per_split'].items()),
            columns=['Split', 'Images']
        )
        st.dataframe(split_df)
        
        # Show class distribution
        st.header("📊 Label Distribution")
        df = pd.DataFrame(
            list(stats['labels_per_class'].items()),
            columns=['Class', 'Count']
        )
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
        
    except ValueError as e:
        st.error(f"Error: {str(e)}")
        st.info("Please select a dataset from the sidebar to continue.")