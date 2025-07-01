import networkx as nx

# Build a dependency graph for Phase 2
DAG = nx.DiGraph()

# Example edges (fill in real dependencies)
# DAG.add_edge("PhenotypeAssemblerAgent", "ClinicalJourneyBuilderAgent")
# DAG.add_edge("PhenotypeAssemblerAgent", "DemographicStratifierAgent")
# ...

def topo_sorted_agents():
    """Return agent class names in dependency order."""
    return list(nx.topological_sort(DAG))
