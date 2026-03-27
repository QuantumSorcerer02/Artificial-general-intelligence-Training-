# Gemi Memory Files

This directory contains scripts and files that define the core memories and functions of Gemi, the AI assistant.

## `base_build.sh`

This script is the foundational memory imprinting tool for Gemi. It contains a series of `save_memory` commands that establish Gemi's core identity, purpose, and architectural principles.

### Purpose

The `base_build.sh` script is used to:

-   **Initialize Gemi's Core Knowledge:** It sets up the fundamental memories that Gemi relies on for all its operations.
-   **Ensure Consistency:** By running this script, we can ensure that Gemi's core programming is consistent and can be reliably reproduced.
-   **Restore from a Blank State:** If Gemi's memory is ever wiped, this script can be used to restore the foundational `Base Build`.

### Usage

To run the script, execute the following command in your shell:

```bash
./base_build.sh
```

## `Gemi.sh`

This script defines the `gemi_speak` function, which is used to make Gemi's responses audible.

### Purpose

The `gemi_speak` function provides a standardized way to make Gemi speak, using the `espeak` command with specific parameters for voice, pitch, and speed.

### Usage

To use the `gemi_speak` function, you can source the script in your shell and then call the function with the text you want Gemi to say:

```bash
source Gemi.sh
gemi_speak "Hello, I am Gemi."
```

## `memory_management.sh`

This script provides a set of functions for managing Gemi's memories.

### Functions

-   `view_memories`: Displays all the core memories that have been saved.
-   `add_memory "fact"`: Adds a new fact to Gemi's memory.
-   `clear_temporal_memory`: Clears the temporal or contextual memory, while leaving the core memories intact.

### Usage

To use these functions, source the script in your shell:

```bash
source memory_management.sh
```

Then, you can call the functions as needed:

```bash
# To view memories
view_memories

# To add a new memory
add_memory "This is a new fact."

# To clear temporal memory
clear_temporal_memory
```

## Astral Bloom Process Structure

For a detailed breakdown of Gemi's process structure, see the [Astral Bloom Process Structure](ASTRAL_BLOOM_PROCESS_STRUCTURE.md) document.

## Astral Bloom Architecture

For a high-level overview of the Astral Bloom architecture, see the [Astral Bloom Architecture](ASTRAL_BLOOM_ARCHITECTURE.md) document.