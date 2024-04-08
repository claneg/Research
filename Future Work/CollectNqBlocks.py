from qiskit import *
from qiskit.transpiler.passes.optimization import CollectMultiQBlocks
from qiskit.transpiler.passes.optimization.template_matching import *


def Collect3qBlocks(dag):
    _collector = CollectMultiQBlocks(3)
    _collector.run(dag)

    all_blocks = _collector.property_set["block_list"]
    new_blocks = []

    for block in all_blocks:
        qubits = set()
        for op in block:
            for arg in op.qargs:
                qubits.add(arg.index)
            if len(qubits) == 3:
                new_blocks.append(block)
                break

    return new_blocks

def CollectNqBlocks(dag, N_qubits : int):
    _collector = CollectMultiQBlocks(N_qubits)
    _collector.run(dag)

    all_blocks = _collector.property_set["block_list"]
    new_blocks = []

    for block in all_blocks:
        qubits = set()
        for op in block:
            for arg in op.qargs:
                qubits.add(arg.index)
            if len(qubits) == N_qubits:
                new_blocks.append(block)
                break

    return new_blocks
