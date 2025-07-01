from ..exporter import JSONLinesExporter

def run_phase4(agents, all_outputs, exporter: JSONLinesExporter, logger):
    audit = agents[0].run(all_outputs)
    report = agents[1].run(all_outputs)
    summary = agents[2].run(all_outputs)
    exporter.write([audit, report, summary])
    return {"audit": audit, "report": report, "summary": summary}
