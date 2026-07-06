"""
Tosca XML Generator - Alternative to API
Generates Tosca XML files that can be imported into Commander
No special license required - uses standard Tosca import functionality
"""

import json
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any
from xml.dom import minidom

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ToscaXMLGenerator:
    """
    Generates Tosca-compatible XML files from migration.json
    These XML files can be imported using Tosca Commander's built-in Import feature
    """
    
    def __init__(self):
        self.modules = {}
        self.testcases = []
        self.actionwords = []
    
    def generate_from_migration(self, migration_json_path: str, output_folder: str) -> Dict[str, Any]:
        """
        Generate Tosca XML files from migration.json
        
        Args:
            migration_json_path: Path to migration.json file
            output_folder: Folder to save XML files
            
        Returns:
            Dict with generation statistics
        """
        logger.info(f"Loading migration file: {migration_json_path}")
        
        with open(migration_json_path, 'r', encoding='utf-8') as f:
            migration_data = json.load(f)
        
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
        
        stats = {
            "modules_created": 0,
            "testcases_created": 0,
            "actionwords_created": 0,
            "files_generated": []
        }
        
        # Generate Modules XML
        if "pages" in migration_data or "objects" in migration_data:
            module_file = output_path / "Modules.xml"
            self._generate_modules_xml(migration_data, module_file)
            stats["modules_created"] = len(self.modules)
            stats["files_generated"].append(str(module_file))
            logger.info(f"✓ Generated: {module_file}")
        
        # Generate TestCases XML
        if "testCases" in migration_data:
            testcase_file = output_path / "TestCases.xml"
            self._generate_testcases_xml(migration_data, testcase_file)
            stats["testcases_created"] = len(migration_data["testCases"])
            stats["files_generated"].append(str(testcase_file))
            logger.info(f"✓ Generated: {testcase_file}")
        
        # Generate ActionWords XML
        if "actionWords" in migration_data and migration_data["actionWords"]:
            actionword_file = output_path / "ActionWords.xml"
            self._generate_actionwords_xml(migration_data, actionword_file)
            stats["actionwords_created"] = len(migration_data["actionWords"])
            stats["files_generated"].append(str(actionword_file))
            logger.info(f"✓ Generated: {actionword_file}")
        
        # Generate import instructions
        instructions_file = output_path / "IMPORT_INSTRUCTIONS.txt"
        self._generate_import_instructions(instructions_file, stats)
        stats["files_generated"].append(str(instructions_file))
        
        return stats
    
    def _generate_modules_xml(self, migration_data: Dict, output_file: Path):
        """Generate Modules XML file"""
        # Create root element
        root = ET.Element("ToscaObjectModel")
        root.set("Version", "14.0")
        
        # Get objects from migration data
        objects = migration_data.get("objects", [])
        
        if not objects:
            logger.warning("No objects found in migration data")
            return
        
        # Create module
        module = ET.SubElement(root, "Module")
        module_name = migration_data.get("metadata", {}).get("projectName", "CenteneHomePage")
        module.set("Name", module_name)
        module.set("Engine", "TBox Web")
        
        # Add module attributes (controls)
        for obj in objects:
            attr = ET.SubElement(module, "ModuleAttribute")
            attr.set("Name", obj.get("name", obj.get("objectId", "Unknown")))
            
            # Convert selector to proper XPath if needed
            selector = obj.get("selector", "")
            technique = obj.get("technique", "XPath")
            
            # Fix Cypress-style :contains() to proper XPath
            if ":contains(" in selector:
                # Convert button:contains('Accept') to //button[contains(text(),'Accept')]
                selector = self._convert_cypress_selector_to_xpath(selector)
                technique = "XPath"
            
            attr.set("Technique", technique)
            attr.set("Value", selector)
            
            # Add control type if available
            control_type = self._map_control_type(obj.get("name", ""))
            if control_type:
                attr.set("ControlType", control_type)
        
        # Write to file
        self._write_xml(root, output_file)
        logger.info(f"Created module '{module_name}' with {len(objects)} attributes")
    
    def _convert_cypress_selector_to_xpath(self, selector: str) -> str:
        """Convert Cypress-style selectors to proper XPath"""
        import re
        
        # Pattern: element:contains('text')
        pattern = r"([a-zA-Z]+):contains\(['\"]([^'\"]+)['\"]\)"
        match = re.search(pattern, selector)
        
        if match:
            element = match.group(1)
            text = match.group(2)
            return f"//{element}[contains(text(),'{text}')]"
        
        # Pattern: :contains('text') without element
        pattern2 = r":contains\(['\"]([^'\"]+)['\"]\)"
        match2 = re.search(pattern2, selector)
        
        if match2:
            text = match2.group(1)
            return f"//*[contains(text(),'{text}')]"
        
        return selector
    
    def _generate_testcases_xml(self, migration_data: Dict, output_file: Path):
        """Generate TestCases XML file"""
        root = ET.Element("ToscaObjectModel")
        root.set("Version", "14.0")
        
        testcases = migration_data.get("testCases", [])
        
        for tc_data in testcases:
            testcase = ET.SubElement(root, "TestCase")
            testcase.set("Name", tc_data.get("name", "Untitled TestCase"))
            
            # Add test steps
            for step_data in tc_data.get("steps", []):
                step = ET.SubElement(testcase, "TestStep")
                
                action = step_data.get("action", "Unknown")
                tosca_action = self._map_action(action)
                step.set("ActionWord", tosca_action)
                
                # Add parameters
                if "target" in step_data:
                    param = ET.SubElement(step, "Parameter")
                    param.set("Name", "Control")
                    param.set("Value", step_data["target"])
                
                if "value" in step_data:
                    param = ET.SubElement(step, "Parameter")
                    param.set("Name", "Value")
                    param.set("Value", str(step_data["value"]))
                
                if "url" in step_data:
                    param = ET.SubElement(step, "Parameter")
                    param.set("Name", "URL")
                    param.set("Value", step_data["url"])
        
        self._write_xml(root, output_file)
        logger.info(f"Created {len(testcases)} test cases")
    
    def _generate_actionwords_xml(self, migration_data: Dict, output_file: Path):
        """Generate ActionWords XML file"""
        root = ET.Element("ToscaObjectModel")
        root.set("Version", "14.0")
        
        actionwords = migration_data.get("actionWords", [])
        
        for aw_data in actionwords:
            actionword = ET.SubElement(root, "ActionWord")
            actionword.set("Name", aw_data.get("name", "Untitled ActionWord"))
            
            # Add parameters
            for param_data in aw_data.get("parameters", []):
                param = ET.SubElement(actionword, "Parameter")
                param.set("Name", param_data.get("name", "param"))
                param.set("Type", param_data.get("type", "String"))
        
        self._write_xml(root, output_file)
        logger.info(f"Created {len(actionwords)} action words")
    
    def _map_action(self, generic_action: str) -> str:
        """Map generic action to Tosca ActionWord"""
        action_map = {
            "Navigate": "TBox Navigate",
            "Click": "TBox Click",
            "Input": "TBox Enter Text",
            "Verify": "TBox Verify Attribute",
            "VerifyText": "TBox Verify Text",
            "Select": "TBox Select",
            "Wait": "TBox Wait",
            "Clear": "TBox Clear Text"
        }
        return action_map.get(generic_action, generic_action)
    
    def _map_control_type(self, name: str) -> str:
        """Infer control type from name"""
        name_lower = name.lower()
        if "btn" in name_lower or "button" in name_lower:
            return "Button"
        elif "input" in name_lower or "textbox" in name_lower:
            return "TextBox"
        elif "link" in name_lower:
            return "Link"
        elif "dropdown" in name_lower or "select" in name_lower:
            return "ComboBox"
        elif "checkbox" in name_lower:
            return "CheckBox"
        else:
            return "Control"
    
    def _write_xml(self, root: ET.Element, output_file: Path):
        """Write XML to file with pretty formatting"""
        xml_str = ET.tostring(root, encoding='utf-8')
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="  ", encoding='utf-8')
        
        with open(output_file, 'wb') as f:
            f.write(pretty_xml)
    
    def _generate_import_instructions(self, output_file: Path, stats: Dict):
        """Generate import instructions for user"""
        instructions = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                  TOSCA XML IMPORT INSTRUCTIONS                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

Generation Statistics:
  ✓ Modules Created: {stats['modules_created']}
  ✓ TestCases Created: {stats['testcases_created']}
  ✓ ActionWords Created: {stats['actionwords_created']}

Files Generated:
{chr(10).join(f'  • {f}' for f in stats['files_generated'])}

═══════════════════════════════════════════════════════════════════════════════

HOW TO IMPORT INTO TOSCA COMMANDER:

Step 1: Prepare Import Files
  1. Ensure Tosca Commander is OPEN
  2. Navigate to the workspace you want to import into
  
Step 2: Import Modules
  1. In Tosca Commander, go to: PROJECT → Import
  2. Select: "Import from XML"
  3. Browse to: Modules.xml
  4. Choose destination folder: Modules/Migrated/Cypress
  5. Click "Import"
  6. Verify: {stats['modules_created']} module(s) imported successfully

Step 3: Import TestCases
  1. Go to: TESTCASES → Import
  2. Select: "Import from XML"
  3. Browse to: TestCases.xml
  4. Choose destination folder: TestCases/Migrated/Cypress
  5. Click "Import"
  6. Verify: {stats['testcases_created']} test case(s) imported successfully

Step 4: Import ActionWords (if applicable)
  1. Go to: TESTCASES → Import
  2. Select: "Import from XML"
  3. Browse to: ActionWords.xml
  4. Choose destination folder: TestCases/ActionWords
  5. Click "Import"
  6. Verify: {stats['actionwords_created']} action word(s) imported successfully

═══════════════════════════════════════════════════════════════════════════════

ALTERNATIVE IMPORT METHOD:

If XML import doesn't work, use Tosca's built-in Excel import:

  1. Open: TOOLS → Import → From Excel
  2. Use the provided Excel templates in: tosca-output/excel/
  3. Follow the Tosca Excel Import Wizard

═══════════════════════════════════════════════════════════════════════════════

TROUBLESHOOTING:

Issue: "Invalid XML format"
  → Solution: Check Tosca version compatibility (generated for v14.0+)
  → Try: TOOLS → Options → Import/Export → Enable "Legacy XML Mode"

Issue: "Module not found"
  → Solution: Import Modules BEFORE TestCases
  → TestCases reference Modules, so order matters

Issue: "Duplicate names"
  → Solution: Rename existing items in Tosca or use "Merge" option during import

═══════════════════════════════════════════════════════════════════════════════

NEXT STEPS AFTER IMPORT:

  1. ✓ Verify all modules appear in: Modules/Migrated/Cypress
  2. ✓ Verify all test cases appear in: TestCases/Migrated/Cypress
  3. ✓ Open a test case and verify steps are correct
  4. ✓ Run a smoke test (1-2 test cases) to verify functionality
  5. ✓ Address any manual items flagged in validation-report.json
  6. ✓ Execute full test suite

═══════════════════════════════════════════════════════════════════════════════

For support, refer to:
  • docs/TOSCA_API_SETUP.md
  • output/validation-report.json
  • output/build-report.json

═══════════════════════════════════════════════════════════════════════════════
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(instructions)


def main():
    """Command-line interface for Tosca XML Generator"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Tosca XML files from migration.json")
    parser.add_argument("migration_json", help="Path to migration.json file")
    parser.add_argument("--output", help="Output folder for XML files", default="tosca-output/xml")
    
    args = parser.parse_args()
    
    generator = ToscaXMLGenerator()
    stats = generator.generate_from_migration(args.migration_json, args.output)
    
    print("\n" + "="*80)
    print("✅ XML GENERATION COMPLETE")
    print("="*80)
    print(f"\nModules Created: {stats['modules_created']}")
    print(f"TestCases Created: {stats['testcases_created']}")
    print(f"ActionWords Created: {stats['actionwords_created']}")
    print(f"\nFiles Generated:")
    for file in stats['files_generated']:
        print(f"  • {file}")
    print("\n" + "="*80)
    print("Next: Read IMPORT_INSTRUCTIONS.txt for import steps")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
