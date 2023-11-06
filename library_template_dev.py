import numpy as np
from qiskit import *
from qiskit.transpiler import PassManager, preset_passmanagers
from qiskit.transpiler.passes.optimization import TemplateOptimization, Collect2qBlocks, CollectMultiQBlocks
from qiskit.transpiler.passes.optimization.template_matching import TemplateMatching, MaximalMatches

# Modified TemplateSubstitution
from library_template_substitution import TemplateSubstitution

from qiskit.converters import circuit_to_dag, circuit_to_dagdependency, dagdependency_to_circuit, dagdependency_to_dag
from qiskit.visualization import dag_drawer
from qiskit.quantum_info import Operator
import os
from qiskit import QuantumCircuit

def library_template_matching(circuit_dag_dep, template_dag_dep, replacement_dag_dep):

    pass_ = TemplateMatching(circuit_dag_dep=circuit_dag_dep, template_dag_dep=template_dag_dep)
    pass_.run_template_matching()
    matches = pass_.match_list

    maximal = MaximalMatches(matches)
    maximal.run_maximal_matches()
    max_matches = maximal.max_match_list

    # If full template found
    if len(max_matches[0].match) == template_dag_dep.size():
        substitution = TemplateSubstitution(max_matches, circuit_dag_dep, template_dag_dep, replacement_dag_dep)
        substitution.run_dag_opt()
        circ_dag_dep = substitution.dag_dep_optimized
        circ = dagdependency_to_circuit(circ_dag_dep)

    return circ

qreg_q = QuantumRegister(3, 'q')

template = QuantumCircuit(qreg_q)
template.x(qreg_q[0])
template.x(qreg_q[1])
template.cx(qreg_q[0], qreg_q[2])
template.cx(qreg_q[1], qreg_q[2])
template.x(qreg_q[0])

replacement = QuantumCircuit(qreg_q)
replacement.cx(qreg_q[0], qreg_q[2])
replacement.cx(qreg_q[1], qreg_q[2])
replacement.x(qreg_q[0])
replacement.x(qreg_q[0])
replacement.x(qreg_q[1])

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
template_dag_dep = circuit_to_dagdependency(template)
replacement_dag_dep = circuit_to_dagdependency(replacement)

circ = library_template_matching(circuit_dag_dep, template_dag_dep, replacement_dag_dep)

circ.draw('mpl', filename='replaced.jpg')