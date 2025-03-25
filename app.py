# app.py
import streamlit as st
import json
import networkx as nx
import matplotlib.pyplot as plt
from src.main import main, visualize_hierarchy

def main_app():
    st.set_page_config(page_title="Neo4j Hierarchy Validator", layout="wide")
    st.title("Neo4j Hierarchy Validation Results")
    
    if st.button("Run Validation"):
        with st.spinner("Validating hierarchy..."):
            try:
                # Run validation
                report = main()
                
                # Display results
                st.success("Validation completed successfully!")
                st.json(report)
                
                # Show visualization
                st.pyplot(plt.gcf())
                
            except Exception as e:
                st.error(f"Validation failed: {str(e)}")

if __name__ == "__main__":
    main_app()