import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from numpy_impl import pass_intensity


def qiskit_pair_pass_probability(prev_deg: float, curr_deg: float) -> float:
    """
    Use Qiskit to compute the probability that a photon polarized at prev_deg
    passes a polarizer at curr_deg.

    This should equal cos^2(curr_deg - prev_deg).
    """
    prev_rad = np.deg2rad(prev_deg)
    curr_rad = np.deg2rad(curr_deg)

    qc = QuantumCircuit(1)

    # Prepare the photon polarization direction: |prev>
    qc.ry(2 * prev_rad, 0)

    # Rotate the current polarizer direction back to the |0> measurement basis
    qc.ry(-2 * curr_rad, 0)

    state = Statevector.from_instruction(qc)

    probs = state.probabilities()

    # probs[0] means probability of measuring |0>
    # Here, measuring |0> means passing the polarizer.
    return float(probs[0])


def qiskit_pass_intensity(
    initial_intensity: float,
    angles_deg: list[float],
    unpolarized_input: bool = True
) -> float:
    """
    Qiskit validation version of pass_intensity().
    It should match the NumPy implementation.
    """
    if initial_intensity < 0:
        raise ValueError("initial_intensity must be non-negative")

    if len(angles_deg) == 0:
        return float(initial_intensity)

    intensity = float(initial_intensity)

    if unpolarized_input:
        intensity *= 0.5

    for prev, curr in zip(angles_deg[:-1], angles_deg[1:]):
        probability = qiskit_pair_pass_probability(prev, curr)
        intensity *= probability

    return float(intensity)


def run_qiskit_validation() -> None:
    test_cases = [
        (1, [], True),
        (1, [0], True),
        (1, [0, 90], True),
        (1, [0, 45, 90], True),
        (1, [0, 30, 60, 90], True),
        (10, [0, 45], False),
    ]

    for initial_intensity, angles_deg, unpolarized_input in test_cases:
        numpy_result = pass_intensity(
            initial_intensity,
            angles_deg,
            unpolarized_input
        )

        qiskit_result = qiskit_pass_intensity(
            initial_intensity,
            angles_deg,
            unpolarized_input
        )

        print("case:", initial_intensity, angles_deg, unpolarized_input)
        print("NumPy result: ", numpy_result)
        print("Qiskit result:", qiskit_result)
        print()

        assert np.isclose(numpy_result, qiskit_result)

    print("All Qiskit validation tests passed.")


if __name__ == "__main__":
    run_qiskit_validation()