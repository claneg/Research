"""
Generate Exhaustive Circuits

This Python file contains functions to exhaustively generate 3-qubit, 5-layer NCT circuits with a template spanning layers 2-4.

Author: Christian Grauberger
Date: 09 Nov 2023
"""

from qiskit import *
from qiskit.transpiler.passes.optimization.template_matching import TemplateMatching, MaximalMatches

from qiskit.converters import circuit_to_dagdependency, dagdependency_to_circuit, dagdependency_to_dag
from qiskit.quantum_info import Operator
from qiskit import QuantumCircuit
from qiskit.dagcircuit.dagdependency import DAGDependency
from qiskit.dagcircuit.dagcircuit import DAGCircuit

from library_template_substitution import LibraryTemplateSubstitution

from qiskit.quantum_info import Operator

def generate_non_ccx_circuits():

    circuits = []

    templates = load_templates()
    layers = generate3QubitLayers()

    for first_layer in layers:
        for template_dag_dep in templates:
            for last_layer in layers:
                template = (template_dag_dep[0])
                circuit = first_layer & template & last_layer
                circuits.append(circuit)

    return circuits

def generate_ccx_circuits():
    circuits = []
    templates = load_templates()
    ccx_layers = generate3QubitCCXLayers()
    layers = generate3QubitLayers()

    # Toffoli first layer
    for first_layer in ccx_layers:
        for template_dag_dep in templates:
            for last_layer in layers:
                template = (template_dag_dep[0])
                circuit = first_layer & template & last_layer
                circuits.append(circuit)

    # Toffoli second layer
    for first_layer in layers:
        for template_dag_dep in templates:
            for last_layer in ccx_layers:
                template = (template_dag_dep[0])
                circuit = first_layer & template & last_layer
                circuits.append(circuit)

    # Toffoli both layers
    for first_layer in ccx_layers:
        for template_dag_dep in templates:
            for last_layer in ccx_layers:
                template = (template_dag_dep[0])
                circuit = first_layer & template & last_layer
                circuits.append(circuit)

    return circuits

# Function from Brenna Cole's repository
def generate3QubitCCXLayers():
    q_circuits = []

    ############################## Toffoli Layers #############
    tcc = QuantumCircuit(3)
    tcc.ccx(1,2,0)
    q_circuits.append(tcc)

    ctc = QuantumCircuit(3)
    ctc.ccx(0,2,1)
    q_circuits.append(ctc)

    cct  = QuantumCircuit(3)
    cct.ccx(0,1,2)
    q_circuits.append(cct)

    return(q_circuits)

def generate3QubitLayers():

    q_circuits = []

    ############################## X Only Layers #############
    xxx = QuantumCircuit(3)
    xxx.x(0)
    xxx.x(1)
    xxx.x(2)
    q_circuits.append((xxx))

    xxi = QuantumCircuit(3)
    xxi.x(0)
    xxi.x(1)
    q_circuits.append(xxi)

    ixx = QuantumCircuit(3)
    ixx.x(1)
    ixx.x(2)
    q_circuits.append(ixx)

    xix = QuantumCircuit(3)
    xix.x(0)
    xix.x(2)
    q_circuits.append(xix)

    xii = QuantumCircuit(3)
    xii.x(0)
    q_circuits.append(xii)

    ixi = QuantumCircuit(3)
    ixi.x(1)
    q_circuits.append(ixi)

    iix = QuantumCircuit(3)
    iix.x(2)
    q_circuits.append(iix)

    ############################### CX and X Layers ################
    tcx = QuantumCircuit(3)
    tcx.cx(1,0)
    tcx.x(2)
    q_circuits.append(tcx)

    txc = QuantumCircuit(3)
    txc.cx(2,0)
    txc.x(1)
    q_circuits.append(txc)

    ctx = QuantumCircuit(3)
    ctx.cx(0,1)
    ctx.x(2)
    q_circuits.append(ctx)

    xtc = QuantumCircuit(3)
    xtc.cx(2,1)
    xtc.x(0)
    q_circuits.append(xtc)

    cxt = QuantumCircuit(3)
    cxt.cx(0,2)
    cxt.x(1)
    q_circuits.append((cxt))

    xct = QuantumCircuit(3)
    xct.cx(1,2)
    xct.x(0)
    q_circuits.append(xct)

    ############################# CNOT Only Layers ############
    tci = QuantumCircuit(3)
    tci.cx(1,0)
    q_circuits.append(tci)

    tic = QuantumCircuit(3)
    tic.cx(2,0)
    q_circuits.append(tic)

    cti = QuantumCircuit(3)
    cti.cx(0,1)
    q_circuits.append(cti)

    itc = QuantumCircuit(3)
    itc.cx(2,1)
    q_circuits.append(itc)

    cit = QuantumCircuit(3)
    cit.cx(0,2)
    q_circuits.append(cit)

    ict = QuantumCircuit(3)
    ict.cx(1,2)
    q_circuits.append(ict)

    return(q_circuits)

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
    template_dag_dep = (template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[0], qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.cx(qreg_q[1], qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement_dag_dep = (replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[1], qreg_q[2])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2.cx(qreg_q[0], qreg_q[2])
    replacement_2_dag_dep = (replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 1
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[0])
    template.x(qreg_q[1])
    template.x(qreg_q[2])
    template.cx(qreg_q[1], qreg_q[0])
    template.x(qreg_q[1])
    template.cx(qreg_q[2], qreg_q[0])
    template_dag_dep = (template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[1], qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.cx(qreg_q[2], qreg_q[0])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement_dag_dep = (replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.x(qreg_q[1])
    replacement_2.cx(qreg_q[2], qreg_q[0])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[2])
    replacement_2.cx(qreg_q[1], qreg_q[0])
    replacement_2_dag_dep = (replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 2
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[0])
    template.x(qreg_q[1])
    template.x(qreg_q[2])
    template.cx(qreg_q[2], qreg_q[0])
    template.cx(qreg_q[1], qreg_q[0])
    template.x(qreg_q[2])
    template_dag_dep = (template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[2], qreg_q[0])
    replacement.cx(qreg_q[1], qreg_q[0])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement_dag_dep = (replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[1], qreg_q[0])
    replacement_2.x(qreg_q[2])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[2])
    replacement_2.cx(qreg_q[2], qreg_q[0])
    replacement_2_dag_dep = (replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 3
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[2])
    template.x(qreg_q[0])
    template.x(qreg_q[1])
    template.cx(qreg_q[2], qreg_q[1])
    template.x(qreg_q[2])
    template.cx(qreg_q[0], qreg_q[1])
    template_dag_dep = (template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[2], qreg_q[1])
    replacement.x(qreg_q[2])
    replacement.cx(qreg_q[0], qreg_q[1])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement_dag_dep = (replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.x(qreg_q[2])
    replacement_2.cx(qreg_q[0], qreg_q[1])
    replacement_2.x(qreg_q[2])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2.cx(qreg_q[2], qreg_q[1])
    replacement_2_dag_dep = (replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 4
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[2])
    template.x(qreg_q[0])
    template.x(qreg_q[1])
    template.cx(qreg_q[0], qreg_q[1])
    template.cx(qreg_q[2], qreg_q[1])
    template.x(qreg_q[0])
    template_dag_dep = (template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[0], qreg_q[1])
    replacement.cx(qreg_q[2], qreg_q[1])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement_dag_dep = (replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[2], qreg_q[1])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[2])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2.cx(qreg_q[0], qreg_q[1])
    replacement_2_dag_dep = (replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 5
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[0])
    template.x(qreg_q[1])
    template.x(qreg_q[2])
    template.cx(qreg_q[0], qreg_q[2])
    template.cx(qreg_q[1], qreg_q[2])
    template.x(qreg_q[0])
    template_dag_dep = (template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[0], qreg_q[2])
    replacement.cx(qreg_q[1], qreg_q[2])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement_dag_dep = (replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[1], qreg_q[2])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[2])
    replacement_2.cx(qreg_q[0], qreg_q[2])
    replacement_2_dag_dep = (replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 6
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[0])
    template.x(qreg_q[1])
    template.x(qreg_q[2])
    template.cx(qreg_q[1], qreg_q[2])
    template.cx(qreg_q[0], qreg_q[2])
    template.x(qreg_q[1])
    template_dag_dep = (template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[1], qreg_q[2])
    replacement.cx(qreg_q[0], qreg_q[2])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement_dag_dep = (replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[0], qreg_q[2])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[2])
    replacement_2.cx(qreg_q[1], qreg_q[2])
    replacement_2_dag_dep = (replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 7
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[0])
    template.x(qreg_q[1])
    template.cx(qreg_q[1], qreg_q[2])
    template.cx(qreg_q[0], qreg_q[2])
    template.x(qreg_q[1])
    template_dag_dep = (template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[0], qreg_q[2])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.cx(qreg_q[1], qreg_q[2])
    replacement_dag_dep = (replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[1], qreg_q[2])
    replacement_2.cx(qreg_q[0], qreg_q[2])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2_dag_dep = (replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 8
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[1])
    template.x(qreg_q[2])
    template.cx(qreg_q[1], qreg_q[0])
    template.cx(qreg_q[2], qreg_q[0])
    template.x(qreg_q[1])
    template_dag_dep = (template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[1], qreg_q[0])
    replacement.cx(qreg_q[2], qreg_q[0])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement_dag_dep = (replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[2], qreg_q[0])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[2])
    replacement_2.cx(qreg_q[1], qreg_q[0])
    replacement_2_dag_dep = (replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 9
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[1])
    template.x(qreg_q[2])
    template.cx(qreg_q[2], qreg_q[0])
    template.cx(qreg_q[1], qreg_q[0])
    template.x(qreg_q[2])
    template_dag_dep = (template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[2], qreg_q[0])
    replacement.cx(qreg_q[1], qreg_q[0])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[1])
    replacement.x(qreg_q[2])
    replacement_dag_dep = (replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[1], qreg_q[0])
    replacement_2.x(qreg_q[2])
    replacement_2.x(qreg_q[1])
    replacement_2.x(qreg_q[2])
    replacement_2.cx(qreg_q[2], qreg_q[0])
    replacement_2_dag_dep = (replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))

    # Template 10
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[2])
    template.x(qreg_q[0])
    template.cx(qreg_q[0], qreg_q[1])
    template.cx(qreg_q[2], qreg_q[1])
    template.x(qreg_q[0])
    template_dag_dep = (template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[0], qreg_q[1])
    replacement.cx(qreg_q[2], qreg_q[1])
    replacement.x(qreg_q[0])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[0])
    replacement_dag_dep = (replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[2], qreg_q[1])
    replacement_2.x(qreg_q[0])
    replacement_2.x(qreg_q[2])
    replacement_2.x(qreg_q[0])
    replacement_2.cx(qreg_q[0], qreg_q[1])
    replacement_2_dag_dep = (replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))
    
    # Template 11
    template = QuantumCircuit(qreg_q)
    template.x(qreg_q[2])
    template.x(qreg_q[0])
    template.cx(qreg_q[2], qreg_q[1])
    template.cx(qreg_q[0], qreg_q[1])
    template.x(qreg_q[2])
    template_dag_dep = (template)

    replacement = QuantumCircuit(qreg_q)
    replacement.cx(qreg_q[2], qreg_q[1])
    replacement.cx(qreg_q[0], qreg_q[1])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[2])
    replacement.x(qreg_q[0])
    replacement_dag_dep = (replacement)

    replacement_2 = QuantumCircuit(qreg_q)
    replacement_2.cx(qreg_q[0], qreg_q[1])
    replacement_2.x(qreg_q[2])
    replacement_2.x(qreg_q[2])
    replacement_2.x(qreg_q[0])
    replacement_2.cx(qreg_q[2], qreg_q[1])
    replacement_2_dag_dep = (replacement)
    templates.append((template_dag_dep, replacement_dag_dep, replacement_2_dag_dep))
    
    return templates