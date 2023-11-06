import numpy as np
from qiskit import *
from qiskit.transpiler import PassManager, preset_passmanagers
from qiskit.transpiler.passes.optimization import TemplateOptimization, Collect2qBlocks, CollectMultiQBlocks
from qiskit.transpiler.passes.optimization.template_matching import *
from qiskit.converters import circuit_to_dag, circuit_to_dagdependency, dagdependency_to_circuit, dagdependency_to_dag
from qiskit.visualization import dag_drawer
from qiskit.quantum_info import Operator
import os
from qiskit import QuantumCircuit

identity = QuantumCircuit(3)

identity.cx(1, 2)
identity.cx(0, 1)
identity.cx(1, 2)
identity.cx(0, 1)
identity.cx(0, 2)

circuit = QuantumCircuit(3)

circuit.x(2)
circuit.cx(1, 2)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.x(1)

dag_templates = []
dag_templates.append(circuit_to_dagdependency(identity))

dag1 = circuit_to_dagdependency(circuit)

pass_ = TemplateMatching(circuit_dag_dep=dag1, template_dag_dep=dag_templates[0])
pass_.run_template_matching()
matches = pass_.match_list

maximal = MaximalMatches(matches)
maximal.run_maximal_matches()
max_matches = maximal.max_match_list

substitution = TemplateSubstitution(max_matches, pass_.circuit_dag_dep, pass_.template_dag_dep)
substitution.run_dag_opt()
circ_dag_dep = substitution.dag_dep_optimized
circ = dagdependency_to_circuit(circ_dag_dep)

circ.draw('mpl')