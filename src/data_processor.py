# src/data_processor.py
import json
from typing import List, Dict

def clean_extracted_data(raw_data: List[Dict]) -> List[Dict]:
    """
    Clean and standardize the extracted data from JSON file
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

def load_data_from_json(json_file_path: str = 'data/extracted_data.json') -> List[Dict]:
    """
    Load data directly from the extracted JSON file
    """
    try:
        with open(json_file_path, 'r') as f:
            raw_data = json.load(f)
        return raw_data
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found at {json_file_path}")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in the extracted data file")