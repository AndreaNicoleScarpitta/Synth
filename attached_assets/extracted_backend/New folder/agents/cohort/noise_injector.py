from utils.base_agent import BaseAgent

class NoiseInjector(BaseAgent):
    def run(self, input_data: dict) -> dict:
        '''
        Stub for NoiseInjector. Replace with real logic.
        '''
        output = {
            "noise_injector": "stubbed output"
        }

        log = "NoiseInjector executed with stub output."

        return {
            "output": output,
            "log": log
        }
