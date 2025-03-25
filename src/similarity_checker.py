# src/similarity_checker.py
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class NodeSimilarityChecker:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
    
    def calculate_similarity(self, parent: Dict, child: Dict) -> float:
        """Calculate semantic similarity between nodes"""
        parent_text = f"{parent['name']} {parent['description']}".lower()
        child_text = f"{child['name']} {child['description']}".lower()
        
        # Handle empty descriptions
        if not parent_text.strip() or not child_text.strip():
            return 0.0
            
        tfidf_matrix = self.vectorizer.fit_transform([parent_text, child_text])
        return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    def validate_parent_child_relationships(self, nodes: List[Dict]) -> List[Dict]:
        """Validate relationships with improved logic"""
        results = []
        levels = {}
        
        # Organize nodes by level
        for node in nodes:
            level = node['properties']['level']
            levels.setdefault(level, []).append(node)
        
        # Validate relationships
        for level, children in sorted(levels.items()):
            if level == 0:  # Skip root level
                continue
                
            parents = levels.get(level - 1, [])
            
            for child in children:
                best_match = {
                    "parent": None,
                    "score": 0.0
                }
                
                # Find best parent match
                for parent in parents:
                    score = self.calculate_similarity(
                        parent['properties'],
                        child['properties']
                    )
                    if score > best_match['score']:
                        best_match = {
                            "parent": parent,
                            "score": score
                        }
                
                # Build result with string booleans for JSON
                results.append({
                    "child_id": child['identity'],
                    "child_name": child['properties']['name'],
                    "parent_id": best_match['parent']['identity'] if best_match['parent'] else None,
                    "parent_name": best_match['parent']['properties']['name'] if best_match['parent'] else None,
                    "similarity_score": float(best_match['score']),
                    "level": level,
                    "is_valid": str(best_match['score'] > 0.15)  # Lowered threshold
                })
        
        return results