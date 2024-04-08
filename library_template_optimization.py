# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Library Template Optimization

This module implements the LibraryTemplateOptimization class, a pass for applying template
matching substitution to a quantum circuit. The pass substitutes all compatible full matches
from a list of library templates, reducing the size of the circuit.

Author: Christian Grauberger
Date: 09 Nov 2023

**Reference:**

[1] Iten, R., Moyard, R., Metger, T., Sutter, D. and Woerner, S., 2020.
Exact and practical pattern matching for quantum circuit optimization.
`arXiv:1909.05270 <https://arxiv.org/abs/1909.05270>`_
"""

from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.dagcircuit import DAGDependency
from qiskit.converters.circuit_to_dagdependency import circuit_to_dagdependency
from qiskit.converters.dag_to_dagdependency import dag_to_dagdependency
from qiskit.converters.dagdependency_to_dag import dagdependency_to_dag
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.transpiler.exceptions import TranspilerError
from qiskit.transpiler.passes.optimization.template_matching import TemplateMatching

from library_template_substitution import LibraryTemplateSubstitution


class LibraryTemplateOptimization(TransformationPass):
    """
    Class for the library template optimization pass.
    """

    def __init__(
        self,
        template_list,
        heuristics_qubits_param=None,
        heuristics_backward_param=None,
    ):
        """
        Args:
            template_list (list[tuple[QuantumCircuit()]]): list of pairs of template 
                circuits and replacement circuits to apply. The first position in the tuple is the
                template to be matched, and the second position is the replacement circuit.
            heuristics_backward_param (list[int]): [length, survivor] Those are the parameters for
                applying heuristics on the backward part of the algorithm. This part of the
                algorithm creates a tree of matching scenario. This tree grows exponentially. The
                heuristics evaluates which scenarios have the longest match and keep only those.
                The length is the interval in the tree for cutting it and survivor is the number
                of scenarios that are kept. We advice to use l=3 and s=1 to have serious time
                advantage. We remind that the heuristics implies losing a part of the maximal
                matches. Check reference for more details.
            heuristics_qubits_param (list[int]): [length] The heuristics for the qubit choice make
                guesses from the dag dependency of the circuit in order to limit the number of
                qubit configurations to explore. The length is the number of successors or not
                predecessors that will be explored in the dag dependency of the circuit, each
                qubits of the nodes are added to the set of authorized qubits. We advice to use
                length=1. Check reference for more details.
        """
        super().__init__()

        self.template_list = template_list
        self.heuristics_qubits_param = (
            heuristics_qubits_param if heuristics_qubits_param is not None else []
        )
        self.heuristics_backward_param = (
            heuristics_backward_param if heuristics_backward_param is not None else []
        )

    def run(self, dag):
        """
        Args:
            dag(DAGCircuit): DAG circuit.
        Returns:
            DAGCircuit: optimized DAG circuit.
        Raises:
            TranspilerError: If the template has not the right form or
             if the output circuit acts differently as the input circuit.
        """
        circuit_dag = dag
        circuit_dag_dep = dag_to_dagdependency(circuit_dag)

        for template in self.template_list:

            # Confirm templates are QuantumCircuit or DAGDependency
            if any(not isinstance(template[i], (QuantumCircuit, DAGDependency)) for i in (0, 1)):
                raise TranspilerError("A template is a Quantumciruit or a DAGDependency.")
            
            # If template has more qubits than circuit, no matches exist
            if len(template[0].qubits) > len(circuit_dag_dep.qubits):
                continue

            # Convert to dagdependency if needed
            template_dag_dep = [circuit_to_dagdependency(template[i]) if isinstance(template[i], QuantumCircuit) else template[i] for i in (0, 1)]


            template_m = TemplateMatching(
                circuit_dag_dep,
                template_dag_dep[0],
                self.heuristics_qubits_param,
                self.heuristics_backward_param,
            )

            template_m.run_template_matching()

            # Only keep full matches
            matches = [match for match in template_m.match_list if len(match.match) == template[0].size()]

            if matches:

                substitution = LibraryTemplateSubstitution(
                    matches,
                    circuit_dag_dep,
                    template_dag_dep[0],
                    template_dag_dep[1]                
                    )

                substitution.run_dag_opt()

                circuit_dag_dep = substitution.dag_dep_optimized
            else:
                continue
        circuit_dag = dagdependency_to_dag(circuit_dag_dep)
        return circuit_dag