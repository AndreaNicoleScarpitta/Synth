# utils/logger.py

import os
from datetime import datetime

# Folder to store log files
LOG_DIR = "logs"

# Ensure the logs folder exists
os.makedirs(LOG_DIR, exist_ok=True)

def _get_log_file_path(agent_name: str) -> str:
    """
    Returns the path for a daily log file for the given agent.
    """
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"{agent_name}_{date_str}.log"
    return os.path.join(LOG_DIR, filename)

def log_chain_of_thought(agent_name: str, log_text: str):
    """
    Appends a clear, timestamped entry to the agent's log file.
    This includes both happy path and error messages.
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    log_file = _get_log_file_path(agent_name)

    formatted_log = f"""\
=======================================
🧠 Agent: {agent_name}
🕒 Time: {timestamp}
📜 Log:
{log_text.strip()}
=======================================

"""

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(formatted_log)
    except Exception as e:
        print(f"⚠️ Failed to write log for {agent_name}: {e}")
