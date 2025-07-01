from ..scheduler import topo_sorted_agents
from ..retry import with_retry

def run_phase2(agent_map, initial_data, metrics, logger, retry_params):
    data = dict(initial_data)
    for agent_name in topo_sorted_agents():
        agent = agent_map[agent_name]
        result = with_retry(
            agent.run,
            retry_params["max_retries"],
            retry_params["initial_backoff"],
            retry_params["backoff_factor"],
            logger,
            data
        )
        data[agent_name] = result
    return data
