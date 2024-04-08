"""
Generate Random Circuits

This Python file contains functions to generate random NCT circuits given qubit and layer counts.

Author: Christian Grauberger
Date: 09 Nov 2023
"""

from qiskit import *
from qiskit import QuantumCircuit
import random
from math import floor
from itertools import product


def generate_random_layer(num_qubits):
    qubits_used = 0

    # Determine number of each gate
    num_ccx = random.randint(0, floor(num_qubits/3))
    qubits_used += (num_ccx * 3)

    num_cx = random.randint(0, floor((num_qubits - qubits_used) / 2))
    qubits_used += (num_cx * 2)

    num_x = random.randint(0, num_qubits - qubits_used)

    # Generate random qubit permutation
    qubits = list(range(num_qubits))
    random.shuffle(qubits)

    # Create circuit and add gates
    layer = QuantumCircuit(num_qubits)

    i = 0

    for _ in range(num_ccx):
        layer.ccx(qubits[i], qubits[i+1], qubits[i+2])
        i += 3

    for _ in range(num_cx):
        layer.cx(qubits[i], qubits[i+1])
        i += 2

    for _ in range(num_x):
        layer.x(qubits[i])
        i += 1

    return layer

def generate_all_layers(num_qubits):
    layers = []

    for ccx_count, cx_count, x_count in product(range(num_qubits + 1), repeat=3):
        if 3 * ccx_count + 2 * cx_count + x_count <= num_qubits:
            layer_info = {'ccx': ccx_count, 'cx': cx_count, 'x': x_count}
            layers.append(layer_info)

    return layers

def generate_random_circuit(num_qubits, num_layers):
    layers = generate_all_layers(num_qubits)

    circuit = QuantumCircuit(num_qubits)

    while circuit.depth() < num_layers:
        # Choose layer
        layer_info = layers[random.randint(0, len(layers) - 1)]

        # Get qubit list
        qubits = list(range(num_qubits))
        random.shuffle(qubits)

        # Create layer
        layer = QuantumCircuit(num_qubits)


        for _ in range(layer_info['ccx']):
            layer.ccx(qubits.pop(0), qubits.pop(0), qubits.pop(0))
        
        for _ in range(layer_info['cx']):
            layer.cx(qubits.pop(0), qubits.pop(0))
        
        for _ in range(layer_info['x']):
            layer.x(qubits.pop(0))

        # Append to circuit
        circuit = transpile(circuit & layer, optimization_level=2)
        

    return circuit


def generate_all_layers_non_ccx(num_qubits):
    layers = []

    for cx_count, x_count in product(range(num_qubits + 1), repeat=2):
        if 2 * cx_count + x_count <= num_qubits:
            layer_info = {'cx': cx_count, 'x': x_count}
            layers.append(layer_info)

    return layers

def generate_random_circuit_non_ccx(num_qubits, num_layers):
    layers = generate_all_layers(num_qubits)

    circuit = QuantumCircuit(num_qubits)

    while circuit.depth() < num_layers:
        # Choose layer
        layer_info = layers[random.randint(0, len(layers) - 1)]

        # Get qubit list
        qubits = list(range(num_qubits))
        random.shuffle(qubits)

        # Create layer
        layer = QuantumCircuit(num_qubits)
        
        for _ in range(layer_info['cx']):
            layer.cx(qubits.pop(0), qubits.pop(0))
        
        for _ in range(layer_info['x']):
            layer.x(qubits.pop(0))

        # Append to circuit
        circuit = transpile(circuit & layer, optimization_level=2)
        

    return circuit
