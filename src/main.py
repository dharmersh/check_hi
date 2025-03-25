# src/main.py
import json
import numpy as np
from .data_processor import load_data_from_json, clean_extracted_data
from .hierarchy_validator import HierarchyValidator
from .similarity_checker import NodeSimilarityChecker

def visualize_hierarchy(validator):
    """Moved visualization function here"""
    import networkx as nx
    import matplotlib.pyplot as plt
    
    G = nx.DiGraph()
    for node in validator.node_dict.values():
        G.add_node(node.identity, label=f"{node.name} (L{node.level})", level=node.level)
        if node.parent:
            G.add_edge(node.parent.identity, node.identity)
    
    pos = nx.multipartite_layout(G, subset_key="level")
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, 
            labels=nx.get_node_attributes(G, 'label'),
            node_size=2000, node_color='skyblue',
            font_size=10, font_weight='bold')
    plt.show()

def generate_report(validation_results, similarity_results):
    """Generate validation report"""
    return {
        "hierarchy_validation": {
            "total_nodes": len(validation_results),
            "valid_nodes": sum(1 for r in validation_results if r['status'] == 'OK'),
            "invalid_nodes": sum(1 for r in validation_results if r['status'] != 'OK'),
            "details": validation_results
        },
        "similarity_validation": {
            "total_relationships": len(similarity_results),
            "valid_relationships": sum(1 for r in similarity_results if r['is_valid'] == 'True'),
            "invalid_relationships": sum(1 for r in similarity_results if r['is_valid'] == 'False'),
            "average_similarity": float(np.mean([r['similarity_score'] for r in similarity_results])),
            "details": similarity_results
        }
    }

def main():
    """Main execution function"""
    try:
        # Load and clean data
        raw_data = load_data_from_json()
        cleaned_data = clean_extracted_data(raw_data)
        
        # Validate hierarchy
        validator = HierarchyValidator(cleaned_data)
        is_valid, validation_results = validator.validate_hierarchy()
        
        # Validate similarity
        similarity_checker = NodeSimilarityChecker()
        similarity_results = similarity_checker.validate_parent_child_relationships(cleaned_data)
        
        # Generate report
        report = generate_report(validation_results, similarity_results)
        with open('validation_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Visualization (optional - remove if not needed)
        visualize_hierarchy(validator)
        
        return report
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()