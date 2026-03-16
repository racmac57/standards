# Quick Guide: Getting Claude Code Review

**Date**: 2026-01-16  
**Purpose**: How to get Claude AI to review the migration plan

---

## ⚡ Quick Steps

### 1. Open Claude Code
Start a new conversation in Claude Code (not this session - get fresh eyes)

### 2. Copy the Prompt
Open: `docs/merge/CLAUDE-CODE-PROMPT.md`  
Copy the entire contents

### 3. Paste and Send
Paste into Claude Code and send

### 4. Let Claude Read Files
Claude will ask to read specific files. Say yes to all Priority 1-3 files.

### 5. Answer Context Questions
Claude may ask:
- Do you use UDD CLI? (Yes/No)
- Do you sync with GitHub? (Yes/No)
- Any custom scripts using UDD? (Yes/No)

### 6. Get Review
Claude will provide structured review with risk assessment and recommendations.

---

## 📋 Files Claude Will Need

Claude will ask to read these files (in order):

**Must Read:**
1. `docs/merge/05-UDD-Hybrid-Migration-REVISED.md` (the plan)
2. `unified_data_dictionary/pyproject.toml` (package config)
3. `unified_data_dictionary/src/cli.py` (main code)
4. `unified_data_dictionary/README.md` (UDD overview)

**Should Read:**
5. `unified_data_dictionary/config.yaml`
6. `unified_data_dictionary/src/*.py` (other Python files)
7. `.claude/settings.local.json` (context)

**Nice to Have:**
8. Directory listings
9. Import analysis
10. Path dependency searches

---

## 🎯 What Claude Will Check

✅ Python package integrity  
✅ Path dependencies  
✅ Import statements  
✅ Configuration files  
✅ Test suite impact  
✅ Missing coverage  
✅ Risk assessment  
✅ Alternative approaches  

---

## 📊 Expected Output

Claude will provide:

1. **Executive Summary**
   - Safe/Risky/Needs Changes
   - Key concerns
   - Go/No-Go recommendation

2. **Detailed Analysis**
   - Each area: PASS/FAIL/WARNING
   - Specific issues found
   - Recommended fixes

3. **Risk Assessment**
   - High/Medium/Low risks listed
   - Impact analysis

4. **Recommendations**
   - Pre-migration actions
   - Script modifications
   - Post-migration tasks
   - Alternative approaches

---

## 💡 Pro Tips

**Before Asking:**
- Run the analysis scripts in CLAUDE-REVIEW-PACKAGE.md
- Have recent git status ready
- Know if UDD tool currently works

**During Review:**
- Be ready to answer context questions
- Provide additional files if Claude asks
- Ask follow-up questions about concerns

**After Review:**
- Save Claude's output
- Update migration plan based on findings
- Address high-risk items before executing

---

## 🔍 Additional Context Files

If Claude asks for more context, provide:

**Python Analysis:**
```powershell
# Search for path references
Get-ChildItem unified_data_dictionary\src\*.py -Recurse | 
    Select-String "os.path|Path\(|__file__|\.\./"
```

**Import Analysis:**
```powershell
# Find all imports
Get-ChildItem unified_data_dictionary\src\*.py -Recurse |
    Select-String "^import |^from "
```

**Directory Structure:**
```powershell
# Current structure
Get-ChildItem unified_data_dictionary -Directory -Recurse -Name
```

---

## ⚠️ Key Questions for Claude

Make sure Claude answers:

1. **Will `pip install -e .` work from tools/unified_data_dictionary/?**
2. **Are there hardcoded paths that will break?**
3. **Will tests still run?**
4. **Is the standards_paths.ini approach sound?**
5. **What are we missing?**

---

## 📁 Files Created for You

All in `docs/merge/`:

- **CLAUDE-CODE-PROMPT.md** ← Copy this entire file to Claude
- **CLAUDE-REVIEW-PACKAGE.md** ← Reference guide for what to provide
- **05-UDD-Hybrid-Migration-REVISED.md** ← The plan being reviewed
- **APPROACH-COMPARISON.md** ← Why hybrid approach

---

## 🚀 Next Steps After Review

1. Review Claude's findings
2. Address high-risk issues
3. Update migration plan if needed
4. Re-run analysis if major changes
5. Execute migration when confident

---

**Ready to start?**

1. Open Claude Code (new session)
2. Open `docs/merge/CLAUDE-CODE-PROMPT.md`
3. Copy all contents
4. Paste to Claude Code
5. Let Claude analyze

**Estimated review time: 15-30 minutes**

---

**Created**: 2026-01-16  
**Purpose**: Quick reference for getting external review  
**Status**: Ready to use
