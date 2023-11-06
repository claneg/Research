from qiskit import *

from qiskit.converters import circuit_to_dagdependency
from qiskit.visualization import dag_drawer
from qiskit import QuantumCircuit

from library_template_dev import library_template_matching

from commuting_layer_optimization import *

qreg_q = QuantumRegister(3, 'q')

circuit = QuantumCircuit(qreg_q)
circuit.cx(qreg_q[0], qreg_q[1])
circuit.x(qreg_q[2])
circuit.x(qreg_q[0])
circuit.x(qreg_q[1])
circuit.cx(qreg_q[0], qreg_q[2])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.x(qreg_q[0])
circuit.cx(qreg_q[0], qreg_q[2])
circuit.x(qreg_q[1])

circuit_dag_dep = circuit_to_dagdependency(circuit)