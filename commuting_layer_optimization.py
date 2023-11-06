from qiskit import *
from qiskit.transpiler.passes.optimization.template_matching import TemplateMatching, MaximalMatches, TemplateSubstitution

from qiskit.converters import circuit_to_dagdependency, dagdependency_to_circuit, dagdependency_to_dag
from qiskit.quantum_info import Operator
from qiskit import QuantumCircuit
from qiskit.dagcircuit.dagdependency import DAGDependency
from qiskit.dagcircuit.dagcircuit import DAGCircuit

#from library_template_substitution import TemplateSubstitution

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
    templates.append((template_dag_dep, replacement_dag_dep))

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[1], qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.cx(qreg_q[0], qreg_q[2])
    replacement_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep))

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
    templates.append((template_dag_dep, replacement_dag_dep))

    replacement = QuantumCircuit(qreg_q)
    replacement.x(qreg_q[1])
    replacement.cx(qreg_q[2], qreg_q[0])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement.cx(qreg_q[1], qreg_q[0])
    replacement_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep))

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
    templates.append((template_dag_dep, replacement_dag_dep))

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[1], qreg_q[0])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement.cx(qreg_q[2], qreg_q[0])
    replacement_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep))

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
    templates.append((template_dag_dep, replacement_dag_dep))

    replacement = QuantumCircuit(qreg_q)
    replacement.x(qreg_q[2])
    replacement.cx(qreg_q[0], qreg_q[1])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.cx(qreg_q[2], qreg_q[1])
    replacement_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep))

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
    templates.append((template_dag_dep, replacement_dag_dep))

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[2], qreg_q[1])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.cx(qreg_q[0], qreg_q[1])
    replacement_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep))

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
    templates.append((template_dag_dep, replacement_dag_dep))

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[1], qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement.cx(qreg_q[0], qreg_q[2])
    replacement_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep))

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
    templates.append((template_dag_dep, replacement_dag_dep))

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[0], qreg_q[2])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement.cx(qreg_q[1], qreg_q[2])
    replacement_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep))

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
    templates.append((template_dag_dep, replacement_dag_dep))

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[1], qreg_q[2])
    replacement.cx(qreg_q[0], qreg_q[2])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep))

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
    templates.append((template_dag_dep, replacement_dag_dep))

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[2], qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement.cx(qreg_q[1], qreg_q[0])
    replacement_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep))

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
    templates.append((template_dag_dep, replacement_dag_dep))

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[1], qreg_q[0])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement.cx(qreg_q[2], qreg_q[0])
    replacement_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep))

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
    templates.append((template_dag_dep, replacement_dag_dep))

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[2], qreg_q[1])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.cx(qreg_q[0], qreg_q[1])
    replacement_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep))
    
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
    templates.append((template_dag_dep, replacement_dag_dep))

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[0], qreg_q[1])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.cx(qreg_q[2], qreg_q[1])
    replacement_dag_dep = circuit_to_dagdependency(replacement)
    templates.append((template_dag_dep, replacement_dag_dep))
    
    return templates

def library_template_matching(circuit_dag_dep, template_dag_dep, replacement_dag_dep):

    TemplateSubstitution.run_dag_opt = run_dag_opt
    TemplateSubstitution.__init__ = __init__

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
        substitution = TemplateSubstitution(max_match, circuit_dag_dep, template_dag_dep, replacement_dag_dep)
        substitution.run_dag_opt()
        circ_dag_dep = substitution.dag_dep_optimized
        circ = dagdependency_to_circuit(circ_dag_dep)
        return circ
    
    return None


def commuting_layer_optimization(circuit, templates):

    # Remove once testing is done
    original_circuit = circuit.copy()

    # Begin with fully optimized circuit
    circuit = transpile(circuits=circuit, optimization_level=2)

    # Convert to dag dependency
    circuit_dag_dep = circuit_to_dagdependency(circuit=circuit)

    # Flag to detect if algorithm should be run again on a new optimized circuit
    reduced = True

    while reduced:

        reduced = False

        # For each template
        for template in templates:

            if not is_equivalent(dagdependency_to_circuit(template[0]), dagdependency_to_circuit(template[1])):
                raise ValueError("Templates are not equivalent.")

            # Apply template matching
            commuted_circ = library_template_matching(circuit_dag_dep, template[0], template[1])

            # If match is found
            if commuted_circ is not None:
                reduced_circ = transpile(circuits=commuted_circ, optimization_level=2)

                # If the commutation resulted in a circuit with less operations, repeat process with new circuit
                if sum(reduced_circ.count_ops().values()) < sum(circuit.count_ops().values()):
                    reduced = True
                    circuit = reduced_circ
                    break
    
    # Remove once testing is done
    if not is_equivalent(circuit, original_circuit):
        raise ValueError("Error in function, time to debug.")
        
    return circuit


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
        group = self.substitution_list[0]

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

        # Then add the corresponding template
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

    self.match_stack = max_matches
    self.circuit_dag_dep = circuit_dag_dep
    self.template_dag_dep = template_dag_dep
    self.replacement_dag_dep = replacement_dag_dep

    self.substitution_list = []
    self.unmatched_list = []
    self.dag_dep_optimized = DAGDependency()
    self.dag_optimized = DAGCircuit()

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