from agents.reporting.base_agent import BaseReportingAgent
from typing import Dict, Any, List

class ProcessLineageGraph(BaseReportingAgent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts a lineage graph representing the flow of data through agents/processes.
        Assumes each agent's output is stored under a top-level key matching its name.
        Creates an edge for each step in the pipeline.
        """
        lineage: List[Dict[str, str]] = []

        # Sort agent keys (optional: use agent execution order if available)
        agent_keys = [k for k in input_data.keys() if not k.startswith("_")]

        for i in range(1, len(agent_keys)):
            lineage.append({
                "from": agent_keys[i - 1],
                "to": agent_keys[i]
            })

        output = {
            "lineage_graph": lineage,
            "node_count": len(agent_keys),
            "edge_count": len(lineage),
            "nodes": agent_keys
        }
        log = f"ProcessLineageGraph: {len(lineage)} edges across {len(agent_keys)} nodes."

        return self.standard_response(
            output=output,
            log=log
        )
