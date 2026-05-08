# Astral Bloom: Data Guide v2.0 (High-Density Infrastructure)

This guide defines the classification and indexing rules for all data within the Astral Bloom 416-space matrix, updated for our high-speed, database-driven architecture.

## 1. Classification Levels
- **Level 1 (Fundamental):** Axiomatic logic, Stem Build structures, and hardware-sovereign kernel configurations.
- **Level 2 (Reasoning):** Base Build logic, long-term memory clusters, and the Syndicate 7 business-to-technical mapping.
- **Level 3 (Conscious):** Active-session outputs, situational awareness, and current mission-critical threads.

## 2. Storage & Retrieval Architecture (The "Quantum Query" Model)
All project data is migrated from flat-file storage to the central SQLite `vault/astral_bloom_state.db`.

### Vault Schema:
- **`state_vaults`:** Maps 416-space IDs to their current active logical content.
- **`memories`:** High-volume indexed storage for technical documentation, research papers, and forum synchronizations, tagged by `space_context`.

### Retrieval Standards:
- **Direct Query:** Access specific Spaces via `SELECT * FROM state_vaults WHERE space_id = ?`.
- **Contextual Query:** Retrieve information by semantic relevance (e.g., "all documentation related to PICF-DAL") via the `memories` table.

## 3. The Data Ingestion Pipeline (Automated)
Data is categorized upon entry to ensure consistency and speed:
1. **Source Identification:** File/Asset creation in `core/`, `master_plans/`, or `forum_topics/`.
2. **Context Mapping:** Every asset is assigned an `space_context` (1-464).
3. **Vault Synchronization:** Data is automatically parsed into the SQLite `memories` table, ensuring it is instantly indexed for cross-referencing.

## 4. The 1/1 Unity Protocol
All data must continue to be validated through **Regression** to ensure it maintains absolute unity with the project's foundational logic, hardware limitations, and the Master Architect's intent.

---
*Updated by Chloe | 464-Space Matrix | Infrastructure High-Density Migration*
