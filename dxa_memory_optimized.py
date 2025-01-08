"""
Memory-Optimized Dislocation Analysis (DXA) for Large Datasets in OVITO

This script demonstrates how to reduce memory usage by preprocessing datasets
and analyzing only defective regions. Ideal for large-scale atomistic simulations
where memory limitations make full DXA impractical.

Author: Prashant Dwivedi
Repository: Memory-Optimized-DXA-OVITO
"""

# Import necessary libraries
from ovito.io import import_file
from ovito.modifiers import (
    PolyhedralTemplateMatchingModifier, 
    SelectTypeModifier, 
    ExpandSelectionModifier, 
    DislocationAnalysisModifier
)
import os

# File paths
input_file = "data/sample_input.lammpstrj"  # Replace with your input file path
output_file = "results/sample_output.dump"  # Output file path

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Step 1: Load the dataset
pipeline = import_file(input_file)
print(f"Loaded dataset from {input_file}")

# Step 2: Apply Polyhedral Template Matching (PTM) to identify structures
ptm_modifier = PolyhedralTemplateMatchingModifier(
    rmsd_cutoff=0.1  # RMSD threshold for defect detection
)
pipeline.modifiers.append(ptm_modifier)
print("Applied Polyhedral Template Matching (PTM)")

# Step 3: Select defective regions (structure type 'Other')
select_modifier = SelectTypeModifier(
    property='Structure Type',
    types={0}  # 0 corresponds to 'Other' structure type
)
pipeline.modifiers.append(select_modifier)
print("Selected defective regions")

# Step 4: Expand selection to include atoms near defects
expand_modifier = ExpandSelectionModifier(
    neighbor_mode=ExpandSelectionModifier.NeighborMode.BY_NEAREST_NEIGHBORS,
    num_neighbors=10,  # Number of nearest neighbors to include
    iterations=5       # Number of expansion iterations
)
pipeline.modifiers.append(expand_modifier)
print("Expanded selection to include surrounding atoms")

# Step 5: Perform DXA only on the selected subset of atoms
dxa_modifier = DislocationAnalysisModifier(
    only_selected_particles=True,
    input_crystal_type=DislocationAnalysisModifier.CrystalType.BCC  # Assuming BCC material
)
pipeline.modifiers.append(dxa_modifier)
print("Performed Dislocation Analysis (DXA)")

# Step 6: Export results
pipeline.compute().export(output_file, "lammps/dump")
print(f"DXA results saved to {output_file}")
