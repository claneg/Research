import numpy as np
from qiskit import *
from qiskit.transpiler import PassManager, preset_passmanagers
from qiskit.transpiler.passes.optimization import TemplateOptimization, Collect2qBlocks, CollectMultiQBlocks
from qiskit.transpiler.passes.optimization.template_matching import TemplateMatching, MaximalMatches, TemplateSubstitution

# Modified TemplateSubstitution
#from library_template_substitution import TemplateSubstitution

from qiskit.converters import circuit_to_dag, circuit_to_dagdependency, dagdependency_to_circuit, dagdependency_to_dag
from qiskit.visualization import dag_drawer
from qiskit.quantum_info import Operator
import os
from qiskit import QuantumCircuit

from library_template_dev import library_template_matching

qreg_q = QuantumRegister(3, 'q')

circuit = QuantumCircuit(qreg_q)
circuit.cx(qreg_q[0], qreg_q[1])
circuit.x(qreg_q[2])
circuit.x(qreg_q[0])
circuit.x(qreg_q[1])
circuit.cx(qreg_q[0], qreg_q[2])
circuit.x(qreg_q[0])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[2])
circuit.x(qreg_q[1])

template = QuantumCircuit(qreg_q)
template.x(qreg_q[0])
template.x(qreg_q[1])
template.cx(qreg_q[0], qreg_q[2])
template.x(qreg_q[0])
template.cx(qreg_q[1], qreg_q[2])

replacement = QuantumCircuit(qreg_q)
replacement.cx(qreg_q[0], qreg_q[2])
replacement.x(qreg_q[0])
replacement.cx(qreg_q[1], qreg_q[2])
replacement.x(qreg_q[0])
replacement.x(qreg_q[1])