"""
Get Custom Pass

This Python file provides the get_custom_pass function to generate an L3 optimization pass with UnitarySynthesis and
ConsolidateBlocks removed. Future work can aim to use L3 pass with basis gates set as the NCT library to decompose
Unitary nodes rather than removing these passes altogether.

Author: Christian Grauberger
Date: 09 Nov 2023
"""

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.transpiler.passes import UnitarySynthesis, ConsolidateBlocks

def get_custom_pass():
    pass_manager = generate_preset_pass_manager(optimization_level=3)
    
    # Filter out UnitarySynthesis and ConsolidateBlocks from the optimization passes
    for item in pass_manager.optimization._pass_sets:
        item['passes'] = [pass_ for pass_ in item['passes'] if not isinstance(pass_, (UnitarySynthesis, ConsolidateBlocks))]

    return pass_manager

pass_manager = generate_preset_pass_manager(optimization_level=3)
print()