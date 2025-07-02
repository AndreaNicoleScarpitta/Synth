# Synthetic Ascension Langflow Exports

This directory contains Langflow-compatible workflow exports for the Synthetic Ascension EHR generation system.

## Files

- `synthetic_ascension_complete_pipeline.json` - Complete 6-phase pipeline with all agent categories

## Usage

1. Install Langflow locally:
   ```bash
   pip install langflow
   ```

2. Start Langflow:
   ```bash
   langflow run
   ```

3. Import the JSON files through the Langflow UI

4. Connect to your Synthetic Ascension backend at http://localhost:8004

## Custom Components

Each agent is exported as a custom Langflow component that can:
- Connect to the live Synthetic Ascension backend
- Run in simulation mode for testing
- Be modified and extended in Langflow

## Modifying Flows

You can:
- Rearrange agent execution order
- Add new custom components
- Modify agent parameters
- Create new conditional logic
- Export modified flows back to JSON

## Integration

The exported flows maintain full compatibility with your Synthetic Ascension backend while allowing visual workflow modification in Langflow.
