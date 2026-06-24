# Cypress to Tosca Migration Report

Project: Centene Homepage Test Suite  
Platform Engine: TBox Web  
Tosca Version: 2025.1.8  
ActionWord Library: Centene  
Migration Date: 2026-06-24

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
| TestCases-centene-homepage-cy.xml | Medium | Global cy.intercept/cy.wait and strict count assertions are manual/approximate |
| TestCases-centene-homepage-feature.xml | Medium | Scenario mapping is clear, but one strict count assertion still needs manual scripting |
| Modules.xml | Medium | Predominantly text-based XPath/CSS selectors without TestID/ID anchors |
| ActionWords.xml | Medium | Conditional guards and dynamic selector resolution require user decisions in Tosca |

## Manual Migration Items

| Item | Source Location | Cypress Pattern | Action Required |
|---|---|---|---|
| 1 | cypress/e2e/centene-homepage.cy.ts (beforeEach) | cy.intercept('GET', '**/centene.com/') + cy.wait('@homepageLoad') | Replace with element-based synchronization in Tosca, e.g. TBox Verify Attribute (logo Exists=True) |
| 2 | cypress/e2e/centene-homepage.cy.ts (beforeEach) | cy.intercept('GET', '**/news/**', { statusCode: 200, body: { articles: [] } }) | Use Tosca Service Virtualization or controlled environment data; do not auto-convert into Tosca XML |
| 3 | cypress/e2e/centene-homepage.cy.ts | should('have.length.greaterThan', 0) | Replace approximation with Tosca Script module if strict list count is required |
| 4 | cypress/e2e/step_definitions/centene-homepage.steps.ts | should('have.length.greaterThan', 0) | Same as Item 3 for feature-driven execution |
| 5 | cypress/support/commands.ts | if/then guard inside acceptCookieBanner / declineCookieBanner | Use Optional Step, Script guard, or enforce precondition that banner exists |
| 6 | cypress/support/commands.ts | cy.contains('nav a', sectionName), cy.contains('a', linkText), cy.contains('h2', sectionHeading) | Replace runtime text lookup with static ModuleAttributes at design time |
| 7 | cypress/pages/CenteneHomePage.ts | navigateTo(section) dynamic linkMap dispatch | Decompose into static nav attributes (navWhoWeAre, navNews, navContact, etc.) in each TestCase |

## Notes

- No cy.stub() usage was found.
- No cy.fixture() usage was found, so TestConfigurations.xml was not generated.
- Selector priority applied for Web: TestID > ID > Name > CSS > XPath. Available source selectors required CSS/XPath in this suite.
