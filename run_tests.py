"""
Evaluation of TLC Optimization Algorithm

This Python file runs tests to evaluate the performance of the proposed TLC optimization algorithm. The functions can be run
in this file using the main function, or in the run_test.ipynb file to save reduced circuits without having to rerun the tests.

Author: Christian Grauberger
Date: 09 Nov 2023
"""

from qiskit import *
from qiskit.transpiler.passes.optimization.template_matching import TemplateMatching, MaximalMatches
from qiskit.converters import circuit_to_dagdependency, dagdependency_to_circuit, dagdependency_to_dag, circuit_to_dag, dag_to_circuit
from qiskit.quantum_info import Operator
from qiskit import QuantumCircuit
from qiskit.dagcircuit.dagdependency import DAGDependency
from qiskit.dagcircuit.dagcircuit import DAGCircuit
from library_template_substitution import LibraryTemplateSubstitution
from qiskit.quantum_info import Operator
from generate_circuits import generate_non_ccx_circuits, generate_ccx_circuits
from three_layer_optimization_test import ThreeLayerOptimization
import time
import csv
from commuting_layer_optimization import is_equivalent
from qiskit.extensions import UnitaryGate
from generate_random_circ import generate_random_circuit
import os
import random
from custom_optimization_pass import get_custom_pass

def main():
    """
    Driver function to run test cases 
    """
    random.seed(42)

    custom_pass = get_custom_pass()
    non_ccx_circuits = generate_non_ccx_circuits()
    ccx_circuits = generate_ccx_circuits()

    reduced_circuits_2 = run_3x5_tests(non_ccx_circuits, 'non_ccx_2_results.csv', 2)

    reduced_circs = run_3x5_tests(non_ccx_circuits, 'test.csv', 3)

    reduced_circs = run_3x5_tests(non_ccx_circuits, 'non_ccx_results_2.csv', 2)

    run_random_circuits()

def run_3x5_tests(circuits, filename, optimization_pass=None):
    """
    Function to run exhaustive 3-qubit, 5-layer circuits. 

    :param circuits: set of circuits to be run
    :param filename: .csv filename to write results to
    :param optimization_pass: internal optimization pass for TLC algorithm. Defaults to custom pass (TLC 3(-US)). More info in 
        three_layer_optimization.py

    :return: original circuits where L3-optimized cost > TLC-optimized cost
    """
    i = 0

    reduced_circ_index = []

    _pass = ThreeLayerOptimization(optimization_pass=optimization_pass)

    # Specify the file path
    csv_file_path = os.path.join(os.getcwd(), 'Results', filename)

    # Define the header for the CSV file
    header = [
        'Original_X', 'L2_X', 'L3_X', 'TLC_X',
        'Original_CX', 'L2_CX', 'L3_CX', 'TLC_CX',
        'Original_Layers', 'L2_Layers', 'L3_Layers', 'TLC_Layers',
        'L2_Time', 'L3_Time', 'TLC_Time',
        'Original_Cost', 'L2_Cost', 'L3_Cost', 'TLC_Cost',
        'L3_Unitary', 'TLC_Unitary',
        'L3_Unitary_X', 'TLC_Unitary_X',
        'L3_Unitary_CX', 'TLC_Unitary_CX',
        'L3_Unitary_CCX', 'TLC_Unitary_CCX', 'Template_Matched',
        'Template_Matching_Time', 'Template_Substitution_Time', 'Optimization_Pass_Time'
    ]
    
    # Writing data to CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write the header to the CSV file
        csv_writer.writerow(header)

        for circuit in circuits:
            if i % 1 == 0:
                print(f'Iter {i}')

            # Original circuit stats
            orig_x = circuit.count_ops().get('x', 0)
            orig_cx = circuit.count_ops().get('cx', 0)
            orig_layers = circuit.depth()
            orig_cost = quantum_cost(circuit)

            # Level 2 Optimization stats
            start_time = time.time()
            l2_circ = transpile(circuit, optimization_level=2)
            end_time = time.time()

            l2_time = end_time - start_time
            l2_x = l2_circ.count_ops().get('x', 0)
            l2_cx = l2_circ.count_ops().get('cx', 0)
            l2_layers = l2_circ.depth()
            l2_cost = quantum_cost(l2_circ)

            # Level 3 Optimization stats
            start_time = time.time()
            l3_circ = transpile(circuit, optimization_level=3)
            end_time = time.time()

            l3_time = end_time - start_time
            l3_x = l3_circ.count_ops().get('x', 0)
            l3_cx = l3_circ.count_ops().get('cx', 0)
            l3_unitary = l3_circ.count_ops().get('unitary', 0)
            l3_layers = l3_circ.depth()
            l3_cost = quantum_cost(l3_circ)

            l3_unitary_results = decompose_unitary(l3_circ)
            l3_unitary_x, l3_unitary_cx, l3_unitary_ccx = l3_unitary_results

            # 3 Layer Commutation Optimization stats
            start_time = time.time()
            _pass.run_dag_opt(circuit_to_dag(circuit), optimization_pass)
            tlc_circ = dag_to_circuit(_pass.dag_optimized)
            end_time = time.time()

            tlc_time = end_time - start_time
            tlc_x = tlc_circ.count_ops().get('x', 0)
            tlc_cx = tlc_circ.count_ops().get('cx', 0)
            tlc_unitary = tlc_circ.count_ops().get('unitary', 0)
            tlc_layers = tlc_circ.depth()
            tlc_cost = quantum_cost(tlc_circ)

            tlc_unitary_results = decompose_unitary(tlc_circ)
            tlc_unitary_x, tlc_unitary_cx, tlc_unitary_ccx = tlc_unitary_results

            template_matched = _pass.template_matched

            # Additional columns
            template_matching_time = _pass.template_matching_time
            template_substitution_time = _pass.template_substitution_time
            optimization_pass_time = _pass.optimization_pass_time

            if tlc_cost < l3_cost:
                reduced_circ_index.append(i)

            i += 1

            # Write the data to the CSV file
            csv_writer.writerow([
                orig_x, l2_x, l3_x, tlc_x,
                orig_cx, l2_cx, l3_cx, tlc_cx,
                orig_layers, l2_layers, l3_layers, tlc_layers,
                l2_time, l3_time, tlc_time,
                orig_cost, l2_cost, l3_cost, tlc_cost,
                l3_unitary, tlc_unitary,
                l3_unitary_x, tlc_unitary_x, 
                l3_unitary_cx, tlc_unitary_cx,
                l3_unitary_ccx, tlc_unitary_ccx, template_matched,
                template_matching_time, template_substitution_time, optimization_pass_time
            ])
            
            # Checks to confirm equivalence
            if not is_equivalent(circuit, l2_circ):
                print('L2 circ not equivalent.')
                break

            if not is_equivalent(circuit, l3_circ):
                print('L3 circ not equivalent.')
                break

            if not is_equivalent(circuit, tlc_circ):
                print('TLC circ not equivalent.')
                break

    print(f'Data has been written to {csv_file_path}')

    reduced_circs = [circuits[i] for i in reduced_circ_index]

    return reduced_circs

def run_random_circuits(circuits, filename, optimization_level=None):
    """
    Function to run randomly generated circuits. 

    :param circuits: set of circuits to be run
    :param filename: .csv filename to write results to
    :param optimization_pass: internal optimization pass for TLC algorithm. Defaults to custom pass (TLC 3(-US)). More info in 
        three_layer_optimization.py

    :return: original circuits where L3-optimized cost > TLC-optimized cost
    """
    i = 0

    reduced_circ_index = []

    num_iter = 50

    _pass = ThreeLayerOptimization(optimization_pass=optimization_level)

    # Specify the file path
    csv_file_path = os.path.join(os.getcwd(), 'Results', filename)

    # Define the header for the CSV file
    header = [
    'Num_Qubits', 'Num_Layers',
    'Original_X', 'L2_X', 'L3_X', 'TLC_X',
    'Original_CX', 'L2_CX', 'L3_CX', 'TLC_CX',
    'Original_CCX', 'L2_CCX',
    'Original_Layers', 'L2_Layers', 'L3_Layers', 'TLC_Layers',
    'L2_Time', 'L3_Time', 'TLC_Time',
    'Original_Cost', 'L2_Cost', 'L3_Cost', 'TLC_Cost',
    'L3_Unitary', 'TLC_Unitary',
    'L3_Unitary_X', 'TLC_Unitary_X',
    'L3_Unitary_CX', 'TLC_Unitary_CX',
    'L3_Unitary_CCX', 'TLC_Unitary_CCX', 'Template_Matched',
    'Template_Matching_Time', 'Template_Substitution_Time', 'Optimization_Pass_Time'
    ]

    # Writing data to CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the header to the CSV file
        csv_writer.writerow(header)

        for circuit in circuits:
            print(f"Iter {i}")
            i += 1

            # Original circuit stats
            orig_x = circuit.count_ops().get('x', 0)
            orig_cx = circuit.count_ops().get('cx', 0)
            orig_ccx = circuit.count_ops().get('ccx', 0)
            orig_layers = circuit.depth()
            orig_cost = quantum_cost(circuit)

            # Level 2 Optimization stats
            start_time = time.time()
            l2_circ = transpile(circuit, optimization_level=2)
            end_time = time.time()

            l2_time = end_time - start_time
            l2_x = l2_circ.count_ops().get('x', 0)
            l2_cx = l2_circ.count_ops().get('cx', 0)
            l2_ccx = l2_circ.count_ops().get('ccx', 0)

            l2_layers = l2_circ.depth()
            l2_cost = quantum_cost(l2_circ)

            # Level 3 Optimization stats
            start_time = time.time()
            l3_circ = transpile(circuit, optimization_level=3)
            end_time = time.time()

            l3_time = end_time - start_time
            l3_x = l3_circ.count_ops().get('x', 0)
            l3_cx = l3_circ.count_ops().get('cx', 0)
            l3_unitary = l3_circ.count_ops().get('unitary', 0)
            l3_layers = l3_circ.depth()
            l3_cost = quantum_cost(l3_circ)

            l3_unitary_results = decompose_unitary(l3_circ)
            l3_unitary_x, l3_unitary_cx, l3_unitary_ccx = l3_unitary_results

            # 3 Layer Commutation Optimization stats
            start_time = time.time()
            _pass.run_dag_opt(circuit_to_dag(circuit), optimization_level)
            tlc_circ = dag_to_circuit(_pass.dag_optimized)
            end_time = time.time()

            tlc_time = end_time - start_time
            tlc_x = tlc_circ.count_ops().get('x', 0)
            tlc_cx = tlc_circ.count_ops().get('cx', 0)
            tlc_unitary = tlc_circ.count_ops().get('unitary', 0)
            tlc_layers = tlc_circ.depth()
            tlc_cost = quantum_cost(tlc_circ)

            tlc_unitary_results = decompose_unitary(tlc_circ)
            tlc_unitary_x, tlc_unitary_cx, tlc_unitary_ccx = tlc_unitary_results

            template_matched = _pass.template_matched

            # Additional columns
            template_matching_time = _pass.template_matching_time
            template_substitution_time = _pass.template_substitution_time
            optimization_pass_time = _pass.optimization_pass_time

            if tlc_cost < l3_cost:
                reduced_circ_index.append(i)

            # Write the data to the CSV file and flush
            csv_writer.writerow([
                circuit.num_qubits, circuit.depth(), 
                orig_x, l2_x, l3_x, tlc_x,
                orig_cx, l2_cx, l3_cx, tlc_cx,
                orig_ccx, l2_ccx,
                orig_layers, l2_layers, l3_layers, tlc_layers,
                l2_time, l3_time, tlc_time,
                orig_cost, l2_cost, l3_cost, tlc_cost,
                l3_unitary, tlc_unitary,
                l3_unitary_x, tlc_unitary_x,
                l3_unitary_cx, tlc_unitary_cx,
                l3_unitary_ccx, tlc_unitary_ccx, template_matched,
                template_matching_time, template_substitution_time, optimization_pass_time
            ])

            csv_file.flush()  # Flush the file to ensure data is written immediately

    reduced_circs = [circuits[i] for i in reduced_circ_index]

    return reduced_circs


def quantum_cost(circ):
    cost_dict = {
        "id": 0,
        "x": 1,
        "y": 1,
        "z": 1,
        "h": 1,
        "t": 1,
        "tdg": 1,
        "s": 1,
        "sdg": 1,
        "u1": 1,
        "u2": 2,
        "u3": 2,
        "rx": 1,
        "ry": 1,
        "rz": 1,
        "r": 2,
        "cx": 2,
        "cy": 4,
        "cz": 4,
        "ch": 8,
        "swap": 6,
        "iswap": 8,
        "rxx": 9,
        "ryy": 9,
        "rzz": 5,
        "rzx": 7,
        "ms": 9,
        "cu3": 10,
        "crx": 10,
        "cry": 10,
        "crz": 10,
        "ccx": 21,
        "rccx": 12,
        "c3x": 96,
        "rc3x": 24,
        "c4x": 312,
        "p": 1,
    }

    total_cost = 0
    unitary_costs = [cost_dict['x'], cost_dict['cx'], cost_dict['ccx']]

    dag_dep = circuit_to_dagdependency(circ)
    
    for node in dag_dep.get_nodes():

        # For Unitary gates, decompose into 1, 2, and 3 qubit gates.
        # Only NCT library is used in this application, so corresponding
        # costs are added.

        if isinstance(node.op, UnitaryGate):
            circ = node.op.definition
            dag = circuit_to_dagdependency(circ)
            for subnode in dag.get_nodes():
                total_cost += unitary_costs[subnode.op.num_qubits - 1]
        else:
            total_cost += cost_dict[node.name]
            
    return total_cost

def decompose_unitary(circ):
    x = 0
    cx = 0
    ccx = 0

    dag_dep = circuit_to_dagdependency(circ)

    for node in dag_dep.get_nodes():
        if isinstance(node.op, UnitaryGate):
            circ = node.op.definition
            dag = circuit_to_dagdependency(circ)
            for subnode in dag.get_nodes():
                if subnode.op.num_qubits == 1:
                    x += 1
                elif subnode.op.num_qubits == 2:
                    cx += 1
                else:
                    ccx += 1
    
    return (x, cx, ccx)

if __name__ == "__main__":
    main()
