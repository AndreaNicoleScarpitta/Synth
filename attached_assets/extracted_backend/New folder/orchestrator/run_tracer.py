import sys
import os
import uuid
import json
import subprocess
from datetime import datetime
from pathlib import Path
import yaml

def create_run_folder(run_id):
    output_dir = Path(f"outputs/run_{run_id}")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def run_agent(agent_name, input_data, output_dir, step_num):
    agent_path = Path(f"agents/{agent_name}")
    agent_config_path = agent_path / "agent.yaml"

    with open(agent_config_path) as f:
        agent_config = yaml.safe_load(f)

    input_path = output_dir / f"{step_num:02d}_{agent_name}_input.json"
    output_path = output_dir / f"{step_num:02d}_{agent_name}_output.json"

    # Save input for this step
    with open(input_path, "w") as f:
        json.dump(input_data, f, indent=2)

    print(f"⚙️ Running agent: {agent_name} (v{agent_config['version']})")

    subprocess.run([
        "python", str(agent_path / agent_config["entrypoint"]),
        str(input_path),
        str(output_path)
    ], check=True)

    # Load and return output for chaining
    with open(output_path) as f:
        return json.load(f)

def main(use_case_path):
    with open(use_case_path) as f:
        use_case = json.load(f)

    run_id = str(uuid.uuid4())
    print(f"\n🔁 Starting run {run_id} for: {use_case['run_name']}\n")

    output_dir = create_run_folder(run_id)

    # Save initial metadata
    metadata = {
        "run_id": run_id,
        "use_case": use_case["run_name"],
        "start_time": datetime.utcnow().isoformat(),
        "agent_list": use_case["enabled_agents"]
    }
    with open(output_dir / "run_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    # Initialize pipeline with use case as initial input
    current_input = use_case

    for i, agent in enumerate(use_case["enabled_agents"]):
        try:
            current_output = run_agent(agent, current_input, output_dir, i)
            current_input = current_output
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running agent {agent}: {e}")
            break

    print(f"\n✅ Tracer run {run_id} complete.")
    print(f"📁 Outputs saved to: {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python run_tracer.py <use_case.json>")
        sys.exit(1)
    main(sys.argv[1])
