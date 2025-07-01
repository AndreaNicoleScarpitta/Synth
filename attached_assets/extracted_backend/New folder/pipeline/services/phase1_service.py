from concurrent.futures import ThreadPoolExecutor, as_completed
from ..retry import with_retry
from ..errors import TransientError

def run_phase1(agents, config, metrics, logger, fallback, retry_params):
    results = {}
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(
                with_retry,
                agent.run,
                retry_params["max_retries"],
                retry_params["initial_backoff"],
                retry_params["backoff_factor"],
                logger,
                config
            ): agent
            for agent in agents
        }
        for future in as_completed(futures):
            agent = futures[future]
            name = agent.__class__.__name__
            try:
                out = future.result()
            except TransientError as e:
                logger.warning(f"{name} failed; applying fallback")
                out = fallback.handle(name, e)
            except Exception as e:
                logger.error(f"{name} fatal error: {e}")
                raise
            results[name] = out
    return results
