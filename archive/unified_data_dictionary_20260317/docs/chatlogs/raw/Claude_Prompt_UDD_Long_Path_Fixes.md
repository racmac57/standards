# Claude plan review and markdown file
_Exported on 1/20/2026 at 21:21:17 EST from Cursor (2.3.41)_

---

**User**

@claude_prompt_and_long-path_fixes_2b6e70d0.plan.md (1-161)  can you review the directory contents and create a claude..md file

---

**Cursor**

Reviewing the directory structure and referenced files so we can create the Claude prompt file.


Creating the Claude prompt file from the plan and the reviewed code:


Summary of what was added:

## Created: `c:\_chunker\CLAUDE_CODE_PROMPT_UDD_LongPath_And_Fixes.md`

The prompt file matches the plan and is aimed at Claude Code. It includes:

### 1. **Context**
- OneDrive “path too long” (260-character limit)
- Recursive `Standards\unified_data_dictionary` paths
- Process_UDD_Chatlog timeout with `"Searching for: SEARCH_BASENAME:*=_*"`

### 2. **Tasks (A–D)**

- **A. SEARCH_BASENAME (Process_UDD_Chatlog.bat)**  
  - Remove the two `set "SEARCH_BASENAME=..."` lines that alter `"` and `*`.  
  - Keep the rest of the sanitization and `~0,60` truncation.

- **B. Chunker path limits (watcher_splitter.py)**  
  - Resolve `output_dir`/`archive_dir` with `expandvars` and `abspath`.  
  - `MAX_PATH` from `config.get("max_total_path_length", 240)`, `RESERVED = 100`.  
  - `max_base` and `clean_base` logic for `file_output_folder` and for archive paths in `move_to_processed_enhanced` and `celery_tasks.archive_processed_file`.  
  - Optional `max_total_path_length` in `config.json`.

- **C. UDD batch path limits (Process_UDD_Chatlog.bat)**  
  - Truncate the `CHUNKED_DIR` subfolder name so the full path stays ≤ 260; optional uniqueness suffix to avoid collisions.

- **D. Recursive path audit**  
  - Check UDD for symlinks/junctions, `.code-workspace` includes, and scripts that copy UDD into itself.  
  - Optional `scripts/Find-LongPaths.ps1` to report paths > 260 and repeated path segments.

### 3. **References**
- Paths and line ranges for:
  - `Process_UDD_Chatlog.bat`
  - `watcher_splitter.py` (`sanitize_folder_name`, `file_output_folder`, `move_to_processed_enhanced`)
  - `celery_tasks.archive_processed_file`
  - `config.json`

### 4. **Acceptance and summary table**
- Definition of done and a short table of edits by file.

The prompt is self-contained so it can be copied into a new Claude Code session. `Process_UDD_Chatlog.bat` is referenced at  
`C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary\scripts\Process_UDD_Chatlog.bat` (it is outside `c:\_chunker`).

---

**User**

I'm preparing to export this chat. Please generate a descriptive filename that summarizes the main topic or task of this conversation.

Requirements:
• 4-8 words
• Title Case (capitalize major words)
• Replace spaces with underscores
• Include .md extension
• No dates or special characters

Output only the filename, nothing else.

After export, I'll process it using: scripts\quick_process_chatlog.bat

---

**Cursor**


Claude_Prompt_UDD_Long_Path_Fixes.md

