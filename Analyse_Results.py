import numpy as np
import pandas as pd


def analyse_results(simulated_results, analysis_type: str = "auto") -> dict:
    """Analyse simulation results into expectation and distributions.

    Args:
        simulated_results: 1D array-like of per-episode outputs from the simulator.
            For non-unit attacks this should be damage values; for infantry attacks
            this should be casualty counts.
        analysis_type: "damage", "casualties", or "auto".

    Returns:
        Dictionary with expectation plus both probability and cumulative
        distributions, formatted as lists for direct plotting.
    """
    series = pd.Series(np.asarray(simulated_results).reshape(-1), dtype="float64")
    if series.empty:
        raise ValueError("simulated_results must contain at least one value")

    if analysis_type not in {"damage", "casualties", "auto"}:
        raise ValueError("analysis_type must be 'damage', 'casualties', or 'auto'")

    if analysis_type == "auto":
        is_integer = np.allclose(series.values, np.round(series.values))
        analysis_type = "casualties" if is_integer and np.all(series.values >= 0) else "damage"

    distribution = series.value_counts(normalize=True).sort_index()
    cumulative_distribution = distribution.cumsum()

    return {
        "metric": analysis_type,
        "expectation": float(series.mean()),
        "probability_distribution": {
            "values": distribution.index.to_list(),
            "probabilities": distribution.values.tolist(),
        },
        "cumulative_distribution": {
            "values": cumulative_distribution.index.to_list(),
            "cumulative_probabilities": cumulative_distribution.values.tolist(),
        },
    }


def analyze_results(simulated_results, analysis_type: str = "auto") -> dict:
    """US-English alias for analyse_results."""
    return analyse_results(simulated_results=simulated_results, analysis_type=analysis_type)

