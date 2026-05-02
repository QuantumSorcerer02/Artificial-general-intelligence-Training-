class CognitiveCluster:
    def __init__(self, name):
        self.name = name
        self.active_state = "IDLE"

    def process(self, context, momentum):
        self.active_state = "PROCESSING"
        # Base processing logic to be overridden
        return context
