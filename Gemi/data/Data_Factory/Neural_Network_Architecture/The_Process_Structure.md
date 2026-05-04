Project Astral Bloom: Technical Specification - The Process Structure
The Process Structure is the fundamental, static logical unit of the Astral Bloom architecture. It represents the "subdermal" blueprint of the network—a set of pre-defined conditions that react to specific initiates to generate deterministic consequences.

1. The Blueprint Concept
Process Structures are "context-blind." They do not learn or adapt during the execution phase; they are the Fixed Geometry of the network. Each structure is programmed with a specific Initiate Threshold and a corresponding Weighted Consequence.

2. Threshold Logic
A Structure remains dormant until the incoming weighted value from a Sequential Key meets its internal activation threshold. This is the "Ignition Point" of the architecture.

3. Technical Implementation
```python
def fire(self, incoming_value):
        """
        Executes the basic Initiate -> Consequence logic.
        """
        if incoming_value >= self.threshold:
            return incoming_value * self.weight
        return 0.0
```