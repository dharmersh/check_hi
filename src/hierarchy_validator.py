# src/hierarchy_validator.py
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class HierarchyNode:
    identity: int
    level: int
    name: str
    description: str
    children: List['HierarchyNode']
    parent: 'HierarchyNode' = None

class HierarchyValidator:
    def __init__(self, nodes: List[Dict]):
        self.nodes = nodes
        self.root = None
        self.node_dict = {}
        self.build_hierarchy()
    
    def build_hierarchy(self) -> None:
        """Build the hierarchy tree from the flat node list"""
        # Create all nodes first
        for node_data in self.nodes:
            node = HierarchyNode(
                identity=node_data['identity'],
                level=node_data['properties']['level'],
                name=node_data['properties']['name'],
                description=node_data['properties']['description'],
                children=[]
            )
            self.node_dict[node.identity] = node
            
            if node.level == 0:
                self.root = node
        
        # Build parent-child relationships
        for node in self.node_dict.values():
            if node.level > 0:
                # Find potential parents (nodes with level = current level - 1)
                potential_parents = [
                    n for n in self.node_dict.values() 
                    if n.level == node.level - 1
                ]
                
                if potential_parents:
                    # In a real implementation, you'd use similarity to find the best parent
                    # For now, we'll just assign the first potential parent
                    parent = potential_parents[0]
                    parent.children.append(node)
                    node.parent = parent
    
    def validate_hierarchy(self) -> Tuple[bool, List[Dict]]:
        """
        Validate the hierarchy structure and relationships
        Returns a tuple of (is_valid, validation_results)
        """
        validation_results = []
        is_valid = True
        
        # Check all nodes have appropriate level relationships
        for node in self.node_dict.values():
            if node.level > 0 and not node.parent:
                is_valid = False
                validation_results.append({
                    "node_id": node.identity,
                    "node_name": node.name,
                    "level": node.level,
                    "issue": "No parent assigned",
                    "status": "ERROR"
                })
            elif node.level == 0 and node.parent:
                is_valid = False
                validation_results.append({
                    "node_id": node.identity,
                    "node_name": node.name,
                    "level": node.level,
                    "issue": "Root node has a parent",
                    "status": "ERROR"
                })
            else:
                validation_results.append({
                    "node_id": node.identity,
                    "node_name": node.name,
                    "level": node.level,
                    "parent": node.parent.name if node.parent else "None",
                    "issue": "None",
                    "status": "OK"
                })
        
        return is_valid, validation_results
    
    def print_hierarchy(self, node: HierarchyNode = None, indent: int = 0) -> None:
        """Print the hierarchy tree for visualization"""
        if node is None:
            node = self.root
        
        print("  " * indent + f"- {node.name} (Level {node.level}, ID: {node.identity})")
        for child in node.children:
            self.print_hierarchy(child, indent + 1)