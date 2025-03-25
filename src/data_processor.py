# src/data_processor.py
import json
from typing import List, Dict

def clean_extracted_data(raw_data: List[Dict]) -> List[Dict]:
    """
    Clean and standardize the extracted data from images
    """
    cleaned_data = []
    
    for item in raw_data:
        # Standardize the data structure
        cleaned_item = {
            "identity": item.get("identity"),
            "labels": item.get("labels", item.get("label", [])),
            "properties": {
                "run_id": item.get("properties", {}).get("run_id"),
                "project_id": item.get("properties", {}).get("project_id"),
                "level": item.get("properties", {}).get("level"),
                "name": item.get("properties", {}).get("name"),
                "description": item.get("properties", {}).get("description"),
                "key": item.get("properties", {}).get("key", 
                      item.get("properties", {}).get("msg", 
                      item.get("properties", {}).get("may", "")))
            },
            "elementId": item.get("elementId", item.get("classwifi", ""))
        }
        cleaned_data.append(cleaned_item)
    
    return cleaned_data

def load_data_from_images(image_files: List[str]) -> List[Dict]:
    """
    Mock function to represent loading data from image files
    In a real implementation, you would use OCR to extract the JSON
    """
    # This would be replaced with actual OCR extraction
    # For now, we'll assume the data is pre-extracted
    with open('data/extracted_data.json', 'r') as f:
        return json.load(f)