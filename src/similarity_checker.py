# src/similarity_checker.py
from typing import Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class NodeSimilarityChecker:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
    
    def calculate_similarity(self, parent: Dict, child: Dict) -> float:
        """
        Calculate the semantic similarity between a parent and child node
        using TF-IDF and cosine similarity
        """
        # Combine name and description for better context
        parent_text = f"{parent['name']} {parent['description']}"
        child_text = f"{child['name']} {child['description']}"
        
        # Vectorize the texts
        tfidf_matrix = self.vectorizer.fit_transform([parent_text, child_text])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        
        return similarity[0][0]
    
    def validate_parent_child_relationships(self, nodes: List[Dict]) -> List[Dict]:
        """
        Validate all parent-child relationships based on semantic similarity
        """
        results = []
        
        # First, organize nodes by level
        levels = {}
        for node in nodes:
            level = node['properties']['level']
            if level not in levels:
                levels[level] = []
            levels[level].append(node)
        
        # Check each level against the previous level
        for level in sorted(levels.keys()):
            if level == 0:
                continue  # Skip root level
                
            parent_level = level - 1
            if parent_level not in levels:
                continue  # No parents available
                
            for child in levels[level]:
                best_similarity = 0
                best_parent = None
                
                for parent in levels[parent_level]:
                    similarity = self.calculate_similarity(parent['properties'], child['properties'])
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_parent = parent
                
                results.append({
                    "child_id": child['identity'],
                    "child_name": child['properties']['name'],
                    "parent_id": best_parent['identity'] if best_parent else None,
                    "parent_name": best_parent['properties']['name'] if best_parent else None,
                    "similarity_score": best_similarity,
                    "level": level,
                    "is_valid": best_similarity > 0.2  # Threshold can be adjusted
                })
        
        return results