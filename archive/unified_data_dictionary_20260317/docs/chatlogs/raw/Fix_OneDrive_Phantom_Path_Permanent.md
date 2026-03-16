# Permanent Fix: OneDrive "Path Is Too Long" (Phantom)

When the **"We can't sync this item because the path is too long"** error keeps returning after a cache reset, OneDrive has a **phantom reference** to that path. It can be **(A) in the cloud** or **(B) only in your PC’s sync database**. Use the fix that matches what you find.

---

## Problem path (from the error)

```
09_Reference\Standards\tools\unified_data_dictionary\Standards\unified_data_dictionary\Standards\unified_data_dictionary\...\unified_data_dictionary.code-workspace
```

The recursive `Standards\unified_data_dictionary\...` tree under `tools\unified_data_dictionary` is **legacy/obsolete**. The canonical UDD is at `09_Reference\Standards\unified_data_dictionary` (not under `tools`). It is safe to remove `tools\unified_data_dictionary` or the whole `tools` folder.

---

## Which fix to use

**In OneDrive on the web:** Go to **09_Reference** → **Standards** and **look at the folder list** (don’t rely only on search).  
- **If you see a `tools` folder** → use **A. Delete from OneDrive on the web** below.  
- **If there is no `tools` folder** (search for “tools” in that folder also returns nothing) → the phantom is **only on your PC**. Use **B. Unlink and re-link OneDrive** below.

---

## A. Delete from OneDrive on the web (when `tools` exists in the cloud)

### 1. Open OneDrive in your browser

- **Work/school (City of Hackensack):**  
  [https://www.onedrive.com](https://www.onedrive.com) or [https://onedrive.live.com](https://onedrive.live.com)  
  Sign in with your work account (e.g. `carucci_r@hackensackpd.local`).  
  If your org uses SharePoint, you may be redirected; use the OneDrive / “My files” view.

- Or run this to open OneDrive in your default browser:
  ```powershell
  Start-Process "https://www.onedrive.com"
  ```

### 2. Go to the folder

In OneDrive, go to **`09_Reference`** → **`Standards`**. You should see **`tools`** in the list.

### 3. Delete the problematic tree

**Option A – Delete the whole `tools` folder (simplest)**

- In `Standards`, select the **`tools`** folder.
- Delete it (right‑click → **Delete**, or select and use the **Delete** / trash icon).
- Confirm.  
  This removes `tools\unified_data_dictionary` and the entire long-path tree.

**Option B – Delete only `unified_data_dictionary` under `tools`**

- Open **`tools`**.
- If you see **`unified_data_dictionary`**, select it and delete.  
  If the path is too long and you cannot open or see it, use **Option A** and delete **`tools`** instead.

### 4. Empty the OneDrive Recycle Bin (recommended)

- In OneDrive on the web, open **Recycle bin** (left rail or top).
- Find the `tools` (or `unified_data_dictionary`) you just deleted.
- Select it → **Delete** (or “Delete permanently”) so it is not restored by a recycle-bin sync.

### 5. On your PC: clear the error and resync

- In the OneDrive **“path is too long”** dialog, click **Exit** (or **Try again**; it may fail once more until the client sees the delete).
- **Pause syncing** (tray → **Pause syncing** → **2 hours**), wait **~1 minute**, then **Resume syncing**.
- Or **restart OneDrive:**  
  - Tray → **Exit**; or Task Manager → End **Microsoft OneDrive Sync Service**, **OneDriveFileSyncHelper**, etc.  
  - Run `"C:\Program Files\Microsoft OneDrive\OneDrive.exe"`.
- Wait 5–10 minutes. The error should stop; you should see **“Your files are synced”** or **“Looking for changes”** that finishes without the “path is too long” dialog.

---

## B. Unlink and re-link OneDrive (when `tools` is NOT in the cloud)

If **`tools` does not exist** under `09_Reference\Standards` in OneDrive on the web, the phantom exists **only in your PC's sync database**. Deleting from the web does nothing. You must **rebuild the local sync database** by unlinking and re-linking OneDrive.

### 1. Unlink this PC

1. **OneDrive tray icon** → **Settings** (gear) → **Account**.
2. Click **Unlink this PC**.
3. Confirm. OneDrive will show **"Signing out"** with a spinner—this can take **30 seconds to 2–3 minutes** (longer with a large library). Wait for it to finish; do **not** force-close.
4. OneDrive will stop syncing and close.

Your files stay in the OneDrive folder on disk; they are not deleted. Re-linking will reconnect that folder to the cloud and rebuild the index from the server. Because `tools` is not on the server, it will not be in the new index and the phantom will be gone.

**Shared files:** Unlink and re-link do **not** change sharing. People you've shared with keep access; you do **not** need to re-share or take any action.

### 2. Sign back in and re-select folders

1. **Start OneDrive:** Run `"C:\Program Files\Microsoft OneDrive\OneDrive.exe"` (Win+R; quotes required) or Start → **OneDrive**. On some installs it is in `%LocalAppData%\Microsoft\OneDrive\OneDrive.exe`.
2. **Sign in:** Use your **work account** (e.g. City of Hackensack / `carucci_r@hackensackpd.local`), **not** a personal email. Enter password and complete MFA if prompted.
3. **Set up your OneDrive folder:** When it shows the path (e.g. `C:\Users\carucci_r\OneDrive - City of Hackensack`), **leave it as is** and click **Next**. Do **not** click "Choose location" to change it.
4. **"A OneDrive folder already exists on this PC":** Click **Use this folder**. Do **not** choose "Choose new folder."
5. **"Back up folders on this PC" (Documents, Pictures, Desktop):** This is **optional** and only affects those three Windows folders. Your main OneDrive (SYNC, 09_Reference, etc.) is already set to sync. Turn the toggles **on** if you want those three in OneDrive, or **off** to leave them local; either way, click **Next**.
6. **Choose folders** (if shown): Select the same folders you sync now (or **Sync all**), then **OK**.

### 3. Wait for sync to settle

- OneDrive will show **"Processing X changes"** (e.g. 418,447). With 300+ GB and hundreds of thousands of changes, this can take **many hours** (6–24+). The count goes down as items are processed.
- When done, you'll see **"Your files are synced"** (or **"Looking for changes"** that then finishes). The **"path is too long"** error should **not** return.
- **To check progress:** Click **>** or the "Processing X changes" line for the activity list; **Settings** → **Sync and backup** → **Choose folders** to confirm which folders are selected; check the tray icon (arrows = syncing, cloud+check = synced). Folders in File Explorer may not fully populate until more of the queue is processed.
- If the error appears again, the item may exist in the cloud under a path we didn't check; try **"Search across the whole organization for 'tools'"** on the web and delete any `tools` or `unified_data_dictionary` you find, then Unlink again if needed.

### 4. Sync speed and power (leaving for the day)

- **Using the PC:** Normal use is fine. Heavy disk or network use can slow sync; leaving the PC idle (e.g. overnight) helps it finish sooner.
- **Lock (Win+L):** Sync **continues** when the PC is locked. **Sleep** or **Hibernate** **pauses** sync until you wake it.
- **For overnight sync:** When **plugged in**, set **Make my device sleep after: Never** (Settings → System → Power & battery / Power & sleep). Set **Power button** and **Sleep button** to **Do Nothing** so an accidental press doesn't put the PC to sleep.

### 5. If the tray icon is missing when you need to Unlink

- **Task Manager** → **Processes** → **Microsoft OneDrive** (under Apps or Background) → **End task** to close the app.
- Run `"C:\Program Files\Microsoft OneDrive\OneDrive.exe"` to start it again so you can open **Settings** → **Account** → **Unlink this PC**.

---

## If you need to keep other content under `Standards\tools`

If `tools` contains something you need (other than the recursive `unified_data_dictionary`):

1. In OneDrive on the web, open **`tools`** and try to open **`unified_data_dictionary`**.
2. If you can, delete only **`unified_data_dictionary`**.
3. If the path is too long to navigate, you must delete the whole **`tools`** folder. Copy any needed files from `tools` to another folder (e.g. under `Standards`) **before** deleting `tools`.

---

## After this fix

- **A (delete from web):** The phantom is removed from the cloud. **B (Unlink/re-link):** The local sync DB is rebuilt from the server; if `tools` is not on the server, the phantom is gone from the new index.
- The “path is too long” error for this item should not return.
- To avoid creating the same problem again: do not copy `Standards` or `unified_data_dictionary` into `tools\unified_data_dictionary`, and avoid symlinks/junctions under `tools` that create a `Standards\unified_data_dictionary\...` loop.

---

## Related

- `Investigation_09_Reference_UDD_Sync_Break.md` — cause (phantom, recursion), cache reset, sync messages.
- `Fix_OneDrive_Long_Path_Issue_README.md` — `-Repair` for folders that still exist on disk; “Folder already deleted” and Option B (delete from web).
