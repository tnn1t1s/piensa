#!/usr/bin/env python3
"""
Analyze seed variance experiment results.

Reads all seed result files and performs distribution analysis:
- Shapiro-Wilk test for normality
- Hartigan's dip test for unimodality
- Gaussian mixture model fitting (if bimodal)
- Summary statistics (mean, variance, skewness, kurtosis)

Usage:
    python analyze.py --results-dir results/mini/
    python analyze.py --results-dir results/mini/ --plot histogram.png

Output: Statistics to stdout, optional histogram PNG
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats


def log(msg: str):
    """Log to stderr with flush."""
    print(msg, file=sys.stderr, flush=True)


def load_leakage_rates(results_dir: Path) -> list[tuple[int, float]]:
    """Load leakage rates from all seed result files."""
    rates = []
    for f in sorted(results_dir.glob("seed_*.json")):
        with open(f) as fp:
            data = json.load(fp)
        seed = data["seed"]
        rate = data["leakage_rate"]
        rates.append((seed, rate))
    return rates


def hartigans_dip_test(data: np.ndarray) -> tuple[float, float]:
    """
    Compute Hartigan's dip statistic for unimodality test.

    Returns (dip_statistic, p_value).
    Uses bootstrap to estimate p-value.

    The dip statistic measures the maximum difference between the empirical
    distribution and the best-fitting unimodal distribution.

    Implementation based on diptest algorithm.
    """
    try:
        from diptest import diptest as dip
        dip_stat, p_value = dip(data)
        return dip_stat, p_value
    except ImportError:
        # Fallback: simple bootstrap approach
        n = len(data)
        sorted_data = np.sort(data)

        # Compute empirical CDF
        ecdf = np.arange(1, n + 1) / n

        # For uniform distribution (most unimodal), compute max deviation
        uniform_cdf = (sorted_data - sorted_data.min()) / (sorted_data.max() - sorted_data.min() + 1e-10)
        dip_stat = np.max(np.abs(ecdf - uniform_cdf)) / 2

        # Bootstrap p-value under uniform null
        n_bootstrap = 1000
        null_dips = []
        for _ in range(n_bootstrap):
            uniform_sample = np.sort(np.random.uniform(0, 1, n))
            u_ecdf = np.arange(1, n + 1) / n
            null_dip = np.max(np.abs(u_ecdf - uniform_sample)) / 2
            null_dips.append(null_dip)

        p_value = np.mean(np.array(null_dips) >= dip_stat)
        return dip_stat, p_value


def fit_gaussian_mixture(data: np.ndarray, n_components: int = 2) -> dict:
    """
    Fit a Gaussian Mixture Model.

    Returns dict with means, stds, weights, and BIC.
    """
    try:
        from sklearn.mixture import GaussianMixture

        X = data.reshape(-1, 1)
        gmm = GaussianMixture(n_components=n_components, random_state=42)
        gmm.fit(X)

        return {
            "n_components": n_components,
            "means": gmm.means_.flatten().tolist(),
            "stds": np.sqrt(gmm.covariances_.flatten()).tolist(),
            "weights": gmm.weights_.tolist(),
            "bic": gmm.bic(X),
            "aic": gmm.aic(X),
        }
    except ImportError:
        return {"error": "sklearn not available"}


def compute_statistics(rates: list[float]) -> dict:
    """Compute summary statistics for leakage rates."""
    data = np.array(rates)

    return {
        "n": len(data),
        "mean": float(np.mean(data)),
        "std": float(np.std(data, ddof=1)),
        "variance": float(np.var(data, ddof=1)),
        "min": float(np.min(data)),
        "max": float(np.max(data)),
        "median": float(np.median(data)),
        "q25": float(np.percentile(data, 25)),
        "q75": float(np.percentile(data, 75)),
        "skewness": float(stats.skew(data)),
        "kurtosis": float(stats.kurtosis(data)),
        "range": float(np.max(data) - np.min(data)),
    }


def run_tests(data: np.ndarray) -> dict:
    """Run statistical tests on the distribution."""
    results = {}

    # Shapiro-Wilk test for normality
    if len(data) >= 3:
        stat, p = stats.shapiro(data)
        results["shapiro_wilk"] = {
            "statistic": float(stat),
            "p_value": float(p),
            "is_normal": p > 0.05,
        }

    # Hartigan's dip test for unimodality
    dip_stat, dip_p = hartigans_dip_test(data)
    results["hartigans_dip"] = {
        "statistic": float(dip_stat),
        "p_value": float(dip_p),
        "is_unimodal": dip_p > 0.05,
    }

    # Kolmogorov-Smirnov test against uniform
    ks_stat, ks_p = stats.kstest(data, 'uniform', args=(data.min(), data.max() - data.min()))
    results["ks_uniform"] = {
        "statistic": float(ks_stat),
        "p_value": float(ks_p),
    }

    return results


def plot_histogram(data: np.ndarray, output_path: Path, title: str = "Temporal Tilt Distribution"):
    """Generate histogram with KDE overlay."""
    try:
        import matplotlib.pyplot as plt
        from matplotlib import rcParams

        # Set high-quality defaults
        rcParams['font.size'] = 12
        rcParams['axes.labelsize'] = 14
        rcParams['axes.titlesize'] = 16

        fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

        # Histogram
        n_bins = min(20, max(10, len(data) // 5))
        counts, bins, patches = ax.hist(
            data * 100,  # Convert to percentage
            bins=n_bins,
            density=True,
            alpha=0.7,
            color='steelblue',
            edgecolor='white',
            linewidth=0.5,
        )

        # KDE overlay
        if len(data) > 5:
            kde = stats.gaussian_kde(data * 100)
            x_range = np.linspace(0, 100, 200)
            ax.plot(x_range, kde(x_range), 'r-', linewidth=2, label='KDE')

        # Add vertical lines for mean and median
        mean_pct = np.mean(data) * 100
        median_pct = np.median(data) * 100
        ax.axvline(mean_pct, color='darkred', linestyle='--', linewidth=1.5, label=f'Mean: {mean_pct:.1f}%')
        ax.axvline(median_pct, color='darkgreen', linestyle=':', linewidth=1.5, label=f'Median: {median_pct:.1f}%')

        ax.set_xlabel('Temporal Tilt Rate (%)')
        ax.set_ylabel('Density')
        ax.set_title(title)
        ax.legend(loc='upper right')
        ax.set_xlim(0, 100)

        # Add statistics text box
        stats_text = f"n={len(data)}\nMean={mean_pct:.1f}%\nStd={np.std(data)*100:.1f}%"
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
                verticalalignment='top', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        log(f"[analyze] saved histogram to {output_path}")

    except ImportError:
        log("[analyze] WARNING: matplotlib not available, skipping histogram")


def main():
    parser = argparse.ArgumentParser(description="Analyze seed variance experiment results")
    parser.add_argument("--results-dir", "-r", required=True, help="Directory with seed_*.json files")
    parser.add_argument("--plot", "-p", help="Output histogram PNG path")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON instead of formatted text")
    parser.add_argument("--compare", "-c", help="Second results directory for comparison")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    if not results_dir.exists():
        log(f"[analyze] ERROR: Results directory not found: {args.results_dir}")
        sys.exit(1)

    # Load data
    seed_rates = load_leakage_rates(results_dir)
    if not seed_rates:
        log(f"[analyze] ERROR: No seed result files found in {args.results_dir}")
        sys.exit(1)

    rates = [r for _, r in seed_rates]
    data = np.array(rates)

    log(f"[analyze] loaded {len(data)} seeds from {args.results_dir}")

    # Compute statistics
    summary = compute_statistics(rates)
    tests = run_tests(data)

    # Fit mixture models
    gmm_2 = fit_gaussian_mixture(data, 2)
    gmm_1 = fit_gaussian_mixture(data, 1)

    # Determine if bimodal based on BIC
    if "error" not in gmm_1 and "error" not in gmm_2:
        bimodal_preferred = gmm_2["bic"] < gmm_1["bic"]
    else:
        bimodal_preferred = None

    output = {
        "source": str(results_dir),
        "n_seeds": len(data),
        "summary": summary,
        "tests": tests,
        "mixture_1": gmm_1,
        "mixture_2": gmm_2,
        "bimodal_preferred": bimodal_preferred,
    }

    # Add comparison if requested
    if args.compare:
        compare_dir = Path(args.compare)
        compare_rates = load_leakage_rates(compare_dir)
        if compare_rates:
            compare_data = np.array([r for _, r in compare_rates])
            output["comparison"] = {
                "source": str(compare_dir),
                "n_seeds": len(compare_data),
                "summary": compute_statistics([r for _, r in compare_rates]),
                "tests": run_tests(compare_data),
            }

            # Mann-Whitney U test for difference between distributions
            u_stat, u_p = stats.mannwhitneyu(data, compare_data, alternative='two-sided')
            output["comparison"]["mann_whitney_u"] = {
                "statistic": float(u_stat),
                "p_value": float(u_p),
            }

    # Output
    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print("\n" + "="*60)
        print("SEED VARIANCE ANALYSIS")
        print("="*60)
        print(f"\nSource: {results_dir}")
        print(f"Seeds analyzed: {len(data)}")

        print("\n--- SUMMARY STATISTICS ---")
        print(f"Mean:     {summary['mean']*100:.1f}%")
        print(f"Std:      {summary['std']*100:.1f}%")
        print(f"Variance: {summary['variance']*10000:.1f}%^2")
        print(f"Range:    [{summary['min']*100:.1f}%, {summary['max']*100:.1f}%]")
        print(f"IQR:      [{summary['q25']*100:.1f}%, {summary['q75']*100:.1f}%]")
        print(f"Skewness: {summary['skewness']:.2f}")
        print(f"Kurtosis: {summary['kurtosis']:.2f}")

        print("\n--- DISTRIBUTION TESTS ---")
        sw = tests["shapiro_wilk"]
        print(f"Shapiro-Wilk (normality): W={sw['statistic']:.4f}, p={sw['p_value']:.4f}")
        print(f"  -> {'Normal' if sw['is_normal'] else 'Non-normal'} distribution")

        hd = tests["hartigans_dip"]
        print(f"Hartigan's Dip (unimodality): D={hd['statistic']:.4f}, p={hd['p_value']:.4f}")
        print(f"  -> {'Unimodal' if hd['is_unimodal'] else 'Multimodal'} distribution")

        print("\n--- MIXTURE MODEL FIT ---")
        if bimodal_preferred is not None:
            print(f"1-component BIC: {gmm_1['bic']:.1f}")
            print(f"2-component BIC: {gmm_2['bic']:.1f}")
            print(f"  -> {'Bimodal' if bimodal_preferred else 'Unimodal'} preferred by BIC")

            if bimodal_preferred:
                print(f"\n2-Gaussian mixture:")
                for i in range(2):
                    print(f"  Component {i+1}: mean={gmm_2['means'][i]*100:.1f}%, "
                          f"std={gmm_2['stds'][i]*100:.1f}%, weight={gmm_2['weights'][i]:.2f}")

        if args.compare and "comparison" in output:
            comp = output["comparison"]
            print("\n--- COMPARISON ---")
            print(f"Comparison source: {comp['source']}")
            print(f"Comparison seeds: {comp['n_seeds']}")
            print(f"Comparison mean: {comp['summary']['mean']*100:.1f}%")
            print(f"Comparison std: {comp['summary']['std']*100:.1f}%")
            mw = comp["mann_whitney_u"]
            print(f"Mann-Whitney U: U={mw['statistic']:.1f}, p={mw['p_value']:.4f}")
            if mw['p_value'] < 0.05:
                print("  -> Distributions are significantly different")
            else:
                print("  -> No significant difference between distributions")

        print("\n" + "="*60)

    # Generate plot
    if args.plot:
        title = f"Temporal Tilt Distribution (n={len(data)})"
        plot_histogram(data, Path(args.plot), title)


if __name__ == "__main__":
    main()
