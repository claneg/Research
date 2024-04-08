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
Library Template Matching Substitution

This module implements the LibraryTemplateSubstitution class, which runs the library template
substitution algorithm from a list of maximal matches. It substitutes the maximal matches in the 
circuit and creates a new optimized DAGCircuit. 

Author: Christian Grauberger
Date: 10 Nov 2023
"""

from qiskit.dagcircuit.dagdependency import DAGDependency
from qiskit.converters.dagdependency_to_dag import dagdependency_to_dag
from qiskit.transpiler.passes.optimization.template_matching import TemplateSubstitution


class LibraryTemplateSubstitution(TemplateSubstitution):
    """
    Class to run the library template substitution algorithm from the list of maximal matches.
    """

    def __init__(self, max_matches, circuit_dag_dep, template_dag_dep, replacement_dag_dep, user_cost_dict=None):
        """
        Initialize TemplateSubstitution with necessary arguments.
        Args:
            max_matches (list): list of maximal matches obtained from the running
             the template matching algorithm.
            circuit_dag_dep (DAGDependency): circuit in the dag dependency form.
            template_dag_dep (DAGDependency): template in the dag dependency form.
            user_cost_dict (Optional[dict]): user provided cost dictionary that will override
                the default cost dictionary.
        """
        super().__init__(max_matches, circuit_dag_dep, template_dag_dep, user_cost_dict)
        self.replacement_dag_dep = replacement_dag_dep


    def run_dag_opt(self):
            """
            It runs the substitution algorithm and creates the optimized DAGCircuit().
            """
            self._substitution()

            dag_dep_opt = DAGDependency()

            dag_dep_opt.name = self.circuit_dag_dep.name

            qregs = list(self.circuit_dag_dep.qregs.values())
            cregs = list(self.circuit_dag_dep.cregs.values())

            for register in qregs:
                dag_dep_opt.add_qreg(register)

            for register in cregs:
                dag_dep_opt.add_creg(register)

            already_sub = []

            if self.substitution_list:

                # Loop over the different matches.
                for group in self.substitution_list:

                    circuit_sub = group.circuit_config

                    pred = group.pred_block

                    qubit = group.qubit_config[0]

                    if group.clbit_config:
                        clbit = group.clbit_config[0]
                    else:
                        clbit = []

                    # First add all the predecessors of the given match.
                    for elem in pred:
                        node = self.circuit_dag_dep.get_node(elem)
                        inst = node.op.copy()
                        dag_dep_opt.add_op_node(inst, node.qargs, node.cargs)
                        already_sub.append(elem)

                    already_sub = already_sub + circuit_sub

                    # Then add the inverse of the template.
                    for index in range(self.replacement_dag_dep.size()):
                        all_qubits = self.circuit_dag_dep.qubits
                        qarg_t = self.replacement_dag_dep.get_node(index).qindices
                        qarg_c = [qubit[x] for x in qarg_t]
                        qargs = [all_qubits[x] for x in qarg_c]

                        all_clbits = self.circuit_dag_dep.clbits
                        carg_t = self.replacement_dag_dep.get_node(index).cindices

                        if all_clbits and clbit:
                            carg_c = [clbit[x] for x in carg_t]
                            cargs = [all_clbits[x] for x in carg_c]
                        else:
                            cargs = []
                        node = self.replacement_dag_dep.get_node(index)
                        inst = node.op.copy()
                        dag_dep_opt.add_op_node(inst, qargs, cargs)

                # Add the unmatched gates.
                for node_id in self.unmatched_list:
                    node = self.circuit_dag_dep.get_node(node_id)
                    inst = node.op.copy()
                    dag_dep_opt.add_op_node(inst, node.qargs, node.cargs)

                dag_dep_opt._add_predecessors()
                dag_dep_opt._add_successors()
            # If there is no valid match, it returns the original dag.
            else:
                dag_dep_opt = self.circuit_dag_dep

            self.dag_dep_optimized = dag_dep_opt
            self.dag_optimized = dagdependency_to_dag(dag_dep_opt)