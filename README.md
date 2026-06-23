# AI Cypress → Tosca Migration

> **AI-powered migration** of Cypress E2E tests to Tricentis Tosca format with full Cucumber/Gherkin support.

## 📋 Project Overview

This repository demonstrates an **automated Cypress-to-Tosca migration** for the Centene homepage test suite. It includes:

- ✅ **Source Cypress tests** (spec + Cucumber feature files)
- ✅ **Page Object Model (POM)** with 32 element locators
- ✅ **Custom Cypress commands** (`commands.ts`)
- ✅ **Tosca XML output** ready for import into Tosca Commander
- ✅ **Migration report** with manual action items

---

## 🎯 Use Case

**Target Application:** [Centene Corporation Homepage](https://www.centene.com)  
**Test Scope:** Navigation, hero content, featured stories, careers, investor relations, footer, accessibility  
**Migration Type:** Cypress E2E → Tosca TestCases, Modules, ActionWords  

---

## 🗂️ Repository Structure

```
├── cypress/
│   ├── e2e/
│   │   ├── centene-homepage.cy.ts        # Spec-style tests (29 test cases)
│   │   ├── centene-homepage.feature      # Gherkin BDD tests (15 scenarios)
│   │   └── step_definitions/
│   │       └── centene-homepage.steps.ts # Cucumber step implementations
│   ├── pages/
│   │   └── CenteneHomePage.ts            # Page Object Model (32 getters + 4 methods)
│   └── support/
│       ├── commands.ts                   # 6 custom Cypress commands
│       └── e2e.ts                        # Global configuration
├── tosca-output/
│   ├── Modules.xml                       # 1 Tosca Module with 32 attributes
│   ├── ActionWords.xml                   # 6 Tosca ActionWords
│   ├── TestCases-spec.xml                # 29 TestCases from .cy.ts file
│   ├── TestCases-feature.xml             # 15 TestCases from .feature file
│   └── migration-report.md               # Detailed migration analysis + manual items
├── docs/
│   ├── cypress-migration-standards.md    # Best practices for migration accuracy
│   ├── agent-flow-diagram.html           # Visual workflow of the AI agent
│   └── agent-flow-diagram_v1.html
├── cypress.config.ts                     # Cypress + Cucumber preprocessor config
├── package.json
├── tsconfig.json
└── README.md                             # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** ≥ 18.x
- **npm** ≥ 9.x
- **Cypress** 13.17.0 (installed as devDependency)

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd AI_Cypress_Tosca_Migration

# Install dependencies
npm install
```

### Run Cypress Tests

```bash
# Open Cypress Test Runner (interactive)
npm run cy:open

# Run all E2E tests headlessly
npm run cy:run

# Run spec file only
npm run cy:run:spec

# Run Cucumber feature file only
npm run cy:run:feature
```

---

## 🤖 AI Migration Agent

### What It Does

The **Cypress → Tosca Migrator** agent analyzes Cypress source files and generates Tosca-compatible XML artifacts:

1. **Modules** — POM getters → `ModuleAttribute` definitions (XPath, CSS, TestID techniques)
2. **ActionWords** — Custom commands → reusable Tosca subroutines
3. **TestCases** — `it()` blocks and Gherkin scenarios → Tosca TestSteps

### Key Features

- ✅ **Selector mapping**: `cy.get('[data-testid="btn"]')` → `<ModuleAttribute technique="TestID" value="btn" />`
- ✅ **POM method conversion**: `page.visit()` → `TBox Navigate` + URL parameter
- ✅ **Custom command translation**: `cy.acceptCookieBanner()` → Tosca ActionWord call
- ✅ **Gherkin support**: `Scenario Outline` expansion + `Background` step inlining
- ✅ **API mock detection**: Flags `cy.intercept()` stubs as manual migration items
- ✅ **Conditional logic detection**: Flags `if/else` branches requiring Tosca Script

### Architecture

See [docs/agent-flow-diagram.html](docs/agent-flow-diagram.html) for a visual workflow.

---

## 📦 Migration Output

All generated Tosca XML files are in [`tosca-output/`](tosca-output/):

| File | Content | Import Into |
|------|---------|-------------|
| `Modules.xml` | 1 Module (`CenteneHomePage`)<br>32 ModuleAttributes | Tosca Commander → Modules folder |
| `ActionWords.xml` | 6 ActionWords:<br>• acceptCookieBanner<br>• declineCookieBanner<br>• visitCenteneHome<br>• verifyExternalLink<br>• verifySectionVisible<br>• navigateToSection | Tosca Commander → ActionWords folder |
| `TestCases-spec.xml` | 29 TestCases from `centene-homepage.cy.ts` | Tosca Commander → TestCases folder |
| `TestCases-feature.xml` | 15 TestCases from `centene-homepage.feature` | Tosca Commander → TestCases folder |

**Total:** 44 TestCases ready for execution in Tosca.

---

## ⚠️ Manual Migration Items

The migration report identifies **8 items** requiring manual intervention:

| # | Issue | Resolution |
|---|-------|-----------|
| 1 | `cy.intercept()` + `cy.wait('@homepageLoad')` | Replace with `TBox Verify Attribute` on stable element |
| 2 | News API stub (`cy.intercept` with empty data) | Use Tosca Service Virtualization or stable test environment |
| 3-4 | Conditional cookie banner guards | Use Tosca Optional Step or precondition guarantees |
| 5 | Dynamic navigation dispatch (`linkMap[section]`) | Use specific `navWhoWeAre`, `navCareers`, etc. attributes per TestCase |
| 6-7 | Dynamic text-based lookups (`cy.contains(variable)`) | Substitute runtime variables with static ModuleAttribute names at design time |
| 8 | News article count assertion (`newsArticles.should('have.length.greaterThan', 0)`) | Approximated as `Verify Exists=True`; adjust in Tosca if exact count required |

📄 Full details in [tosca-output/migration-report.md](tosca-output/migration-report.md).

---

## 📖 Cypress Coding Standards

To maximize migration accuracy, follow the guidelines in [docs/cypress-migration-standards.md](docs/cypress-migration-standards.md):

### Key Rules

1. ✅ **Always use `data-testid` attributes** → Maps to Tosca `TestID` technique (most stable)
2. ✅ **Keep POM getters simple** → Single `cy.get()` per getter (no chained `.parent()` traversal)
3. ✅ **Avoid dynamic selectors in custom commands** → `cy.contains(selector, runtimeVar)` cannot map to static Tosca attributes
4. ✅ **Remove conditional guards** → `if/else` requires Tosca Script or Optional Step workarounds
5. ✅ **Use `cy.fixture()` for test data** → Maps cleanly to Tosca `TestConfiguration` parameters

---

## 🔍 Test Coverage

### Source: `centene-homepage.cy.ts` (29 test cases)

- Cookie consent banner (3 tests)
- Top navigation links (5 tests)
- Hero section (3 tests)
- Featured stories (3 tests)
- Serving our members (2 tests)
- Careers section (2 tests)
- Investor relations (2 tests)
- Social media links (2 tests)
- Footer legal links (4 tests)
- Accessibility (2 tests)
- Page title (1 test)

### Source: `centene-homepage.feature` (15 scenarios)

- Cookie consent (2 scenarios)
- Hero section (1 scenario)
- Navigation outline (5 scenarios from 1 `Scenario Outline`)
- News section (1 scenario)
- Members section (1 scenario)
- Careers section (1 scenario)
- Investors section (1 scenario)
- Social media (1 scenario)
- Footer (1 scenario)
- Accessibility (1 scenario)

**Combined:** 44 unique TestCases migrated to Tosca.

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Test Framework** | Cypress | 13.17.0 |
| **BDD Plugin** | @badeball/cypress-cucumber-preprocessor | 21.0.2 |
| **Bundler** | @bahmutov/cypress-esbuild-preprocessor | 2.2.5 |
| **Language** | TypeScript | 5.8.3 |
| **Build Tool** | esbuild | 0.25.5 |
| **Target Platform** | Tricentis Tosca | 14.x+ (XML format) |

---

## 📝 Development Commands

```bash
# Run TypeScript compiler (check types)
npx tsc --noEmit

# Open Cypress interactive mode
npm run cy:open

# Run all tests headlessly
npm run cy:run

# Run specific spec file
npm run cy:run:spec

# Run specific feature file
npm run cy:run:feature
```

---

## 🤝 Contributing

If you discover additional migration patterns or encounter edge cases:

1. Document the issue in `docs/cypress-migration-standards.md`
2. Update the AI agent prompt with the new pattern
3. Regenerate Tosca XML and validate the migration report

---

## 📄 License

This project is **private** and intended for internal demonstration of AI-powered Cypress → Tosca migration capabilities.

---

## 📞 Contact

For questions about the migration process or Tosca import issues, refer to:

- Migration report: [`tosca-output/migration-report.md`](tosca-output/migration-report.md)
- Coding standards: [`docs/cypress-migration-standards.md`](docs/cypress-migration-standards.md)
- Agent architecture: [`docs/agent-flow-diagram.html`](docs/agent-flow-diagram.html)

---

## ✨ Highlights

- **44 TestCases** automatically migrated from Cypress to Tosca
- **32 stable element locators** in the Page Object Model
- **6 reusable ActionWords** for common operations
- **Cucumber/Gherkin support** with Scenario Outline expansion
- **Detailed migration report** with 8 documented manual action items
- **Standards documentation** to improve future migration accuracy

**Ready for import into Tosca Commander.**