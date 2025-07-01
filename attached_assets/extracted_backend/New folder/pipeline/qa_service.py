from statsmodels.stats.multitest import multipletests

class StatisticalValidator:
    def __init__(self, thresholds: dict):
        self.thresholds = thresholds

    def validate(self, raw_metrics: dict) -> dict:
        """
        raw_metrics: {
          "RealismAssessorAgent": {"score": 0.75, "pval": 0.02, ...},
          "PrivacyRiskEvaluatorAgent": {"risk": 0.15, "pval": 0.05, ...},
          ...
        }
        Returns adjusted p-values and pass/fail flags.
        """
        pvals = [m.get("pval", 1.0) for m in raw_metrics.values()]
        rejected, adj_pvals, _, _ = multipletests(pvals, method="holm")
        return {
            "rejected": dict(zip(raw_metrics.keys(), rejected)),
            "adj_pvals": dict(zip(raw_metrics.keys(), adj_pvals))
        }
