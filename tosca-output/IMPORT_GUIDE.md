# 📋 TOSCA COMMANDER IMPORT GUIDE

## ✅ Updated XML Files Generated (with proper XPath)

The XML files have been regenerated with correct XPath syntax compatible with Tosca.

---

## 🎯 HOW TO IMPORT INTO TOSCA COMMANDER

### Option 1: Using File Menu (Recommended)

1. **Open Tosca Commander**
2. **Open your workspace**: `AI_Centene` (the one shown in your screenshot)
3. Click **File** menu (top left)
4. Select **Import...**
5. Choose **"Import XModule or XTestCase from file"**
6. Browse to: `C:\Users\RMo380\OneDrive - ascendion\Documents\REPO\CYPRESS\AI_Cypress_Tosca_Migration\tosca-output\xml\Modules.xml`
7. Click **Open**

### Option 2: Using HOME Tab

1. Click the **HOME** tab (you can see it in your screenshot)
2. Look for **"Create"** section in the ribbon
3. Click **"Create Folder"** dropdown arrow
4. Select **"Import"**
5. Choose **"From XML file"**

### Option 3: Right-Click Context Menu

1. In the left panel, navigate to **"Modules"** section
2. Right-click on **"Standard module examples"** folder
3. Select **"Import"** or **"Add" → "Import from file"**
4. Browse to the XML file

---

## 🔍 IF YOU DON'T SEE "IMPORT" OPTION

### This usually means:

1. **Tosca Version Too Old**
   - XML import was added in Tosca 11.0+
   - Check your version: **Help** → **About Tosca**
   - If version < 11, you'll need to use **Excel import** instead

2. **Permissions Issue**
   - Your user account may not have import rights
   - Check with your Tosca administrator
   - Try: **Tools** → **Options** → **Security** → check permissions

3. **Wrong Workspace Type**
   - Some workspace types don't support XML import
   - Check if workspace is in "Read-only" mode

---

## 🎯 ALTERNATIVE: Excel Import (Works on ALL Tosca versions)

If XML import isn't available, use Excel import:

### Step 1: Install Excel Import Template

1. In Tosca Commander, go to: **Tools** → **Import**
2. Select **"Import from Excel"**
3. Click **"Download Template"** (if available)

### Step 2: Use Our Generated Excel Files

I can generate Excel files for you that work with Tosca's built-in Excel import.

**Run this command:**
```powershell
cd "c:\Users\RMo380\OneDrive - ascendion\Documents\REPO\CYPRESS\AI_Cypress_Tosca_Migration"
.\.venv\Scripts\Activate.ps1
python converter/generate_tosca_excel.py output/migration.json --output tosca-output/excel
```

### Step 3: Import Excel Files

1. **Tools** → **Import** → **"Import from Excel"**
2. Select: `tosca-output/excel/Modules.xlsx`
3. Follow the wizard
4. Repeat for: `tosca-output/excel/TestCases.xlsx`

---

## 🔧 MANUAL CREATION (If all else fails)

If neither XML nor Excel import works, you can manually create in Tosca:

### Create Module Manually:

1. Right-click **"Modules"** → **"Create Module"**
2. Name: `Centene Homepage Tests`
3. Engine: `TBox Web`
4. Right-click module → **"Add ModuleAttribute"**
5. For each control (32 total), add:
   - Name: (e.g., `cookieBanner`)
   - Technique: `XPath` or `CSS`
   - Value: (from Modules.xml file)

I have all 32 controls listed in the XML file - I can provide them in a simple text format if needed.

---

## 📞 WHAT TO TRY NOW:

### Option A: Find Import in Tosca (Most Likely)

1. Open Tosca Commander
2. Click **File** → **Import...** (or **Tools** → **Import**)
3. Screenshot the menu and show me if you still can't find it

### Option B: Generate Excel Files

Let me know and I'll create Excel files instead of XML

### Option C: Check Tosca Version

1. In Tosca, click **Help** → **About**
2. Tell me your Tosca version number
3. I'll adjust the import method accordingly

---

## ❓ Common Questions

**Q: Where is File menu?**  
A: Top-left corner, same row as PROJECT, HOME, VIEW tabs

**Q: I see "Import" but it's grayed out**  
A: You might not have write permissions on the workspace. Try:
   - Ensure workspace is not open in another instance
   - Check if workspace is in read-only mode
   - Verify you have edit rights

**Q: Import fails with "Invalid format"**  
A: Try Excel import instead - it's more compatible across Tosca versions

---

**Which option would you like to try? Let me know what you see in your Tosca Commander menus!**
