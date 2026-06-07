# Rieffel 2.1-A Polarization Experiment

## Goal

This section implements the classical polarization experiment using NumPy and validates the result with Qiskit.

## Core Ideas

- Polarization angle
- Malus' Law
- cos² intensity rule
- single-qubit abstraction
- RY gate validation
- measurement probability
- NumPy/Qiskit consistency check

## Files

| File | Meaning |
|---|---|
| numpy_impl.py | NumPy implementation of polarization intensity |
| qiskit_check.py | Qiskit validation using a single-qubit circuit |
| test_polarization.py | pytest unit tests |

## Test Result

Run:

`python -m pytest sections/02_01_A_polarization/test_polarization.py`

Expected result:

`8 passed`

## Learning Summary

In this section, I implemented the polarization intensity rule from scratch with NumPy and validated the result using Qiskit. This connects the classical polarization experiment with a single-qubit measurement model.