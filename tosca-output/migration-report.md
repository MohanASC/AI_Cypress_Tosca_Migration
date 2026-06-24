# Cypress to Tosca Migration Report

Project: Centene Homepage Test Suite  
Platform Engine: TBox Web  
Tosca Version: 2025.1.8  
ActionWord Library: Centene  
Migration Date: 2026-06-24  
Format: Direct Import (PascalCase, ToscaExport wrapper)

## Summary Counts

| Artifact | Output File | Count |
|---|---|---|
| TestCases (spec) | TestCases-centene-homepage-cy.xml | 29 |
| TestCases (feature) | TestCases-centene-homepage-feature.xml | 15 |
| Total TestCases | - | 44 |
| Modules | Modules.xml | 1 |
| ModuleAttributes | Modules.xml | 32 |
| ActionWords | ActionWords.xml | 6 |
| TestConfigurations | - | 0 (no cy.fixture usage found) |

## Accuracy Confidence

| Output File | Confidence | Reason |
|---|---|---|
| TestCases-centene-homepage-cy.xml | High | Direct mapping with standard TBox Web actions; intercept/wait handled via manual items |
| TestCases-centene-homepage-feature.xml | High | Clear Gherkin scenario mapping with proper Background expansion |
| Modules.xml | High | Static selectors with clear CSS/XPath patterns |
| ActionWords.xml | High | Direct mapping of custom commands with proper parameters |

## XML Format Compliance

All XML files adhere to Tosca direct-import format:
- **PascalCase attributes**: Name=, Module=, ActionWord=, Technique=, Value=, Parameter=, Element=, Attribute=, ExpectedValue=, Operator=
- **ToscaExport wrapper**: All content wrapped in `<ToscaExport>` root element
- **Proper container elements**: `<Modules>`, `<TestCases>`, `<ActionWords>` with child containers `<ModuleAttributes>`, `<TestSteps>`, `<Parameters>`
- **XML declaration**: `<?xml version="1.0" encoding="UTF-8"?>`
- **Generation metadata**: Source file, platform, date, accuracy in XML comments

## Manual Migration Items

| Item | Source Location | Cypress Pattern | Action Required |
|---|---|---|---|
| 1 | cypress/e2e/centene-homepage.cy.ts (beforeEach) | cy.intercept('GET', '**/centene.com/') + cy.wait('@homepageLoad') | Replace with element-based synchronization in Tosca, e.g. TBox Verify Attribute (logo Exists=True) |
| 2 | cypress/e2e/centene-homepage.cy.ts (beforeEach) | cy.intercept('GET', '**/news/**', { statusCode: 200, body: { articles: [] } }) | Use Tosca Service Virtualization or controlled environment data; do not auto-convert into Tosca XML |
| 3 | cypress/e2e/centene-homepage.cy.ts | should('have.length.greaterThan', 0) | Count assertion simplified to Exists check; use Tosca Script module if strict count required |
| 4 | cypress/e2e/step_definitions/centene-homepage.steps.ts | should('have.length.greaterThan', 0) | Same as Item 3 for feature-driven execution |
| 5 | cypress/support/commands.ts | if/then guard inside acceptCookieBanner / declineCookieBanner | Conditional logic preserved via sequential exists check before click; mark Optional in Tosca if needed |

## Selector Strategy

All selectors follow Web platform priority:
1. `data-testid` attributes (not available in source)
2. `id` attributes (limited availability)
3. `name` attributes (limited availability)
4. Stable CSS selectors with `href` attributes
5. XPath with `contains(text(),...)` for text-based elements (last resort)

## Notes

- No cy.stub() usage was found.
- No cy.fixture() usage was found, so TestConfigurations.xml was not generated.
- All BeforeEach hooks properly expanded inline in each TestCase.
- Scenario Outline expanded into 5 separate TestCases (FTC-04 through FTC-08).
- Background steps from Gherkin feature properly inlined in each scenario.
- Custom commands mapped to reusable ActionWords with proper parameter passing.
