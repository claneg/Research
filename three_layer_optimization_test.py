"""
THIS FILE IS FOR TESTING ONLY! File for optimization is three_layer_optimization.py. 
This class contains additional attributes for algorithm evaluation.
"""

"""
Quantum Circuit Three-Layer Commuting Optimization

This Python file implements a three-layer commuting optimization algorithm for quantum circuits.
It leverages three-layer commuting templates to substitute matched patterns in the circuit,
resulting in reduced quantum cost.

Author: Christian Grauberger
Date: 09 Nov 2023
"""

from qiskit.dagcircuit.dagcircuit import DAGCircuit
from qiskit.dagcircuit.dagdependency import DAGDependency
from qiskit.converters import dagdependency_to_dag, dag_to_circuit, circuit_to_dagdependency, dagdependency_to_circuit
from qiskit.compiler import transpile
from qiskit.transpiler.passes.optimization.template_matching import TemplateMatching
from qiskit.extensions import UnitaryGate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.transpiler import PassManager, StagedPassManager
import time

from custom_optimization_pass import get_custom_pass
from library_template_substitution import LibraryTemplateSubstitution
from commuting_layer_optimization import load_templates, is_equivalent


class ThreeLayerOptimization:
    """
    Class for performing three-layer commuting optimization on a quantum circuit.

    This class implements an optimization algorithm based on a list of three-layer commuting
    templates. It substitutes matched templates in the circuit and performs optimization
    to reduce the quantum cost.

    """

    def __init__(self, template_list=None, user_cost_dict=None, optimization_pass=None):
        """
        Initialize the ThreeLayerOptimization instance.

        Args:
            template_list (list): List of three-layer commuting templates. Each template is a tuple,
                                where template[0] is the template to look for, and
                                template[1] and template[2] are the replacement templates.
            user_cost_dict (Optional[dict]): User-provided cost dictionary to override the
                                            default cost dictionary.
            optimization_pass (Optional[int, PassManager, StagedPassManager]):
                                    Specifies the internal optimization pass of the algorithm. It can be either:
                                    - An integer (0-3): Sets the optimization level pass internally.
                                    - A PassManager: An instance of PassManager to customize the optimization passes.
                                    - A StagedPassManager: An instance of StagedPassManager for optimization.
        """

        self.dag_dep_optimized = DAGDependency()
        self.dag_optimized = DAGCircuit()

        # Set internal optimization pass
        if optimization_pass is None:
            self.optimization_pass = get_custom_pass()
        elif isinstance(optimization_pass, int):
            self.optimization_pass = generate_preset_pass_manager(optimization_level=optimization_pass)
        elif isinstance(optimization_pass, (PassManager, StagedPassManager)):
            self.optimization_pass = optimization_pass

        if template_list is not None:
            self.template_list = template_list
        else:
            self.template_list = load_templates()

        if user_cost_dict is not None:
            self.cost_dict = dict(user_cost_dict)
        else:
            self.cost_dict = {
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

        # Testing variables
        self.template_matching_time = 0
        self.template_substitution_time = 0
        self.optimization_pass_time = 0

        self.template_matched = False



    def _quantum_cost(self, dag_dep):
        """
        Calculate the quantum cost of a DAGDependency.
        Args:
            circ (DAGDependency): DAGDependency to calculate the quantum cost for.
        Returns:
            int: Total quantum cost of the circuit.
        """
        total_cost = 0
        unitary_costs = [self.cost_dict['x'], self.cost_dict['cx'], self.cost_dict['ccx']]
        
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
                total_cost += self.cost_dict[node.name]
                
        return total_cost


    def run_dag_opt(self, dag, optimization_level = None):
        """
        Run the three-layer commuting optimization algorithm and create the optimized DAGCircuit.

        Args:
            dag (DAGCircuit): The input DAGCircuit to be optimized.
        """

        # Set internal optimization pass. This should not be necessary because it is set during object init.
        # However, an unknown issue is causing this to be necessary as a temporary work-around. 
        # Also needs addressed in three_layer_optimization.py
        if optimization_level is None:
            self.optimization_pass = get_custom_pass()
        elif isinstance(optimization_level, int):
            self.optimization_pass = generate_preset_pass_manager(optimization_level=optimization_level)
        elif isinstance(optimization_level, (PassManager, StagedPassManager)):
            self.optimization_pass = optimization_level

        # Initalize testing parameters
        template_matching_time = 0
        template_sub_time = 0
        optimization_pass_time = 0

        self.template_matched = False

        # Remove once testing is done
        original_circuit = dag_to_circuit(dag).copy()

        # Begin with fully optimized circuit
        circuit = dag_to_circuit(dag)

        start_time = time.time()
        circuit = self.optimization_pass.run(circuit)

        optimization_pass_time += time.time() - start_time

        # Convert to dag dependency
        circuit_dag_dep = circuit_to_dagdependency(circuit=circuit)

        # Flag to detect if algorithm should be run again on a new optimized circuit
        reduced = True

        # Repeat with new circuits until no reductions are found
        while reduced:

            reduced = False

            # For each template
            for template in self.template_list:
                
                # Ensure templates are equivalent
                if not is_equivalent(dagdependency_to_circuit(template[0]), dagdependency_to_circuit(template[1])) or not is_equivalent(dagdependency_to_circuit(template[0]), dagdependency_to_circuit(template[2])):
                    raise ValueError("Templates are not equivalent.")

                # Collect matches
                pass_ = TemplateMatching(circuit_dag_dep=circuit_dag_dep, template_dag_dep=template[0])

                start_time = time.time()
                pass_.run_template_matching()
                template_matching_time += time.time() - start_time

                matches = pass_.match_list

                # Only keep full matches
                full_matches = [match for match in matches if len(match.match) == template[0].size()]

                # For each full match
                for match in full_matches:
                    
                    self.template_matched = True

                    # Sub in first replacement
                    substitution = LibraryTemplateSubstitution([match], circuit_dag_dep, template[0], template[1])

                    start_time = time.time()
                    substitution.run_dag_opt()
                    template_sub_time += time.time() - start_time

                    circ_dag_dep = substitution.dag_dep_optimized
                    commuted_circ_1 = dagdependency_to_circuit(circ_dag_dep)

                    # Sub in second replacement
                    substitution = LibraryTemplateSubstitution([match], circuit_dag_dep, template[0], template[2])

                    start_time = time.time()
                    substitution.run_dag_opt()
                    template_sub_time += time.time() - start_time

                    circ_dag_dep = substitution.dag_dep_optimized
                    commuted_circ_2 = dagdependency_to_circuit(circ_dag_dep)

                    # Optimize both commuted circuits
                    start_time = time.time()
                    reduced_circ_1 = self.optimization_pass.run(commuted_circ_1)
                    reduced_circ_2 = self.optimization_pass.run(commuted_circ_2)
                    optimization_pass_time += time.time() - start_time

                    # Convert back to DAGDependency for quantum cost calculation
                    reduced_dag_dep_1 = circuit_to_dagdependency(reduced_circ_1)
                    reduced_dag_dep_2 = circuit_to_dagdependency(reduced_circ_2)

                    # Calculate quantum costs
                    cost_1 = self._quantum_cost(reduced_dag_dep_1)
                    cost_2 = self._quantum_cost(reduced_dag_dep_2)
                    original_cost = self._quantum_cost(circ_dag_dep)

                    if cost_1 < original_cost or cost_2 < original_cost:
                        reduced = True
                        # Choose the DAG with the minimum cost
                        circuit_dag_dep = reduced_dag_dep_1 if cost_1 < cost_2 else reduced_dag_dep_2

                        # Do not consider the next match, restart with a new circuit
                        break
                
                # If reduction is found, do not consider next template, restart with new circuit
                if reduced:
                    break
        
        # Remove once testing is done
        if not is_equivalent(circuit, original_circuit):
            raise ValueError("Error in function, time to debug.")
        
        # Final optimization pass using L3 optimization
        circuit = dagdependency_to_circuit(circuit_dag_dep)

        start_time = time.time()
        circuit = transpile(circuits=circuit, optimization_level=3)
        optimization_pass_time += time.time() - start_time

        circuit_dag_dep = circuit_to_dagdependency(circuit)

        self.dag_dep_optimized = circuit_dag_dep
        self.dag_optimized = dagdependency_to_dag(circuit_dag_dep)

        self.optimization_pass_time = optimization_pass_time
        self.template_matching_time = template_matching_time
        self.template_substitution_time = template_sub_time