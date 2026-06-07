import importlib.util
from pathlib import Path

import numpy as np
import pytest

from numpy_impl import pass_intensity


def load_qiskit_check_module():
    """
    Load qiskit_check.py as a Python module.

    We use this method because the filename starts with a number,
    so it cannot be imported by normal syntax like:
    import 04_qiskit_check
    """
    current_dir = Path(__file__).parent
    module_path = current_dir / "qiskit_check.py"

    spec = importlib.util.spec_from_file_location(
        "qiskit_check",
        module_path
    )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


qiskit_check = load_qiskit_check_module()


def test_no_polarizer_returns_initial_intensity():
    result = pass_intensity(
        initial_intensity=1,
        angles_deg=[],
        unpolarized_input=True
    )

    assert isinstance(result, float)
    assert np.isclose(result, 1.0)


def test_unpolarized_light_through_one_polarizer_is_halved():
    result = pass_intensity(
        initial_intensity=1,
        angles_deg=[0],
        unpolarized_input=True
    )

    assert np.isclose(result, 0.5)


def test_two_perpendicular_polarizers_block_light():
    result = pass_intensity(
        initial_intensity=1,
        angles_deg=[0, 90],
        unpolarized_input=True
    )

    assert np.isclose(result, 0.0)


def test_three_polarizers_with_middle_45_degrees():
    result = pass_intensity(
        initial_intensity=1,
        angles_deg=[0, 45, 90],
        unpolarized_input=True
    )

    assert np.isclose(result, 0.125)


def test_polarized_input_does_not_get_halved_first():
    result = pass_intensity(
        initial_intensity=10,
        angles_deg=[0, 45],
        unpolarized_input=False
    )

    assert np.isclose(result, 5.0)


def test_negative_initial_intensity_raises_error():
    with pytest.raises(ValueError):
        pass_intensity(
            initial_intensity=-1,
            angles_deg=[0, 45],
            unpolarized_input=True
        )


def test_qiskit_pair_probability_matches_malus_law():
    qiskit_result = qiskit_check.qiskit_pair_pass_probability(0, 45)

    expected = np.cos(np.deg2rad(45)) ** 2

    assert np.isclose(qiskit_result, expected)


def test_numpy_and_qiskit_results_match():
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

        qiskit_result = qiskit_check.qiskit_pass_intensity(
            initial_intensity,
            angles_deg,
            unpolarized_input
        )

        assert np.isclose(numpy_result, qiskit_result)