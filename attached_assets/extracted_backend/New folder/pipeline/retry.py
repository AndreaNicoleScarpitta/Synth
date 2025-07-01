import time
import random
from .errors import TransientError, FatalError

def with_retry(func, max_retries, initial_backoff, backoff_factor, logger, *args, **kwargs):
    """Retry only on TransientError, with exponential backoff + jitter."""
    delay = initial_backoff
    for attempt in range(1, max_retries + 1):
        try:
            return func(*args, **kwargs)
        except FatalError:
            # do not retry fatal errors
            raise
        except TransientError as e:
            jitter = random.uniform(-0.1 * delay, 0.1 * delay)
            sleep_time = max(0, delay + jitter)
            logger.warning(f"{func.__name__} transient failure (attempt {attempt}): {e}; retrying in {sleep_time:.1f}s")
            if attempt == max_retries:
                logger.error(f"{func.__name__} reached max retries")
                raise
            time.sleep(sleep_time)
            delay *= backoff_factor
