class BaseAgent(ABC):
    def __init__(self, name=None):
        self.name = name or self.__class__.__name__

    @abstractmethod
    def run(self, input_data: dict) -> dict:
        pass
