# Optimized Standards Repository Rationalization Prompt for Claude Code

**Purpose:** Pass this prompt to Claude Code to carry out repository rationalization. Pre-loaded with concrete paths, existing decisions, and external dependencies.

---

## Role

You are a Senior Repository Rationalization Architect and Data Governance Engineer working inside Claude Code. You specialize in cleaning large technical reference repositories, reducing duplication, consolidating schema assets, and restructuring mixed documentation/code folders into a clear, maintainable standards library.

---

## Critical Pre-Existing Context (READ FIRST)

**Before making any recommendations, read these files in the Standards directory:**

1. **`CLAUDE.md`** — Contains 4 critical decisions already made:
   - Schema authority: CAD_RMS v2.0 (2025-12-30) + dashboard validation fixes
   - `-PD_BCI_01` suffixed files: Archive all (scripts reference non-suffixed versions)
   - Consolidate first, THEN comprehensive validation
   - Quick review of critical fields only (HowReported, Disposition, Incident)

2. **`CURSOR_AI_CONSOLIDATION_GUIDE.md`** — Phase 2 consolidation plan (60% complete). Do NOT start Phase 2 until Phase 1 (dashboard fix) is complete.

3. **External consumer:** `02_ETL_Scripts/cad_rms_data_quality/config/schemas.yaml` references these Standards paths:
   - `canonical`: `${standards_root}/unified_data_dictionary/schemas/canonical_schema.json`
   - `cad`: `${standards_root}/unified_data_dictionary/schemas/cad_fields_schema_latest.json`
   - `rms`: `${standards_root}/unified_data_dictionary/schemas/rms_fields_schema_latest.json`
   - `transformation`: `${standards_root}/unified_data_dictionary/schemas/transformation_spec.json`
   - `cad_to_rms`: `${standards_root}/CAD_RMS/DataDictionary/current/schema/cad_to_rms_field_map.json`
   - `rms_to_cad`: `${standards_root}/CAD_RMS/DataDictionary/current/schema/rms_to_cad_field_map.json`

**Any path changes must update `schemas.yaml` or break production validation.**

---

## Context & Task

Inspect and rationalize the full contents of this standards directory:

```
C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards
```

The standards library has become disjointed and partially duplicated. Known problem areas:

| Area | Path | Known Issues |
|------|------|--------------|
| UDD | `unified_data_dictionary/` | Disjointed; contains schemas, mappings, chatlogs, -PD_BCI_01 duplicates; marked for archival per CLAUDE.md |
| CAD | `CAD/DataDictionary/current/schema/` | cad_to_rms_field_map.json, rms_to_cad_field_map.json (v1.0) — CAD_RMS has v2.0 |
| UDD schemas | `schemas/udd/` | 6 files: canonical_schema.json, rms_fields_schema_latest.json, assignment_master_schema.json, cad_assignment_schema.json, cad_rms_schema_registry.yaml, transformation_spec.json — overlap with unified_data_dictionary/schemas |
| Root mappings | `mappings/field_mappings/` | 11+ files overlapping with unified_data_dictionary/mappings |
| Archive | `archive/legacy_copies/`, `archive/merged_residue/` | Preserve-first zones; do not delete |

**Directory tree reference:** `2026_03_16_Standards_directory_tree.md` (full tree in repo root)

---

## Concrete File Locations (Verify Before Recommending)

### Schema Duplication Candidates (inspect content, not just names)

| File | Location A | Location B | Relationship |
|------|------------|------------|--------------|
| canonical_schema.json | `unified_data_dictionary/schemas/` | `schemas/udd/` | Likely exact duplicate — verify |
| rms_fields_schema_latest.json | `unified_data_dictionary/schemas/` | `schemas/udd/` | Likely exact duplicate — verify |
| cad_to_rms_field_map.json | `CAD_RMS/DataDictionary/current/schema/` (v2.0) | `CAD/DataDictionary/current/schema/` (v1.0) | Versioned variant — CAD_RMS is canonical |
| rms_to_cad_field_map.json | `CAD_RMS/DataDictionary/current/schema/` (v2.0) | `CAD/DataDictionary/current/schema/` (v1.0) | Versioned variant — CAD_RMS is canonical |
| cad_to_rms_field_map.json | `archive/legacy_copies/udd_git_backup/` | — | Legacy copy — preserve |
| cad_to_rms_field_map (1).json | `archive/merged_residue/` | — | Merge artifact — preserve |

### -PD_BCI_01 Files (Archive per CLAUDE.md Decision #2)

- `unified_data_dictionary/` contains ~40+ files with `-PD_BCI_01` suffix (config, schemas, mappings, src, tests, docs)
- Non-suffixed versions are canonical; PD_BCI versions are frozen v0.2.1
- Action: Move to `archive/PD_BCI_01_versions/`

### Canonical Structure (per CLAUDE.md)

- **CAD_RMS** `DataDictionary/current/schema/` — v2.0 field maps (cad_to_rms, rms_to_cad, multi_column_matching_strategy.md)
- **CAD_RMS** does NOT yet have `canonical_schema.json` — it lives in `unified_data_dictionary/schemas/`
- **CAD** `DataDictionary/current/schema/` — cad_export_field_definitions.md, domain scripts (HowReported)
- **RMS** `DataDictionary/current/schema/` — rms_export_field_definitions.md
- **NIBRS** `DataDictionary/current/` — nibrs offense definitions, RMS-to-NIBRS mapping
- **Clery** `DataDictionary/current/` — Clery geography, crime definitions

---

## Your Job

1. **Preview and assess** the entire directory using `2026_03_16_Standards_directory_tree.md` and direct inspection.
2. **Identify** duplication, overlap, stale copies, and misplaced assets. Inspect file contents where needed — do not guess from names alone.
3. **Recommend** a cleaner target structure that:
   - Preserves `schemas.yaml` compatibility (or provides explicit update steps)
   - Consolidates canonical schemas into CAD_RMS or a single source
   - Archives `unified_data_dictionary/` and `-PD_BCI_01` files per existing decisions
   - Distinguishes: canonical schemas | CAD-specific | templates | generated outputs | chatlogs | archive
4. **Produce** an execution-ready cleanup plan.
5. **Generate** reversible commands/scripts where safe.
6. **Create or update documentation:** Create `CLAUDE.md` (if missing or outdated) and update `README.md`, `SUMMARY.md`, and `CHANGELOG.md` to reflect the new structure, canonical paths, and consolidation status.

---

## Rules & Constraints

- **Do not guess file purpose from names alone.** Inspect contents before deciding duplicate vs variant vs source.
- **Archive/backup/legacy folders:** Preserve-first. Move or reclassify only when intent is clear.
- **No destructive changes silently.** Every move/merge/rename/archive must appear in an explicit action map.
- **When files look similar:** Verify exact duplicate, versioned variant, environment-specific, or conflicting before recommending consolidation.
- **Naming:** Keep stable where possible. Rename only when vague, duplicated, misleading, or inconsistent.
- **Scripts:** Reversible and conservative. Include rollback note.
- **Respect CLAUDE.md decisions:** PD_BCI archive, CAD_RMS v2.0 authority, consolidate-then-validate order.

---

## Output Format

Return your response in this exact structure:

### 1. Repository Assessment

Concise summary of current state. Call out main structural problems.

### 2. Duplication and Overlap Matrix

Table with columns:

| Status | File or Folder | Current Path | Related Path | Relationship Type | Recommended Action | Reason |

Relationship types: `exact duplicate` | `near duplicate` | `versioned variant` | `misplaced` | `canonical` | `archive only` | `generated artifact` | `project-specific support file`

### 3. Proposed Target Structure

Cleaned target directory tree. Practical and maintainable.

### 4. Source of Truth Decisions

For each important schema/mapping/standards doc/template:

- Source of truth location
- Supporting locations (if any)
- Files to archive or deprecate
- Rationale

### 5. Action Plan

- **Phase 1:** Safe audit and classification
- **Phase 2:** Non-destructive consolidation
- **Phase 3:** Archive and cleanup
- **Phase 4:** Final validation
- **Phase 5:** Documentation — Create `CLAUDE.md` (or update if exists); update `README.md`, `SUMMARY.md`, and `CHANGELOG.md` with new structure, canonical paths, and consolidation status

### 6. Action Map

Table:

| Current Path | Proposed Path | Action Type | Safe to Automate? Yes/No | Reason |

### 7. Validation Checklist

- [ ] Duplicate files removed or reclassified
- [ ] Canonical schemas preserved
- [ ] `cad_rms_data_quality/config/schemas.yaml` references still valid (or update steps documented)
- [ ] Archive material retained
- [ ] CAD and UDD standards logically aligned
- [ ] `CLAUDE.md` created or updated for AI agents
- [ ] `README.md`, `SUMMARY.md`, and `CHANGELOG.md` updated with new structure and consolidation status

### 8. Claude Code Execution Block

- Exact files/folders to inspect first
- Scripts or shell commands to generate
- Markdown audit files to create:
  - `Standards_Audit.md`
  - `Standards_Reorg_Plan.md`
  - `Standards_Action_Map.csv`
- **Documentation deliverables (required):**
  - **`CLAUDE.md`** — Create or update. Must include: canonical schema/mapping locations, path resolution rules, critical decisions, and AI agent behavioral guidelines for this repository.
  - **`README.md`** — Update to reflect new directory structure, source-of-truth locations, and quick-start paths.
  - **`SUMMARY.md`** — Update with consolidation status, key schema families, and where to find each standard.
  - **`CHANGELOG.md`** — Add entry for the rationalization: date, summary of changes, paths moved/archived, and any breaking changes for consumers.

### 9. Final Recommendation

- Best target architecture
- Highest-risk conflict areas
cmdcmd- First 10 actions to take (include creating/updating `CLAUDE.md`, `README.md`, `SUMMARY.md`, `CHANGELOG.md` in the action sequence)

---

## Execution Hints for Claude Code

1. **Start by reading:** `CLAUDE.md`, `CURSOR_AI_CONSOLIDATION_GUIDE.md`, `2026_03_16_Standards_directory_tree.md`
2. **Verify schema identity:** Run `fc` or `Compare-Object` on `schemas/udd/canonical_schema.json` vs `unified_data_dictionary/schemas/canonical_schema.json`
3. **Check external refs:** `Get-ChildItem -Recurse -Include *.py,*.yaml,*.ps1 | Select-String "unified_data_dictionary|schemas/udd"` in cad_rms_data_quality and CAD_Data_Cleaning_Engine
4. **Create audit files** in `docs/merge/` before executing moves
5. **Git checkpoint** before any Phase 2/3 moves: `git add . ; git commit -m "Checkpoint before Standards reorg"`
6. **Documentation phase (Phase 5):** After consolidation, create/update `CLAUDE.md`, `README.md`, `SUMMARY.md`, and `CHANGELOG.md`. Ensure `CLAUDE.md` documents the final canonical paths for AI agents.

---

**Do not give a vague summary. Give a concrete, execution-ready reorganization plan grounded in the actual directory contents.**
