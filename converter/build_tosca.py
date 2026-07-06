"""
Tosca Builder - Converts migration.json to Tosca workspace
Uses Commander API instead of XML generation
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from commander_api import ToscaCommanderAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ToscaBuilder:
    """
    Converts validated migration.json to Tosca workspace objects
    using Tosca Commander API
    """
    
    # Action mapping from generic to Tosca-specific
    ACTION_MAP = {
        "Navigate": "TBox Navigate",
        "Click": "TBox Click",
        "Input": "TBox Enter Text",
        "Verify": "TBox Verify Attribute",
        "VerifyText": "TBox Verify Text",
        "Select": "TBox Select",
        "Check": "TBox Check",
        "Uncheck": "TBox Uncheck",
        "Wait": "TBox Wait",
        "Clear": "TBox Clear Text"
    }
    
    def __init__(self, workspace_path: str):
        """
        Initialize Tosca Builder
        
        Args:
            workspace_path: Path to Tosca workspace
        """
        self.api = ToscaCommanderAPI(workspace_path)
        self.created_modules = {}
        self.created_testcases = {}
        
    def build_from_migration(self, migration_json_path: str) -> Dict[str, Any]:
        """
        Build Tosca workspace from migration.json
        
        Args:
            migration_json_path: Path to migration.json file
            
        Returns:
            Build report with statistics and errors
        """
        logger.info(f"Loading migration file: {migration_json_path}")
        
        with open(migration_json_path, 'r', encoding='utf-8') as f:
            migration_data = json.load(f)
            
        if not self.api.connect():
            raise ConnectionError("Failed to connect to Tosca workspace")
            
        try:
            report = {
                "modules_created": 0,
                "testcases_created": 0,
                "actionwords_created": 0,
                "errors": []
            }
            
            # Step 1: Create Modules from Pages
            logger.info("Creating Modules...")
            for page in migration_data.get("pages", []):
                try:
                    self._create_module(page)
                    report["modules_created"] += 1
                except Exception as e:
                    logger.error(f"Failed to create module {page['name']}: {e}")
                    report["errors"].append({
                        "type": "module",
                        "name": page["name"],
                        "error": str(e)
                    })
            
            # Step 2: Create ActionWords from custom commands
            logger.info("Creating ActionWords...")
            for actionword in migration_data.get("actionWords", []):
                try:
                    self._create_actionword(actionword)
                    report["actionwords_created"] += 1
                except Exception as e:
                    logger.error(f"Failed to create actionword {actionword['name']}: {e}")
                    report["errors"].append({
                        "type": "actionword",
                        "name": actionword["name"],
                        "error": str(e)
                    })
            
            # Step 3: Create TestCases
            logger.info("Creating TestCases...")
            for testcase in migration_data.get("testCases", []):
                try:
                    self._create_testcase(testcase)
                    report["testcases_created"] += 1
                except Exception as e:
                    logger.error(f"Failed to create testcase {testcase['name']}: {e}")
                    report["errors"].append({
                        "type": "testcase",
                        "name": testcase["name"],
                        "error": str(e)
                    })
            
            # Step 4: Save workspace
            logger.info("Saving Tosca workspace...")
            self.api.save_workspace()
            
            logger.info(f"Build complete: {report}")
            return report
            
        finally:
            self.api.disconnect()
    
    def _create_module(self, page: Dict) -> None:
        """Create a Tosca Module from a Page object"""
        module = self.api.create_module(
            name=page["name"],
            engine="TBox Web",  # TODO: Make this configurable
            folder="Modules/Migrated"
        )
        
        self.created_modules[page["name"]] = module
        
        # Create ModuleAttributes for each control
        for control in page.get("controls", []):
            self.api.create_module_attribute(
                module=module,
                name=control["name"],
                technique=control["selectorType"],
                value=control["selector"],
                control_type=control.get("controlType")
            )
    
    def _create_actionword(self, actionword: Dict) -> None:
        """Create a custom ActionWord"""
        parameters = [
            {"name": p["name"], "type": p.get("type", "String")}
            for p in actionword.get("parameters", [])
        ]
        
        steps = [
            self._map_step_to_tosca(step)
            for step in actionword.get("steps", [])
        ]
        
        self.api.create_action_word(
            name=actionword["name"],
            parameters=parameters,
            steps=steps
        )
    
    def _create_testcase(self, testcase: Dict) -> None:
        """Create a Tosca TestCase"""
        tc = self.api.create_testcase(
            name=testcase["name"],
            folder="TestCases/Migrated"
        )
        
        self.created_testcases[testcase["name"]] = tc
        
        # Create TestSteps
        for step in testcase.get("steps", []):
            tosca_step = self._map_step_to_tosca(step)
            
            self.api.create_teststep(
                testcase=tc,
                module=tosca_step.get("module"),
                actionword=tosca_step["actionword"],
                parameters=tosca_step.get("parameters", {})
            )
    
    def _map_step_to_tosca(self, step: Dict) -> Dict:
        """
        Map a generic test step to Tosca-specific format
        
        Args:
            step: Generic step from migration.json
            
        Returns:
            Tosca-specific step configuration
        """
        action = step["action"]
        tosca_actionword = self.ACTION_MAP.get(action, action)
        
        tosca_step = {
            "actionword": tosca_actionword,
            "parameters": {}
        }
        
        # Map target to module
        if "target" in step:
            # Look up module by object ID
            tosca_step["module"] = self._get_module_for_object(step["target"])
            tosca_step["parameters"]["Element"] = step["target"]
        
        # Map action-specific parameters
        if action == "Navigate":
            tosca_step["parameters"]["URL"] = step.get("url", "")
        elif action == "Input":
            tosca_step["parameters"]["Value"] = step.get("value", "")
        elif action in ["Verify", "VerifyText"]:
            tosca_step["parameters"]["Expected"] = step.get("value", "")
        elif action == "Wait":
            tosca_step["parameters"]["Milliseconds"] = step.get("value", "1000")
        
        return tosca_step
    
    def _get_module_for_object(self, object_id: str) -> str:
        """
        Find the module that contains a given object ID
        
        Args:
            object_id: Object identifier (e.g., OBJ001)
            
        Returns:
            Module name
        """
        # TODO: Implement proper object-to-module mapping
        # This requires tracking which module each object belongs to
        return "UnknownModule"


def main():
    """Command-line interface for Tosca Builder"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build Tosca workspace from migration.json")
    parser.add_argument("migration_json", help="Path to migration.json file")
    parser.add_argument("workspace", help="Path to Tosca workspace")
    parser.add_argument("--output", help="Output path for build report", default="build-report.json")
    parser.add_argument("--use-api", action="store_true", help="Use real Tosca Commander API (requires pythonnet)")
    parser.add_argument("--username", help="Tosca workspace username (if required)")
    parser.add_argument("--password", help="Tosca workspace password (if required)")
    
    args = parser.parse_args()
    
    # Use real API if requested and available
    if args.use_api:
        try:
            from commander_api_real import get_tosca_api
            logger.info("Using real Tosca Commander API")
            api = get_tosca_api(
                args.workspace, 
                use_real_api=True,
                username=args.username,
                password=args.password
            )
            builder = ToscaBuilder(args.workspace)
            builder.api = api
        except Exception as e:
            logger.error(f"Failed to initialize Tosca API: {e}")
            logger.warning("Falling back to simulated mode")
            builder = ToscaBuilder(args.workspace)
    else:
        logger.info("Using simulated mode (no real Tosca API)")
        builder = ToscaBuilder(args.workspace)
    
    report = builder.build_from_migration(args.migration_json)
    
    # Save report
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"Build report saved to: {args.output}")
    print(f"Modules created: {report['modules_created']}")
    print(f"TestCases created: {report['testcases_created']}")
    print(f"ActionWords created: {report['actionwords_created']}")
    print(f"Errors: {len(report['errors'])}")


if __name__ == "__main__":
    main()
