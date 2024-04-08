"""
Template Analysis (Future Work)

This Python file is used for analysis of the three layer commuting compositions identified by Brenna Cole. It is part of the
future work to identify attributes of the compositions that may be generalized to larger qubit counts. The purpose of this file
was to determine if all templates come in equivalent triplets as observed in three-qubit examples. However, this does not seem to
be the case, and the three-qubit cases actually come in groups of 6. More investigation is needed for this

Author: Christian Grauberger
Date: 09 Nov 2023
"""

from three_layer_optimization import is_equivalent
import os
from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator


def read_qasm_files(folder_path):
    qasm_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    circuits = []
    
    for file_name in qasm_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            qasm_code = file.read()
            circuit = QuantumCircuit.from_qasm_str(qasm_code)
            circuits.append(circuit)
    
    return circuits

def get_circuit_signature(circuit):
    operator = Operator(circuit)
    unitary_matrix = operator.data
    signature = tuple(map(tuple, unitary_matrix))
    return signature

def group_equivalent_circuits(circuits):
    circuit_groups = {}

    for circuit in circuits:

        signature = get_circuit_signature(circuit)
        
        if signature in circuit_groups:
            circuit_groups[signature].append(circuit)
        else:
            circuit_groups[signature] = [circuit]
    
    return list(circuit_groups.values())

def print_group_counts(groups):
    size_counts = {}

    for i, group in enumerate(groups):
        size = len(group)
        if size in size_counts:
            size_counts[size] += 1
        else:
            size_counts[size] = 1

    print("Group Counts:")
    for size in sorted(size_counts.keys()):
        count = size_counts[size]
        print(f"Size {size}: {count} groups")


if __name__ == "__main__":
    folder_path = "../FourQBAllMatches"
    circuits = read_qasm_files(folder_path)

    groups = group_equivalent_circuits(circuits)

    print(f"Number of groups: {len(groups)}")
    print_group_counts(groups)