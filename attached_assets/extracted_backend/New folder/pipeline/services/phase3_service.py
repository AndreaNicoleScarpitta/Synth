from ..qa_service import StatisticalValidator

def run_phase3(agents, data, thresholds, logger):
    raw = {a.__class__.__name__: a.run(data) for a in agents}
    validator = StatisticalValidator(thresholds)
    qa_metrics = validator.validate(raw)
    return raw, qa_metrics
