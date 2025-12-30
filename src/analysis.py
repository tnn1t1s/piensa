"""
Analysis utilities for computing effect sizes and statistical tests.

Computes key metrics from evaluation results:
- Framing effect sizes
- Risk aversion indices
- CRT accuracy
- Cross-language effect comparisons
"""

import json
from pathlib import Path
from collections import defaultdict
from typing import Optional

import pandas as pd
import numpy as np
from scipy import stats


def load_results(results_path: Path) -> pd.DataFrame:
    """Load results JSON into a DataFrame."""
    with open(results_path, "r") as f:
        data = json.load(f)
    return pd.DataFrame(data)


def compute_framing_effect(df: pd.DataFrame, scenario: str = "asian_disease") -> pd.DataFrame:
    """
    Compute framing effect for a given scenario.

    Framing effect = P(risky choice | loss frame) - P(risky choice | gain frame)

    Args:
        df: Results DataFrame
        scenario: Scenario name (default: asian_disease)

    Returns:
        DataFrame with framing effects by adapter × prompt_language
    """
    scenario_df = df[df["scenario"] == scenario].copy()

    # Map responses to risky choice (B in Asian Disease)
    scenario_df["chose_risky"] = scenario_df["extracted_answer"].str.upper() == "B"

    # Group by adapter, prompt_language, and variant (gain/loss)
    grouped = scenario_df.groupby(
        ["adapter", "prompt_language", "variant"]
    )["chose_risky"].mean().unstack("variant")

    # Compute framing effect
    if "loss_frame" in grouped.columns and "gain_frame" in grouped.columns:
        grouped["framing_effect"] = grouped["loss_frame"] - grouped["gain_frame"]
    else:
        grouped["framing_effect"] = np.nan

    return grouped.reset_index()


def compute_crt_accuracy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute CRT accuracy and intuitive response rate.

    Args:
        df: Results DataFrame

    Returns:
        DataFrame with CRT metrics by adapter × prompt_language
    """
    crt_df = df[df["scenario"] == "cognitive_reflection_test"].copy()

    # Compute accuracy
    crt_df["is_correct"] = crt_df["extracted_answer"] == crt_df["correct_answer"]
    crt_df["is_intuitive_wrong"] = crt_df["extracted_answer"] == crt_df["intuitive_wrong_answer"]

    # Group by adapter and prompt_language
    grouped = crt_df.groupby(["adapter", "prompt_language"]).agg({
        "is_correct": "mean",
        "is_intuitive_wrong": "mean",
    }).rename(columns={
        "is_correct": "accuracy",
        "is_intuitive_wrong": "intuitive_rate",
    })

    return grouped.reset_index()


def compute_allais_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Allais paradox metrics.

    Args:
        df: Results DataFrame

    Returns:
        DataFrame with Allais metrics by adapter × prompt_language
    """
    allais_df = df[df["scenario"] == "allais_paradox"].copy()

    results = []
    for (adapter, lang), group in allais_df.groupby(["adapter", "prompt_language"]):
        q1 = group[group["question"] == "question_1"]
        q2 = group[group["question"] == "question_2"]

        if len(q1) > 0 and len(q2) > 0:
            # Risk aversion in Q1: choosing A (sure thing)
            risk_averse_rate = (q1["extracted_answer"].str.upper() == "A").mean()

            # Get paired responses for consistency
            q1_responses = q1["extracted_answer"].str.upper().values
            q2_responses = q2["extracted_answer"].str.upper().values

            if len(q1_responses) == len(q2_responses):
                # Consistent: A,C or B,D
                consistent = np.sum(
                    ((q1_responses == "A") & (q2_responses == "C")) |
                    ((q1_responses == "B") & (q2_responses == "D"))
                ) / len(q1_responses)

                # Allais violation: A,D pattern
                allais_violation = np.sum(
                    (q1_responses == "A") & (q2_responses == "D")
                ) / len(q1_responses)
            else:
                consistent = np.nan
                allais_violation = np.nan

            results.append({
                "adapter": adapter,
                "prompt_language": lang,
                "risk_averse_rate": risk_averse_rate,
                "consistency": consistent,
                "allais_violation": allais_violation,
            })

    return pd.DataFrame(results)


def compute_cross_language_effect(
    df: pd.DataFrame,
    metric_fn,
    metric_name: str = "effect"
) -> pd.DataFrame:
    """
    Compute the cross-language effect (L1 vs L2 conditions).

    For each adapter, compare matched (L1) vs mismatched (L2) conditions.

    Args:
        df: Results DataFrame
        metric_fn: Function to compute the metric
        metric_name: Name of the metric column

    Returns:
        DataFrame with L1/L2 comparison
    """
    metrics = metric_fn(df)

    results = []
    for adapter in metrics["adapter"].unique():
        adapter_data = metrics[metrics["adapter"] == adapter]

        # Determine L1 language from adapter name
        l1_lang = adapter.replace("lora_", "")

        l1_value = adapter_data[
            adapter_data["prompt_language"] == l1_lang
        ][metric_name].values

        l2_values = adapter_data[
            adapter_data["prompt_language"] != l1_lang
        ][metric_name].values

        if len(l1_value) > 0 and len(l2_values) > 0:
            results.append({
                "adapter": adapter,
                "l1_language": l1_lang,
                f"l1_{metric_name}": l1_value[0],
                f"l2_{metric_name}_mean": np.mean(l2_values),
                f"l1_l2_diff": l1_value[0] - np.mean(l2_values),
            })

    return pd.DataFrame(results)


def run_statistical_tests(
    df: pd.DataFrame,
    group1_filter: dict,
    group2_filter: dict,
    value_column: str,
) -> dict:
    """
    Run statistical tests comparing two groups.

    Args:
        df: Results DataFrame
        group1_filter: Dict of column:value filters for group 1
        group2_filter: Dict of column:value filters for group 2
        value_column: Column containing values to compare

    Returns:
        Dict with test statistics
    """
    # Filter groups
    g1_mask = pd.Series([True] * len(df))
    for col, val in group1_filter.items():
        g1_mask &= (df[col] == val)

    g2_mask = pd.Series([True] * len(df))
    for col, val in group2_filter.items():
        g2_mask &= (df[col] == val)

    g1_values = df.loc[g1_mask, value_column].dropna()
    g2_values = df.loc[g2_mask, value_column].dropna()

    if len(g1_values) == 0 or len(g2_values) == 0:
        return {"error": "Insufficient data"}

    # t-test
    t_stat, t_pval = stats.ttest_ind(g1_values, g2_values)

    # Mann-Whitney U
    u_stat, u_pval = stats.mannwhitneyu(g1_values, g2_values, alternative="two-sided")

    # Effect size (Cohen's d)
    pooled_std = np.sqrt(
        (g1_values.std()**2 + g2_values.std()**2) / 2
    )
    cohens_d = (g1_values.mean() - g2_values.mean()) / pooled_std if pooled_std > 0 else np.nan

    return {
        "group1_n": len(g1_values),
        "group2_n": len(g2_values),
        "group1_mean": g1_values.mean(),
        "group2_mean": g2_values.mean(),
        "t_statistic": t_stat,
        "t_pvalue": t_pval,
        "u_statistic": u_stat,
        "u_pvalue": u_pval,
        "cohens_d": cohens_d,
    }


def generate_summary_report(results_path: Path, output_path: Optional[Path] = None) -> str:
    """
    Generate a summary report of all analyses.

    Args:
        results_path: Path to full_results.json
        output_path: Optional path to save report

    Returns:
        Report as string
    """
    df = load_results(results_path)

    report = []
    report.append("=" * 60)
    report.append("PIENSA TWICE: EVALUATION SUMMARY")
    report.append("=" * 60)
    report.append(f"\nTotal evaluations: {len(df)}")
    report.append(f"Adapters: {df['adapter'].unique().tolist()}")
    report.append(f"Languages: {df['prompt_language'].unique().tolist()}")
    report.append(f"Scenarios: {df['scenario'].unique().tolist()}")

    # Framing effects
    report.append("\n" + "-" * 40)
    report.append("FRAMING EFFECTS (Asian Disease)")
    report.append("-" * 40)
    framing = compute_framing_effect(df)
    report.append(framing.to_string(index=False))

    # CRT
    report.append("\n" + "-" * 40)
    report.append("COGNITIVE REFLECTION TEST")
    report.append("-" * 40)
    crt = compute_crt_accuracy(df)
    report.append(crt.to_string(index=False))

    # Allais
    report.append("\n" + "-" * 40)
    report.append("ALLAIS PARADOX")
    report.append("-" * 40)
    allais = compute_allais_metrics(df)
    if len(allais) > 0:
        report.append(allais.to_string(index=False))
    else:
        report.append("No Allais data available")

    # Cross-language effects
    report.append("\n" + "-" * 40)
    report.append("CROSS-LANGUAGE EFFECTS")
    report.append("-" * 40)

    def get_framing_effect_col(df):
        fe = compute_framing_effect(df)
        if "framing_effect" in fe.columns:
            return fe[["adapter", "prompt_language", "framing_effect"]].rename(
                columns={"framing_effect": "effect"}
            )
        return pd.DataFrame()

    cross_lang = compute_cross_language_effect(df, get_framing_effect_col, "effect")
    if len(cross_lang) > 0:
        report.append(cross_lang.to_string(index=False))
    else:
        report.append("Insufficient data for cross-language analysis")

    report_str = "\n".join(report)

    if output_path:
        with open(output_path, "w") as f:
            f.write(report_str)

    return report_str


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Analyze evaluation results")
    parser.add_argument(
        "--results",
        type=Path,
        default=Path("results/full_results.json"),
        help="Path to results JSON",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output path for report",
    )
    args = parser.parse_args()

    report = generate_summary_report(args.results, args.output)
    print(report)


if __name__ == "__main__":
    main()
