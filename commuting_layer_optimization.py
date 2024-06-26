"""
Commuting Layer Optimization

This Python file was the original development of the TLC optimization algorithm. The is_equivalent and load_template functions are
used in various files including three_layer_optimization.py and three_layer_optimization_test.py. These functions can be moved to 
those files rather than importing from this file.

Author: Christian Grauberger
Date: 09 Nov 2023
"""

from qiskit import *
from qiskit.transpiler.passes.optimization.template_matching import TemplateMatching, MaximalMatches

from qiskit.converters import circuit_to_dagdependency, dagdependency_to_circuit
from qiskit.quantum_info import Operator
from qiskit import QuantumCircuit

from library_template_substitution import LibraryTemplateSubstitution
from custom_optimization_pass import get_custom_pass

from qiskit.quantum_info import Operator


def is_equivalent(circ_1, circ_2):
    return Operator(circ_1).equiv(Operator(circ_2))


def load_templates():
    templates = []

    qreg_q = QuantumRegister(3, 'q')

    # Template 0
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[0])
    template.x(qreg_q[1])
    template.cx(qreg_q[0], qreg_q[2])
    template.x(qreg_q[0])
    template.cx(qreg_q[1], qreg_q[2])
    template_dag_dep = circuit_to_dagdependency(template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[0], qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.cx(qreg_q[1], qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement_dag_dep = circuit_to_dagdependency(replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[1], qreg_q[2])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2.cx(qreg_q[0], qreg_q[2])
    replacement_2_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 1
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[0])
    template.x(qreg_q[1])
    template.x(qreg_q[2])
    template.cx(qreg_q[1], qreg_q[0])
    template.x(qreg_q[1])
    template.cx(qreg_q[2], qreg_q[0])
    template_dag_dep = circuit_to_dagdependency(template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[1], qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.cx(qreg_q[2], qreg_q[0])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement_dag_dep = circuit_to_dagdependency(replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.x(qreg_q[1])
    replacement_2.cx(qreg_q[2], qreg_q[0])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[2])
    replacement_2.cx(qreg_q[1], qreg_q[0])
    replacement_2_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 2
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[0])
    template.x(qreg_q[1])
    template.x(qreg_q[2])
    template.cx(qreg_q[2], qreg_q[0])
    template.cx(qreg_q[1], qreg_q[0])
    template.x(qreg_q[2])
    template_dag_dep = circuit_to_dagdependency(template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[2], qreg_q[0])
    replacement.cx(qreg_q[1], qreg_q[0])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement_dag_dep = circuit_to_dagdependency(replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[1], qreg_q[0])
    replacement_2.x(qreg_q[2])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[2])
    replacement_2.cx(qreg_q[2], qreg_q[0])
    replacement_2_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 3
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[2])
    template.x(qreg_q[0])
    template.x(qreg_q[1])
    template.cx(qreg_q[2], qreg_q[1])
    template.x(qreg_q[2])
    template.cx(qreg_q[0], qreg_q[1])
    template_dag_dep = circuit_to_dagdependency(template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[2], qreg_q[1])
    replacement.x(qreg_q[2])
    replacement.cx(qreg_q[0], qreg_q[1])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement_dag_dep = circuit_to_dagdependency(replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.x(qreg_q[2])
    replacement_2.cx(qreg_q[0], qreg_q[1])
    replacement_2.x(qreg_q[2])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2.cx(qreg_q[2], qreg_q[1])
    replacement_2_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 4
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[2])
    template.x(qreg_q[0])
    template.x(qreg_q[1])
    template.cx(qreg_q[0], qreg_q[1])
    template.cx(qreg_q[2], qreg_q[1])
    template.x(qreg_q[0])
    template_dag_dep = circuit_to_dagdependency(template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[0], qreg_q[1])
    replacement.cx(qreg_q[2], qreg_q[1])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement_dag_dep = circuit_to_dagdependency(replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[2], qreg_q[1])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[2])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2.cx(qreg_q[0], qreg_q[1])
    replacement_2_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 5
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[0])
    template.x(qreg_q[1])
    template.x(qreg_q[2])
    template.cx(qreg_q[0], qreg_q[2])
    template.cx(qreg_q[1], qreg_q[2])
    template.x(qreg_q[0])
    template_dag_dep = circuit_to_dagdependency(template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[0], qreg_q[2])
    replacement.cx(qreg_q[1], qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement_dag_dep = circuit_to_dagdependency(replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[1], qreg_q[2])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[2])
    replacement_2.cx(qreg_q[0], qreg_q[2])
    replacement_2_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 6
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[0])
    template.x(qreg_q[1])
    template.x(qreg_q[2])
    template.cx(qreg_q[1], qreg_q[2])
    template.cx(qreg_q[0], qreg_q[2])
    template.x(qreg_q[1])
    template_dag_dep = circuit_to_dagdependency(template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[1], qreg_q[2])
    replacement.cx(qreg_q[0], qreg_q[2])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement_dag_dep = circuit_to_dagdependency(replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[0], qreg_q[2])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[2])
    replacement_2.cx(qreg_q[1], qreg_q[2])
    replacement_2_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 7
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[0])
    template.x(qreg_q[1])
    template.cx(qreg_q[1], qreg_q[2])
    template.cx(qreg_q[0], qreg_q[2])
    template.x(qreg_q[1])
    template_dag_dep = circuit_to_dagdependency(template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[0], qreg_q[2])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.cx(qreg_q[1], qreg_q[2])
    replacement_dag_dep = circuit_to_dagdependency(replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[1], qreg_q[2])
    replacement_2.cx(qreg_q[0], qreg_q[2])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 8
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[1])
    template.x(qreg_q[2])
    template.cx(qreg_q[1], qreg_q[0])
    template.cx(qreg_q[2], qreg_q[0])
    template.x(qreg_q[1])
    template_dag_dep = circuit_to_dagdependency(template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[1], qreg_q[0])
    replacement.cx(qreg_q[2], qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement_dag_dep = circuit_to_dagdependency(replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[2], qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[2])
    replacement_2.cx(qreg_q[1], qreg_q[0])
    replacement_2_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 9
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[1])
    template.x(qreg_q[2])
    template.cx(qreg_q[2], qreg_q[0])
    template.cx(qreg_q[1], qreg_q[0])
    template.x(qreg_q[2])
    template_dag_dep = circuit_to_dagdependency(template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[2], qreg_q[0])
    replacement.cx(qreg_q[1], qreg_q[0])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement_dag_dep = circuit_to_dagdependency(replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[1], qreg_q[0])
    replacement_2.x(qreg_q[2])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[2])
    replacement_2.cx(qreg_q[2], qreg_q[0])
    replacement_2_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 10
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[2])
    template.x(qreg_q[0])
    template.cx(qreg_q[0], qreg_q[1])
    template.cx(qreg_q[2], qreg_q[1])
    template.x(qreg_q[0])
    template_dag_dep = circuit_to_dagdependency(template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[0], qreg_q[1])
    replacement.cx(qreg_q[2], qreg_q[1])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[0])
    replacement_dag_dep = circuit_to_dagdependency(replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[2], qreg_q[1])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[2])
    replacement_2.x(qreg_q[0])
    replacement_2.cx(qreg_q[0], qreg_q[1])
    replacement_2_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))
    
    # Template 11
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[2])
    template.x(qreg_q[0])
    template.cx(qreg_q[2], qreg_q[1])
    template.cx(qreg_q[0], qreg_q[1])
    template.x(qreg_q[2])
    template_dag_dep = circuit_to_dagdependency(template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[2], qreg_q[1])
    replacement.cx(qreg_q[0], qreg_q[1])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[0])
    replacement_dag_dep = circuit_to_dagdependency(replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[0], qreg_q[1])
    replacement_2.x(qreg_q[2])
    replacement_2.x(qreg_q[2])
    replacement_2.x(qreg_q[0])
    replacement_2.cx(qreg_q[2], qreg_q[1])
    replacement_2_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))
    
    return templates

def library_template_matching(circuit_dag_dep, template_dag_dep, replacement_dag_dep):

    # Collect matches
    pass_ = TemplateMatching(circuit_dag_dep=circuit_dag_dep, template_dag_dep=template_dag_dep)
    pass_.run_template_matching()
    matches = pass_.match_list

    # Review and sort matches, get largest match
    maximal = MaximalMatches(matches)
    maximal.run_maximal_matches()
    max_match = [maximal.max_match_list[0]] if maximal.max_match_list else []

    # If full template found
    if len(max_match[0].match) == template_dag_dep.size():
        substitution = LibraryTemplateSubstitution(max_match, circuit_dag_dep, template_dag_dep, replacement_dag_dep)
        substitution.run_dag_opt()
        circ_dag_dep = substitution.dag_dep_optimized
        circ = dagdependency_to_circuit(circ_dag_dep)
        return circ
    
    return None

def commuting_layer_optimization(circuit, templates):
    
    # Custom pass
    _pass = get_custom_pass()

    # Remove once testing is done
    original_circuit = circuit.copy()

    # Begin with fully optimized circuit
    circuit = transpile(circuits=circuit, optimization_level=2)

    # Convert to dag dependency
    circuit_dag_dep = circuit_to_dagdependency(circuit=circuit)

    # Flag to detect if algorithm should be run again on a new optimized circuit
    reduced = True

    # Repeat with new circuits until no reductions are found
    while reduced:

        reduced = False

        # For each template
        for template in templates:
            
            # Ensure templates are equivalent
            if not is_equivalent(dagdependency_to_circuit(template[0]), dagdependency_to_circuit(template[1])) or not is_equivalent(dagdependency_to_circuit(template[0]), dagdependency_to_circuit(template[2])):
                raise ValueError("Templates are not equivalent.")

            # Collect matches
            pass_ = TemplateMatching(circuit_dag_dep=circuit_dag_dep, template_dag_dep=template[0])
            pass_.run_template_matching()
            matches = pass_.match_list

            # Only keep full matches
            full_matches = [match for match in matches if len(match.match) == template[0].size()]

            # For each full match
            for match in full_matches:

                # Sub in first replacement
                substitution = LibraryTemplateSubstitution([match], circuit_dag_dep, template[0], template[1])
                substitution.run_dag_opt()
                circ_dag_dep = substitution.dag_dep_optimized
                commuted_circ_1 = dagdependency_to_circuit(circ_dag_dep)

                # Sub in second replacement
                substitution = LibraryTemplateSubstitution([match], circuit_dag_dep, template[0], template[2])
                substitution.run_dag_opt()
                circ_dag_dep = substitution.dag_dep_optimized
                commuted_circ_2 = dagdependency_to_circuit(circ_dag_dep)

                if _pass is None:
                    # Optimize both commuted circuits
                    reduced_circ_1 = transpile(circuits=commuted_circ_1, optimization_level=2)
                    reduced_circ_2 = transpile(circuits=commuted_circ_2, optimization_level=2)
                else:
                    reduced_circ_1 = _pass.run(commuted_circ_1)
                    reduced_circ_2 = _pass.run(commuted_circ_2)

                # If the commutation resulted in a circuit with less operations, pick substitution that resulted in least number of operations
                if sum(reduced_circ_1.count_ops().values()) < sum(circuit.count_ops().values()) or sum(reduced_circ_2.count_ops().values()) < sum(circuit.count_ops().values()):
                    reduced = True
                    circuit = reduced_circ_2 if sum(reduced_circ_2.count_ops().values()) < sum(reduced_circ_1.count_ops().values()) else reduced_circ_1

                    # Do not consider next match, restart with new circuit
                    break
            
            # If reduction is found, do not consider next template, restart with new circuit
            if reduced:
                break
    
    # Remove once testing is done
    if not is_equivalent(circuit, original_circuit):
        raise ValueError("Error in function, time to debug.")
        
    return circuit