# utils/stats.py

import numpy as np
from scipy.stats import norm, bernoulli, poisson, ks_2samp
import random
import math

# ------------------------------
# 🧪 SAMPLING HELPERS
# ------------------------------

def sample_gaussian(mean: float, stddev: float) -> float:
    """Returns a float sampled from a normal distribution."""
    return round(norm.rvs(loc=mean, scale=stddev), 2)

def sample_binary(p_true: float = 0.5) -> bool:
    """Returns True with probability p_true."""
    return bool(bernoulli.rvs(p=p_true))

def sample_poisson(rate: float) -> int:
    """Samples count data (e.g. hospitalizations)."""
    return poisson.rvs(mu=rate)

def sample_from_distribution(values: list, probs: list) -> any:
    """Samples from a categorical distribution."""
    return np.random.choice(values, p=probs)

# ------------------------------
# 📊 STATISTICAL TESTS
# ------------------------------

def compare_distributions(real: list, synthetic: list) -> dict:
    """
    Performs a Kolmogorov–Smirnov test between real and synthetic samples.
    """
    stat, p = ks_2samp(real, synthetic)
    return {
        "ks_statistic": round(stat, 4),
        "p_value": round(p, 4),
        "similar": p > 0.05
    }

# ------------------------------
# ⚖️ BIAS & FAIRNESS
# ------------------------------

def standardized_mean_difference(real_mean, synthetic_mean, pooled_std):
    """
    Returns SMD between two group means.
    """
    if pooled_std == 0:
        return 0
    return round((real_mean - synthetic_mean) / pooled_std, 4)

# ------------------------------
# ⏱️ TIME UTILITIES
# ------------------------------

def sample_event_timeline(start_day=0, intervals=[7, 30, 90]) -> list:
    """
    Simulates a timeline of patient events over a few months.
    E.g., [0, 7, 37, 127]
    """
    timeline = [start_day]
    for interval in intervals:
        timeline.append(timeline[-1] + interval)
    return timeline
