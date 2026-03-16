# Fix_OneDrive_Long_Path_Issue.ps1

Resolves OneDrive **"We can't sync this item because the path is too long"** errors by shortening folder and file names in the affected tree. OneDrive enforces a 260‑character path limit even when Windows long paths are enabled.

---

## When to use

- OneDrive shows **"path is too long"** (or "Shorten the path by X characters").
- The error points at a path under `Standards_Backup_*`, `09_Reference\Standards\tools\NULL`, `unified_data_dictionary`, long `chunked` folders, or similar deep/long names.

---

## Quick start: run repair

From **PowerShell** (not necessarily from the SYNC folder):

```powershell
& "C:\Users\carucci_r\OneDrive - City of Hackensack\SYNC\Fix_OneDrive_Long_Path_Issue.ps1" -Repair -RootPath "C:\Users\carucci_r\OneDrive - City of Hackensack\SYNC\ssocc_desk\temp\Standards_Backup_20260116_181122"
```

If the root was already renamed to `SB_160116`:

```powershell
& "C:\Users\carucci_r\OneDrive - City of Hackensack\SYNC\Fix_OneDrive_Long_Path_Issue.ps1" -Repair -RootPath "C:\Users\carucci_r\OneDrive - City of Hackensack\SYNC\ssocc_desk\temp\SB_160116"
```

**For `09_Reference\Standards\tools\NULL`** (leftover from UDD merge; see Standards CHANGELOG v2.2.0):

```powershell
& "C:\Users\carucci_r\OneDrive - City of Hackensack\SYNC\Fix_OneDrive_Long_Path_Issue.ps1" -Repair -RootPath "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\tools\NULL"
```

- Repair renames `NULL` → `udd_legacy`, then `unified_data_dictionary` → `udd`, `Standards` → `Std`, and long chunk folders. **Recommended:** after repair, delete the `udd_legacy` tree (it is obsolete; see **tools\\NULL: delete instead of repair** below).

**Before running:** Exit OneDrive and close Cursor/Explorer (or any app using that folder) to avoid "Access denied."

**After repair:** Restart OneDrive; in the error dialog click **Try again** or wait for sync.

---

## What the repair does

| Original | Shortened |
|----------|-----------|
| `Standards_Backup_20260116_181122` | `SB_160116` |
| `NULL` (in `09_Reference\Standards\tools\`) | `udd_legacy` |
| `unified_data_dictionary` | `udd` |
| `Standards` | `Std` |
| Long chunk folders (e.g. `2025_12_17_22_24_14_updated_chunk_cursor_unified_data_dictionary_setup`) | `c_20251217_2224` |
| Matching files (`*_transcript.md`, `*_sidecar.json`, `*_transcript.json`, `*.origin.json`) | Same short prefix (e.g. `c_20251217_2224_transcript.md`) |

---

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `-Repair` | — | Run the automatic path-shortening repair. Without it, the script only runs a diagnostic. |
| `-RootPath` | `...\Standards_Backup_20260116_181122` | Root folder to repair. Use `...\SB_160116` or `...\udd_legacy` if already renamed; use `...\09_Reference\Standards\tools\NULL` for the UDD-merge leftover. |
| `-FilePath` | *(long path from the OneDrive error)* | Used only in diagnostic mode to report path length. |
| `-WhatIf` | — | Preview renames without changing anything. |

---

## Running from the SYNC folder

```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\SYNC"
.\Fix_OneDrive_Long_Path_Issue.ps1 -Repair
.\Fix_OneDrive_Long_Path_Issue.ps1 -Repair -RootPath "C:\...\SB_160116"   # if root already renamed
.\Fix_OneDrive_Long_Path_Issue.ps1 -Repair -WhatIf   # preview only
```

---

## Diagnostic mode (no `-Repair`)

Without `-Repair`, the script reports:

- Path length and OneDrive’s 260‑character limit
- Whether Windows long paths are enabled
- OneDrive process status
- A reminder to run with `-Repair` to fix.

---

## Troubleshooting

### "Access denied" when renaming

1. **Exit OneDrive** (tray icon → Exit).
2. **Close Cursor** (or any IDE) and **File Explorer** windows for that folder.
3. Run the script again from an **external PowerShell** (not from Cursor).

### "Root path not found"

- The `-RootPath` folder may have been moved or deleted. Use the correct path (e.g. `SB_160116` if it was already renamed).
- If the long path exists only in OneDrive (never created locally), run the repair after the folder exists on disk, or shorten the path in OneDrive on the web.

### Script is slow

- Repair does many recursive scans; on large trees it can take **5–10 minutes**. Let it finish.
- Run from a normal PowerShell (not Cursor) to avoid timeouts.

### "SKIP: 'SB_160116' already exists"

- Another folder with that name is in the same parent. Remove or rename it, or pass a different `-RootPath`.

### tools\NULL (09_Reference): delete instead of repair

`09_Reference\Standards\tools\NULL` is the **old `unified_data_dictionary` leftover** from the UDD hybrid migration (CHANGELOG v2.2.0: recursive symlink issue; "can be manually removed"; "does not affect functionality"). The canonical UDD is at `tools/unified_data_dictionary/`.

**Option A – Delete (recommended):** Remove the whole `tools\NULL` tree so OneDrive stops trying to sync it. Exit OneDrive first. In PowerShell:

```powershell
$p = "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\tools\NULL"
if (Test-Path -LiteralPath $p) { Remove-Item -LiteralPath $p -Recurse -Force }
```

If that fails with long-path errors, run **Repair** first (to shorten paths), then delete the resulting `tools\udd_legacy` folder.

**Option B – Repair only:** Run with `-RootPath "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\tools\NULL"` to shorten for sync; you can delete `udd_legacy` afterward.

### Folder already deleted (path too long / "ghost" in OneDrive)

If the **folder no longer exists on disk** but OneDrive still shows "path is too long" for it, OneDrive has a **phantom reference** in its sync database. `-Repair` cannot run (there is nothing to rename).

**Do this instead:**

1. **Reset OneDrive’s sync state**
   - **Stop OneDrive:** Tray icon → **Exit**. If the tray icon is missing: **Task Manager** → **Background processes** → End **Microsoft OneDrive Sync Service**, **Microsoft OneDriveFile Co-Authoring Executable**, **Microsoft OneDriveFileSyncHelper** (and **FileSyncHelper**).
   - **Clear cache:** `Win+R` → `%LocalAppData%\Microsoft\OneDrive` → rename `logs` (e.g. to `logs_backup_YYYYMMDD_HHmmss`), delete any `.dat`/`.db` in that folder (do **not** remove `OneDrive.exe`).
   - **Restart OneDrive:** Run `"C:\Program Files\Microsoft OneDrive\OneDrive.exe"` (Win+R; quotes required) or Start → **OneDrive**. On some installs `OneDrive.exe` is in `%LocalAppData%\Microsoft\OneDrive`; use that path if it exists there.
   - Or use **Unlink this PC** (OneDrive Settings → Account) then sign back in. **Full Unlink/re-link walkthrough** (screens, work account, "Use this folder," "Back up folders," shared files, sync progress, power for overnight): `Fix_OneDrive_Phantom_Path_Permanent.md` → **B. Unlink and re-link**.
2. **Delete from OneDrive on the web:** [onedrive.live.com](https://onedrive.live.com) → `09_Reference` → `Standards` → `tools` → delete `tools` or `tools\unified_data_dictionary` so the item is gone from the cloud.

See `Investigation_09_Reference_UDD_Sync_Break.md` for full fix steps (e.g. stopping OneDrive via Task Manager when the tray icon is missing) and why a deleted `tools\unified_data_dictionary` (or `tools\NULL`) still causes the error.

### OneDrive sync status messages (tray and pop-up)

| Message / icon | Meaning |
|----------------|---------|
| **Your files are synced.** | Up to date. |
| **Processing X changes** | Sync in progress; X is the queue size. With 400K+ changes and 300+ GB, can take **many hours** (6–24+). Click **>** or the line to open the activity list. |
| **Looking for changes** | Scanning for new or modified files; can last minutes on large libraries. Toggling between this and "Your files are synced" when you open the tray is **normal**. |
| **Downloaded to &lt;folder&gt;** / *X hour ago* | Last synced items; old timestamps are normal if nothing new has synced. |
| **Tray: cloud+check** | Synced. |
| **Tray: arrows** | Syncing or "Looking for changes." |
| **Tray: red / !** | Error; click for details (e.g. "path is too long"). |
| **Pause syncing (2 h) → Resume** | Can unstick when "Looking for changes" runs a long time with no new syncs. |

More detail (stopping OneDrive when the tray icon is missing, Task Manager): `Investigation_09_Reference_UDD_Sync_Break.md` → **OneDrive Sync Status Messages**.

---

## Related

- `Fix_OneDrive_Phantom_Path_Permanent.md` — **Unlink/re-link (B):** re-link screens (work account, "Use this folder," "Back up folders"), shared files, "Processing X changes," **sync speed and power** (lock vs sleep, overnight).
- `Investigation_09_Reference_UDD_Sync_Break.md` — Why a **deleted** `09_Reference\Standards\tools\unified_data_dictionary` (recursive path) still breaks sync; phantom reference, cache reset (Task Manager, Program Files OneDrive.exe), and **OneDrive sync status messages** (tray, pop-up, Pause/Resume).
- `Enable_Windows_Long_Paths.ps1` — Enables Windows long path support (OneDrive may still enforce 260 characters).
- `Enable_Windows_Long_Paths_README.md` — Long path setup and scheduling.
- `Fix_OneDrive_Long_Path_Sync_Issues.md` — Other long-path cases (e.g. Evernote, Chunker).
- `OneDrive_Sync_Error_Troubleshooting_Fix.md` — Invalid names, "nul", resetting OneDrive cache.
