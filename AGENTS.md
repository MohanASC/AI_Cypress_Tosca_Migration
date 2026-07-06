# Cypress → Tosca Migration Agents

This project uses a **multi-agent architecture** to achieve enterprise-grade, largely automated Cypress-to-Tosca test migration (85-95% automation).

## Agent Architecture

```
                +----------------------+
                | Cypress Project      |
                | Specs, POM, Support  |
                +----------+-----------+
                           |
                    Agent 1: Analyzer
                           |
                           v
                +----------------------+
                | migration.json       |
                | Canonical IR         |
                +----------+-----------+
                           |
                    Agent 2: Validator
                           |
                           v
                +----------------------+
                | validated-migration  |
                | + validation-report  |
                +----------+-----------+
                           |
                    Agent 3: Tosca Builder
                           |
                           +-----------------------+
                           |                       |
                           v                       v
                  Tosca Commander API      Human Review Workbook
                           |
                           v
                  Tosca Workspace
```

## Available Agents

### 1. Migration Orchestrator (Main Entry Point)

**Agent:** `Cypress → Tosca Migrator`  
**File:** `.github/agents/migration-orchestrator.agent.md`

**Use when:** You want to perform a full migration or coordinate the migration workflow

**Invocation:**
```
@Cypress → Tosca Migrator
Migrate cypress/e2e/login.cy.ts
```

**Responsibilities:**
- Coordinates all three specialized agents
- Manages workflow phases
- Handles quality gates
- Asks for human approval when needed
- Generates final reports

---

### 2. Cypress Analyzer (Phase 1)

**Agent:** `Cypress Analyzer`  
**File:** `.github/agents/cypress-analyzer.agent.md`

**Use when:** You only want to analyze Cypress code and generate migration.json

**Invocation:**
```
@Cypress Analyzer
Analyze cypress/e2e/ and generate migration.json
```

**Responsibilities:**
- Reads Cypress specs, POM, custom commands, features
- Extracts selectors → assigns Object IDs (OBJ001, OBJ002...)
- Maps Cypress commands → generic actions (Navigate, Click, Input...)
- Identifies unsupported patterns (cy.intercept, cy.stub)
- Outputs `migration.json` (canonical intermediate representation)
- **NEVER** thinks about Tosca

**Key Principle:** Understands Cypress only. Stays in its lane.

---

### 3. Migration Validator (Phase 2)

**Agent:** `Migration Validator`  
**File:** `.github/agents/migration-validator.agent.md`

**Use when:** You want to validate migration.json quality and assess risk

**Invocation:**
```
@Migration Validator
Validate output/migration.json
```

**Responsibilities:**
- Reviews migration.json for quality issues
- Detects duplicate selectors
- Identifies broken XPath/CSS syntax
- Flags dynamic selectors (react-id-123, item-456...)
- Assesses flaky patterns (nth-child, positional)
- Calculates risk score (Low/Medium/High/Critical)
- Estimates migration effort (hours)
- Provides prioritized recommendations
- Outputs `validation-report.json`
- **NEVER** generates code or migration artifacts

**Key Principle:** Reviews only. Doesn't fix or create anything.

---

### 4. Tosca Builder (Phase 3)

**Agent:** `Tosca Builder`  
**File:** `.github/agents/tosca-builder.agent.md`

**Use when:** You want to build Tosca workspace from validated-migration.json

**Invocation:**
```
@Tosca Builder
Build Tosca workspace from output/validated-migration.json
Target workspace: C:/Tosca/Workspaces/MyWorkspace.tws
Engine: TBox Web
```

**Responsibilities:**
- Reads validated-migration.json
- Connects to Tosca Commander API
- Creates Modules with ModuleAttributes (controls)
- Creates TestCases with TestSteps
- Creates ActionWords (custom commands)
- Maps generic actions → Tosca ActionWords
- Handles platform-specific engines (Web, Android, iOS, SAP)
- Outputs `build-report.json`
- **NEVER** thinks about Cypress or generates XML

**Key Principle:** Tosca expert only. Uses Commander API, not XML.

---

## Migration Workflow

### Option 1: Full Migration (Recommended)

Invoke the **Migration Orchestrator**:

```
@Cypress → Tosca Migrator
Perform full migration of cypress/e2e/
```

The orchestrator will:
1. ✓ Run Cypress Analyzer → migration.json
2. ✓ Show extraction summary
3. ✓ Run Migration Validator → validation-report.json
4. ⚠️ Show risk assessment → **Ask for your approval**
5. ✓ If approved: Run Tosca Builder → Tosca workspace
6. ✓ Generate final reports

### Option 2: Phase-by-Phase

Run each agent individually for more control:

**Phase 1:**
```
@Cypress Analyzer
Analyze cypress/e2e/
```
→ Review `migration.json`

**Phase 2:**
```
@Migration Validator
Validate output/migration.json
```
→ Review `validation-report.json` → Fix issues if needed

**Phase 3:**
```
@Tosca Builder
Build from output/validated-migration.json
Target: C:/Tosca/Workspaces/MyWorkspace.tws
```
→ Review `build-report.json` → Verify in Tosca Commander

---

## Agent Invocation Examples

### Analyze Specific File
```
@Cypress Analyzer
Analyze cypress/e2e/login.cy.ts
```

### Analyze Entire Folder
```
@Cypress Analyzer
Analyze all Cypress tests in cypress/e2e/
Include POM from cypress/pages/
Include custom commands from cypress/support/commands.ts
```

### Validate with Focus
```
@Migration Validator
Validate migration.json with focus on:
- Dynamic selectors
- cy.intercept usage
- XPath quality
```

### Build with Custom Engine
```
@Tosca Builder
Build workspace from validated-migration.json
Workspace: C:/Tosca/Workspaces/Mobile.tws
Engine: TBox Mobile Android
Folder: Migrated/Cypress
```

### Full Migration with Options
```
@Cypress → Tosca Migrator
Migrate cypress/e2e/
Target: TBox Web
Workspace: C:/Tosca/Workspaces/Web.tws
Auto-approve if risk is Low
```

---

## Output Files

After migration, you'll have:

```
output/
├── migration.json                    # Phase 1: Canonical IR
├── extraction-report.md              # Phase 1: Analysis summary
├── validation-report.json            # Phase 2: Risk assessment
├── validated-migration.json          # Phase 2: Approved for build
├── build-report.json                 # Phase 3: Build statistics
└── tosca-migration-workbook.html     # Interactive review
```

---

## Key Differences from Old Architecture

### ❌ Old Approach
- Single monolithic agent
- Direct XML generation
- No intermediate representation
- Hard to maintain/extend
- ~60-70% automation

### ✅ New Approach
- Three specialized agents + orchestrator
- Canonical JSON (migration.json)
- Tosca Commander API (not XML)
- Clear separation of concerns
- **85-95% automation**

---

## Why This Architecture Works

1. **Separation of Concerns**
   - Each agent has ONE job
   - Cypress expert never thinks about Tosca
   - Tosca expert never thinks about Cypress
   - Validator only reviews, never creates

2. **Canonical Intermediate Representation**
   - `migration.json` is framework-agnostic
   - Can be reused for Playwright, Selenium, etc.
   - Easy to validate and review
   - Version-controllable

3. **Quality Gates**
   - Human approval required after validation
   - Risk assessment before proceeding
   - Clear decision points

4. **API-First**
   - Uses Tosca Commander API directly
   - No XML reverse-engineering
   - Easier to maintain
   - More reliable

5. **Extensible**
   - Add new agents for other frameworks
   - Swap out Tosca Builder for different targets
   - Easy to add validation rules
   - Simple to enhance

---

## Troubleshooting

### Agent Not Found
Make sure agent files exist in `.github/agents/`:
- `migration-orchestrator.agent.md`
- `cypress-analyzer.agent.md`
- `migration-validator.agent.md`
- `tosca-builder.agent.md`

### Migration.json Invalid
Run validator to see specific issues:
```
@Migration Validator
Validate output/migration.json and show detailed errors
```

### Tosca Build Failed
Check build-report.json for errors. Common issues:
- Workspace path incorrect
- Commander API not accessible
- Module name conflicts
- Invalid selector syntax

### Want to Re-run Phase
Just invoke the specific agent again:
```
@Migration Validator
Re-validate after fixes
```

---

## Contributing

To add a new agent:

1. Create `.github/agents/your-agent.agent.md`
2. Define YAML frontmatter:
   ```yaml
   ---
   description: "What the agent does"
   name: "Agent Display Name"
   tools: [read, write, run]
   ---
   ```
3. Write agent instructions
4. Add to this AGENTS.md file
5. Test agent invocation

---

## Support

For issues or questions:
1. Check `output/` folder for detailed reports
2. Review validation-report.json for migration blockers
3. Check build-report.json for Tosca-specific errors
4. Consult agent-specific documentation in `.github/agents/`
