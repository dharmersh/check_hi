# src/main.py
import json
from data_processor import load_data_from_images, clean_extracted_data
from hierarchy_validator import HierarchyValidator
from similarity_checker import NodeSimilarityChecker

def main():
    # Load and clean the data
    image_files = [
        "1000219907.jpg",
        "1000219904.jpg",
        "1000219908.jpg",
        "1000219909.jpg",
        "1000219910.jpg"
    ]
    
    raw_data = load_data_from_images(image_files)
    cleaned_data = clean_extracted_data(raw_data)
    
    # Save cleaned data for reference
    with open('data/cleaned_data.json', 'w') as f:
        json.dump(cleaned_data, f, indent=2)
    
    print(f"Loaded and cleaned {len(cleaned_data)} nodes")
    
    # Validate hierarchy structure
    print("\nValidating hierarchy structure...")
    validator = HierarchyValidator(cleaned_data)
    is_valid, validation_results = validator.validate_hierarchy()
    
    print("\nHierarchy Tree:")
    validator.print_hierarchy()
    
    print("\nValidation Results:")
    for result in validation_results:
        status = "✓" if result['status'] == 'OK' else "✗"
        print(f"{status} {result['node_name']} (Level {result['level']}): {result['issue']}")
    
    # Validate parent-child relationships with similarity checking
    print("\nValidating parent-child relationships with similarity checking...")
    similarity_checker = NodeSimilarityChecker()
    similarity_results = similarity_checker.validate_parent_child_relationships(cleaned_data)
    
    print("\nSimilarity Results:")
    for result in similarity_results:
        status = "✓" if result['is_valid'] else "✗"
        print(f"{status} Child: {result['child_name']} -> Parent: {result['parent_name']}")
        print(f"   Similarity score: {result['similarity_score']:.2f}")
    
    # Generate report
    generate_report(validation_results, similarity_results)

def generate_report(validation_results, similarity_results):
    """Generate a comprehensive validation report"""
    report = {
        "hierarchy_validation": {
            "total_nodes": len(validation_results),
            "valid_nodes": sum(1 for r in validation_results if r['status'] == 'OK'),
            "invalid_nodes": sum(1 for r in validation_results if r['status'] != 'OK'),
            "details": validation_results
        },
        "similarity_validation": {
            "total_relationships": len(similarity_results),
            "valid_relationships": sum(1 for r in similarity_results if r['is_valid']),
            "invalid_relationships": sum(1 for r in similarity_results if not r['is_valid']),
            "average_similarity": np.mean([r['similarity_score'] for r in similarity_results]),
            "details": similarity_results
        }
    }
    
    with open('validation_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\nReport generated: validation_report.json")

if __name__ == "__main__":
    main()