#!/usr/bin/env python3
"""Behavioral simulation for the One-Wave V0-A cell.

This is a control-level model, not a transistor-level or magnetic SPICE proof.
It compares free decay, continuous drive, repeated restart, and phase-timed refresh.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

F0 = 10000.0
Q = 22.0
# The generated package already contains results and plots.
# Edit this file to extend the controller model.
