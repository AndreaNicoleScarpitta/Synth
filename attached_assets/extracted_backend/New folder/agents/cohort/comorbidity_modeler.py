from typing import Dict, Any
import logging
import random
import networkx as nx
from langchain_core.runnables import Runnable

class ComorbidityGraphGenerator(Runnable):
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            "condition_graph": {
                "CKD": ["Hypertension", "Diabetes"],
                "Diabetes": ["CKD", "Neuropathy"],
                "Hypertension": ["CKD", "CAD"],
                "COPD": ["Asthma", "SmokingHistory"],
                "CAD": ["Hyperlipidemia", "Hypertension"]
            },
            "max_total_conditions": 4,
            "add_probability": 0.7  # probability to add a connected node
        }

    def invoke(self, input_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        logging.info("[ComorbidityGraphGenerator] Generating comorbidity graph...")

        base_conditions = input_data.get("phenotypes", [])
        G = nx.Graph()

        # Start with primary conditions
        for cond in base_conditions:
            G.add_node(cond)
            neighbors = self.config["condition_graph"].get(cond, [])
            for neighbor in neighbors:
                if random.random() < self.config["add_probability"]:
                    G.add_edge(cond, neighbor)

        # Prune if too many nodes
        while len(G.nodes) > self.config["max_total_conditions"]:
            node_to_remove = random.choice(list(G.nodes))
            if node_to_remove not in base_conditions:
                G.remove_node(node_to_remove)

        extended_conditions = list(G.nodes)
        input_data["comorbidity_graph"] = G
        input_data["conditions"] = extended_conditions  # used by downstream agents

        return {
            "output": input_data,
            "log": f"Comorbidities added: {set(extended_conditions) - set(base_conditions)}"
        }
