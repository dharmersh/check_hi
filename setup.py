from setuptools import setup, find_packages

setup(
    name="neo4j_hierarchy_validator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
        "streamlit>=1.0.0",
        "networkx>=2.0"
    ],
)