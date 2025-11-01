import logging
import numpy as np
from scipy import stats
from typing import List, Dict, Any

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StatisticalValidator:
    """
    Performs statistical tests to compare ecosystem performance against a baseline.
    """
    def __init__(self, significance_level: float = 0.05):
        """
        Initializes the StatisticalValidator.

        Args:
            significance_level (float): The p-value threshold for statistical significance.
        """
        self.significance_level = significance_level
        logging.info(f"StatisticalValidator initialized with significance level: {self.significance_level}")

    def compare_with_baseline(self, ecosystem_results: List[float], baseline_results: List[float]) -> Dict[str, Any]:
        """
        Compares ecosystem performance with baseline results using a t-test.

        Args:
            ecosystem_results (List[float]): A list of numerical performance scores from the ecosystem.
            baseline_results (List[float]): A list of numerical performance scores from the baseline.

        Returns:
            A dictionary containing the statistical test results.
        """
        if not ecosystem_results or not baseline_results:
            logging.warning("Cannot perform comparison with empty result lists.")
            return {"error": "Input result lists cannot be empty."}

        # Ensure data is in a numpy array format
        eco_array = np.array(ecosystem_results)
        base_array = np.array(baseline_results)

        # Perform an independent two-sample t-test
        t_statistic, p_value = stats.ttest_ind(eco_array, base_array, equal_var=False) # Welch's t-test

        is_significant = p_value < self.significance_level
        
        result = {
            "t_statistic": t_statistic,
            "p_value": p_value,
            "is_significant": is_significant,
            "ecosystem_mean": np.mean(eco_array),
            "baseline_mean": np.mean(base_array),
            "conclusion": ""
        }

        if is_significant:
            if result["ecosystem_mean"] > result["baseline_mean"]:
                result["conclusion"] = "The ecosystem performs significantly better than the baseline."
            else:
                result["conclusion"] = "The ecosystem performs significantly worse than the baseline."
        else:
            result["conclusion"] = "There is no significant performance difference between the ecosystem and the baseline."
        
        logging.info(f"Comparison result: {result['conclusion']}")
        return result

    def calculate_effect_size(self, treatment_group: List[float], control_group: List[float]) -> float:
        """
        Calculates Cohen's d as a measure of effect size.

        Args:
            treatment_group (List[float]): The results from the experimental/ecosystem group.
            control_group (List[float]): The results from the control/baseline group.

        Returns:
            The calculated Cohen's d value.
        """
        if not treatment_group or not control_group:
            return 0.0

        mean_treat, mean_control = np.mean(treatment_group), np.mean(control_group)
        std_treat, std_control = np.std(treatment_group, ddof=1), np.std(control_group, ddof=1)
        
        # Calculate pooled standard deviation
        n1, n2 = len(treatment_group), len(control_group)
        pooled_std = np.sqrt(((n1 - 1) * std_treat ** 2 + (n2 - 1) * std_control ** 2) / (n1 + n2 - 2))
        
        if pooled_std == 0:
            return 0.0
            
        cohens_d = (mean_treat - mean_control) / pooled_std
        return cohens_d

    def generate_statistical_report(self, comparison_results: Dict[str, Any], effect_size: float) -> str:
        """
        Generates a human-readable summary of the statistical analysis.

        Args:
            comparison_results (Dict[str, Any]): The dictionary returned by compare_with_baseline.
            effect_size (float): The calculated effect size (e.g., Cohen's d).

        Returns:
            A formatted string containing the statistical report.
        """
        report = f"Statistical Analysis Report\n"
        report += f"===========================\n"
        report += f"Ecosystem Mean Performance: {comparison_results['ecosystem_mean']:.4f}\n"
        report += f"Baseline Mean Performance:  {comparison_results['baseline_mean']:.4f}\n\n"
        report += f"T-statistic: {comparison_results['t_statistic']:.4f}\n"
        report += f"P-value: {comparison_results['p_value']:.4f}\n"
        report += f"Significance Level: {self.significance_level}\n\n"
        report += f"Effect Size (Cohen's d): {effect_size:.4f}\n"
        report += f"Conclusion: {comparison_results['conclusion']}\n"
        
        return report
