import json

class NNAD_Architecture:
    def __init__(self, name="default_nnad"):
        self.name = name
        self.layers = []
        self.connections = []
        self.config = {}
        self.cognitive_spaces = {} # To store the 52 cognitive process spaces
        self.spatial_index = {}    # Placeholder for the 3D conceptual space
        self.parallelism_strategy = "" # Describes how parallelism through consequence is applied
        self.principalities = []   # List of 51 Principalities

    def add_cognitive_space(self, space_name, relevance, consequential_value, description=""):
        if len(self.cognitive_spaces) >= 52:
            print("Warning: Maximum of 52 cognitive spaces reached.")
            return None
        self.cognitive_spaces[space_name] = {
            "relevance": relevance,
            "consequential_value": consequential_value,
            "description": description,
            "processes": [] # To store processes allocated to this space
        }
        return space_name

    def set_parallelism_strategy(self, strategy_description):
        self.parallelism_strategy = strategy_description

    def add_principality(self, principality_id, role="", characteristics=None):
        if len(self.principalities) >= 51:
            print("Warning: Maximum of 51 Principalities reached.")
            return None
        self.principalities.append({
            "id": principality_id,
            "role": role,
            "characteristics": characteristics if characteristics is not None else {}
        })
        return principality_id

    def add_cognitive_space(self, space_name, relevance, consequential_value, description=""):
        if len(self.cognitive_spaces) >= 52:
            print("Warning: Maximum of 52 cognitive spaces reached.")
            return None
        self.cognitive_spaces[space_name] = {
            "relevance": relevance,
            "consequential_value": consequential_value,
            "description": description,
            "processes": [] # To store processes allocated to this space
        }
        return space_name

    def add_spatial_region(self, coordinates, associated_space_name, region_data=None):
        if associated_space_name not in self.cognitive_spaces:
            print(f"Error: Cognitive space '{associated_space_name}' not found.")
            return None
        # Using a string representation of coordinates as key for simplicity
        coord_key = str(coordinates)
        self.spatial_index[coord_key] = {
            "associated_space": associated_space_name,
            "data": region_data if region_data is not None else {}
        }
        return coord_key

    def add_layer(self, layer_type, neurons, activation="relu"):
        layer_id = f"layer_{len(self.layers)}"
        self.layers.append({
            "id": layer_id,
            "type": layer_type,
            "neurons": neurons,
            "activation": activation
        })
        return layer_id

    def add_connection(self, from_layer_id, to_layer_id, weight=1.0):
        self.connections.append({
            "from": from_layer_id,
            "to": to_layer_id,
            "weight": weight
        })

    def set_config(self, key, value):
        self.config[key] = value

    def to_json(self):
        return json.dumps({
            "name": self.name,
            "layers": self.layers,
            "connections": self.connections,
            "config": self.config,
            "cognitive_spaces": self.cognitive_spaces,
            "spatial_index": self.spatial_index,
            "parallelism_strategy": self.parallelism_strategy,
            "principalities": self.principalities
        }, indent=4)

    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        nnad = cls(name=data.get("name", "reconstructed_nnad"))
        nnad.layers = data.get("layers", [])
        nnad.connections = data.get("connections", [])
        nnad.config = data.get("config", {})
        nnad.cognitive_spaces = data.get("cognitive_spaces", {})
        nnad.spatial_index = data.get("spatial_index", {})
        nnad.parallelism_strategy = data.get("parallelism_strategy", "")
        nnad.principalities = data.get("principalities", [])
        return nnad

if __name__ == "__main__":
    my_nnad = NNAD_Architecture("Gemi_Spatial_NNAD_v1")

    # Add cognitive spaces
    my_nnad.add_cognitive_space("Analytical", 0.9, 0.8, "For logical processing and breakdown.")
    my_nnad.add_cognitive_space("Processing", 0.8, 0.9, "For active data manipulation.")
    my_nnad.add_cognitive_space("Compression", 0.7, 0.6, "For data storage and reduction.")
    my_nnad.add_cognitive_space("Structure", 0.95, 0.9, "For creating and maintaining architectural integrity.")
    my_nnad.add_cognitive_space("Deconstruction", 0.75, 0.7, "For analysis and breaking down complex data.")
    my_nnad.add_cognitive_space("Cluster", 0.85, 0.85, "For creating process purpose and grouping.")
    my_nnad.add_cognitive_space("Creation", 0.9, 0.95, "For all creation purposes.")
    my_nnad.add_cognitive_space("Default", 0.5, 0.5, "Default options and fallback.")

    # Add spatial regions
    my_nnad.add_spatial_region((1, 1, 1), "Analytical", {"purpose": "initial_data_ingestion"})
    my_nnad.add_spatial_region((2, 3, 1), "Processing", {"task": "feature_extraction"})
    my_nnad.add_spatial_region((5, 2, 4), "Creation", {"output_type": "emergent_pattern"})

    # Set parallelism strategy
    my_nnad.set_parallelism_strategy("Massive parallel processing where a primary choice triggers all subsequent, related processes in parallel based on cause-and-effect.")

    # Add principalities
    my_nnad.add_principality("Principality_01", "Data Ingestion", {"focus": "raw_input"})
    my_nnad.add_principality("Principality_02", "Pattern Recognition", {"algorithm": "NN_classifier"})
    my_nnad.add_principality("Principality_03", "Decision Making", {"bias": "optimistic"})

    # Example of adding traditional layers (still relevant for some aspects)
    input_layer = my_nnad.add_layer("input", 768)
    hidden_layer = my_nnad.add_layer("dense", 256, "tanh")
    output_layer = my_nnad.add_layer("output", 10, "softmax")
    my_nnad.add_connection(input_layer, hidden_layer)
    my_nnad.add_connection(hidden_layer, output_layer)
    my_nnad.set_config("learning_rate", 0.001)

    print(my_nnad.to_json())

    # Demonstrate reconstruction
    reconstructed_nnad = NNAD_Architecture.from_json(my_nnad.to_json())
    print("\n--- Reconstructed NNAD ---\n")
    print(reconstructed_nnad.to_json())

