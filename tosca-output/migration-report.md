# Cypress → Tosca Migration Report

**Project:** Centene Homepage Test Suite  
**Migration Date:** 2026-06-23  
**Migrated by:** Cypress → Tosca Migrator  

---

## 1. Summary

| Artifact | Source File | Output File | Count |
|---|---|---|---|
| Modules | `cypress/pages/CenteneHomePage.ts` | `tosca-output/Modules.xml` | 1 Module, 32 ModuleAttributes |
| ActionWords | `cypress/support/commands.ts` | `tosca-output/ActionWords.xml` | 6 ActionWords |
| TestCases (spec) | `cypress/e2e/centene-homepage.cy.ts` | `tosca-output/TestCases-spec.xml` | 29 TestCases |
| TestCases (feature) | `cypress/e2e/centene-homepage.feature` | `tosca-output/TestCases-feature.xml` | 15 TestCases |
| **Total TestCases** | — | — | **44** |

---

## 2. Source Inventory

### 2.1 POM Class — `CenteneHomePage`

| Getter / Property | Technique | Selector |
|---|---|---|
| `cookieBanner` | CSS | `[class*='cookie']` |
| `cookieAcceptBtn` | XPath | `//button[contains(text(),'Accept')]` |
| `cookieDeclineBtn` | XPath | `//button[contains(text(),'Decline')]` |
| `skipToMainContent` | XPath | `//a[contains(text(),'Skip to Main Content')]` |
| `navWhoWeAre` | XPath | `//nav//a[contains(text(),'Who We Are')]` |
| `navWhyDifferent` | XPath | `//nav//a[contains(text(),"Why We're Different")]` |
| `navProductsServices` | XPath | `//nav//a[contains(text(),'Products & Services')]` |
| `navCareers` | XPath | `//nav//a[contains(text(),'Careers')]` |
| `navInvestors` | XPath | `//nav//a[contains(text(),'Investors')]` |
| `navNews` | XPath | `//nav//a[contains(text(),'News')]` |
| `navContact` | XPath | `//nav//a[contains(text(),'CONTACT')]` |
| `logo` | CSS | `a[href='/']` |
| `heroHeading` | XPath | `//h1[contains(text(),'This is Centene')]` |
| `heroTagline` | XPath | `//*[contains(text(),'Transforming the health of the communities we serve')]` |
| `whoWeAreLink` | XPath | `//a[contains(text(),'Who We Are >')]` |
| `featuredStoriesSection` | XPath | `//h2[contains(text(),'Featured Stories')]/parent::*` |
| `viewAllNewsLink` | XPath | `//a[contains(text(),'View All News >')]` |
| `newsArticles` | CSS | `[class*='news'] a, [class*='story'] a` |
| `servingMembersSection` | XPath | `//h2[contains(text(),'Serving our Members')]/parent::*` |
| `productsServicesLink` | XPath | `//a[contains(text(),'Products & Services >')]` |
| `careersSection` | XPath | `//h2[contains(text(),'Careers')]/parent::*` |
| `joinOurTeamLink` | XPath | `//a[contains(text(),'Join our Team')]` |
| `investorSection` | XPath | `//h2[contains(text(),'Centene Investor Relations')]/parent::*` |
| `visitInvestorSiteLink` | XPath | `//a[contains(text(),'Visit Investor Site')]` |
| `linkedInLink` | CSS | `a[href*='linkedin.com/company/centene']` |
| `facebookLink` | CSS | `a[href*='facebook.com/CenteneCorporation']` |
| `twitterLink` | CSS | `a[href*='x.com/Centene']` |
| `youtubeLink` | CSS | `a[href*='youtube.com/user/CenteneCorp']` |
| `footerPrivacyPolicy` | XPath | `//footer//a[contains(text(),'PRIVACY POLICY')]` |
| `footerTerms` | XPath | `//footer//a[contains(text(),'TERMS & CONDITIONS')]` |
| `footerAccessibility` | XPath | `//footer//a[contains(text(),'ACCESSIBILITY')]` |
| `footerCopyright` | XPath | `//*[contains(text(),'© Copyright 2026 Centene Corporation')]` |

**POM Methods → Module TestSteps:**

| Method | Tosca Step | Notes |
|---|---|---|
| `visit()` | `TBox Navigate` (URL: https://www.centene.com/) | Full migration |
| `acceptCookies()` | `TBox Click` (cookieAcceptBtn) | Full migration |
| `declineCookies()` | `TBox Click` (cookieDeclineBtn) | Full migration |
| `navigateTo(section)` | — | **Manual Migration Item #5** — dynamic dispatch |

### 2.2 Custom Commands — `commands.ts`

| Command | Parameters | Status |
|---|---|---|
| `acceptCookieBanner` | none | Partial — conditional guard dropped (item #3) |
| `declineCookieBanner` | none | Partial — conditional guard dropped (item #4) |
| `navigateToSection` | `sectionName: string` | Partial — dynamic lookup (item #7) |
| `visitCenteneHome` | none | Full migration |
| `verifyExternalLink` | `linkText, expectedUrl` | Partial — dynamic lookup (item #6) |
| `verifySectionVisible` | `sectionHeading: string` | Partial — dynamic lookup (item #7) |

### 2.3 Spec File `it()` Blocks → TestCases-spec.xml

| ID | Context | Test Name |
|---|---|---|
| TC-SPEC-01 | Cookie Consent Banner | displays the cookie consent banner on first visit |
| TC-SPEC-02 | Cookie Consent Banner | dismisses the banner when user accepts cookies |
| TC-SPEC-03 | Cookie Consent Banner | dismisses the banner when user declines cookies |
| TC-SPEC-04 | Top Navigation | displays the Centene logo |
| TC-SPEC-05 | Top Navigation | navigates to Who We Are page |
| TC-SPEC-06 | Top Navigation | navigates to Why We're Different page |
| TC-SPEC-07 | Top Navigation | navigates to Products and Services page |
| TC-SPEC-08 | Top Navigation | navigates to News page |
| TC-SPEC-09 | Top Navigation | navigates to Contact page |
| TC-SPEC-10 | Hero Section | displays the main heading This is Centene |
| TC-SPEC-11 | Hero Section | displays the mission tagline |
| TC-SPEC-12 | Hero Section | has a working Who We Are forward-link |
| TC-SPEC-13 | Featured Stories | displays the Featured Stories section |
| TC-SPEC-14 | Featured Stories | renders at least one news article link ⚠️ |
| TC-SPEC-15 | Featured Stories | has a View All News link pointing to news.html |
| TC-SPEC-16 | Serving Our Members | displays the Serving our Members section |
| TC-SPEC-17 | Serving Our Members | has a Products and Services forward-link |
| TC-SPEC-18 | Careers | displays the Careers section |
| TC-SPEC-19 | Careers | Join Our Team link opens the external careers site |
| TC-SPEC-20 | Investor Relations | displays the Centene Investor Relations section |
| TC-SPEC-21 | Investor Relations | Visit Investor Site is an external link |
| TC-SPEC-22 | Social Media Links | has all four social media links |
| TC-SPEC-23 | Social Media Links | LinkedIn link has correct href |
| TC-SPEC-24 | Footer | displays copyright notice |
| TC-SPEC-25 | Footer | footer has Privacy Policy link |
| TC-SPEC-26 | Footer | footer has Terms and Conditions link |
| TC-SPEC-27 | Footer | footer has Accessibility link |
| TC-SPEC-28 | Accessibility | Skip to Main Content link is present in the DOM |
| TC-SPEC-29 | Accessibility | page title contains Centene |

> ⚠️ TC-SPEC-14 uses an approximation — see Manual Migration Item #8.

### 2.4 Gherkin Scenarios → TestCases-feature.xml

| ID | Tags | Scenario | Expansion |
|---|---|---|---|
| FTC-01 | @cookie | Visitor accepts the cookie consent banner | 1 TC |
| FTC-02 | @cookie | Visitor declines the cookie consent banner | 1 TC |
| FTC-03 | @hero @smoke | Homepage hero section displays correctly | 1 TC |
| FTC-04–08 | @navigation @smoke | User navigates to main sections via top navigation | **5 TCs** (Outline × 5 examples) |
| FTC-09 | @news | Featured Stories section renders news articles | 1 TC ⚠️ |
| FTC-10 | @members @smoke | Serving Our Members section is accessible | 1 TC |
| FTC-11 | @careers | Careers section links to external jobs site | 1 TC |
| FTC-12 | @investors | Investor Relations section links to investor site | 1 TC |
| FTC-13 | @social | All social media links are present on the homepage | 1 TC |
| FTC-14 | @footer | Footer displays legal links and copyright | 1 TC |
| FTC-15 | @accessibility @smoke | Page meets basic accessibility requirements | 1 TC |

> **Gherkin `Background`:** "Given I navigate to the Centene homepage" is inlined as a `TBox Navigate` step in every TestCase. Tosca has no native Background concept.  
> **Gherkin `Scenario Outline`:** Expanded to individual TestCases. Tosca supports data-driven execution via TestCaseDesign and Parameters, but static expansion is used here for clarity.  
> ⚠️ FTC-09 uses an approximation for the count assertion — see item #8.

---

## 3. Manual Migration Items

These items have **no automatic Tosca equivalent** and require manual resolution before the migrated suite can run correctly.

| # | Item | Source Location | Cypress Pattern | Action Required |
|---|---|---|---|---|
| 1 | Homepage load intercept + wait | `centene-homepage.cy.ts`, global `beforeEach` | `cy.intercept('GET', '**/centene.com/', req => req.continue()).as('homepageLoad')` + `cy.wait('@homepageLoad')` | Remove the pass-through stub. Replace `cy.wait('@homepageLoad')` with a `TBox Verify Attribute` step that waits for a stable page element to appear (e.g., `logo Exists=True`). This serves the same synchronization purpose without network interception. |
| 2 | News API stub | `centene-homepage.cy.ts`, global `beforeEach` | `cy.intercept('GET', '**/news/**', { statusCode: 200, body: { articles: [] } }).as('newsApiStub')` | This stub returns empty article data, causing Featured Stories tests to pass regardless of real API state. **Affects TC-SPEC-13, TC-SPEC-14, TC-SPEC-15 and FTC-09.** Resolution options: (a) Use Tosca's Service Virtualization to mock the API at the infrastructure level, or (b) configure a test environment with controlled, stable news data. Behavior of these four TestCases may differ without the stub. |
| 3 | Conditional cookie accept guard | `commands.ts`, `acceptCookieBanner` | `cy.get('body').then($body => { if ($body.find('[class*="cookie"]').length > 0) { cy.contains('button','Accept').click(); } })` | Tosca does not natively support `if/else` branching in TestSteps. The ActionWord `acceptCookieBanner` is implemented as an unconditional click. Options: (a) Set up test preconditions to guarantee the banner is always visible at the click point; (b) add a Tosca Script module that checks element existence before clicking; (c) use TBox Optional Step (Tosca ≥ 14.x) to mark the click as non-fatal if the element is absent. |
| 4 | Conditional cookie decline guard | `commands.ts`, `declineCookieBanner` | Same pattern as `acceptCookieBanner` | Same resolution options as item #3. |
| 5 | Dynamic navigation dispatch | `CenteneHomePage.ts`, `navigateTo(section)` method | `linkMap[section].click()` — runtime key lookup in a TypeScript object | Tosca requires statically declared ModuleAttributes. The `navigateTo()` method has been decomposed: each caller TestCase references the specific `navWhoWeAre`, `navWhyDifferent`, `navProductsServices`, etc. attribute directly. The `navigateTo` ActionWord is intentionally absent from `ActionWords.xml`; use individual nav attributes per TestCase. |
| 6 | Dynamic external-link lookup | `commands.ts`, `verifyExternalLink` | `cy.contains('a', linkText)` — element resolved at runtime from a string variable | The ActionWord `verifyExternalLink` uses a `{linkElement}` parameter. Callers must substitute this with the actual ModuleAttribute name at design time (e.g., `joinOurTeamLink`, `visitInvestorSiteLink`). Ensure every call site has been updated before import into Tosca Commander. |
| 7 | Dynamic section/nav text lookup | `commands.ts`, `navigateToSection` and `verifySectionVisible` | `cy.contains('nav a', sectionName)` / `cy.contains('h2', sectionHeading)` — both resolved from string variables | Both ActionWords use `{sectionName}` / `{sectionElement}` parameters. Callers must substitute the actual ModuleAttribute name at design time. Mapping table: `Who We Are` → `navWhoWeAre`; `Featured Stories` → `featuredStoriesSection`; `Serving our Members` → `servingMembersSection`; `Careers` → `careersSection`; `Centene Investor Relations` → `investorSection`. |
| 8 | Count assertion (`length.greaterThan`) | `centene-homepage.cy.ts` TC-SPEC-14; `centene-homepage.feature` FTC-09 | `newsArticles.should('have.length.greaterThan', 0)` | No standard Tosca ActionWord supports count assertions. The step is approximated with `TBox Verify Attribute` (`Exists=True`), which confirms at least one DOM element matches the `newsArticles` CSS selector but does not count them. For a strict count validation, implement a Tosca Script module or a custom ActionWord that queries the element count via JavaScript execution. |

---

## 4. Tosca ActionWord Mapping Reference

| Cypress Command | Tosca ActionWord | Notes |
|---|---|---|
| `cy.visit(url)` | `TBox Navigate` | `URL` parameter |
| `cy.get(sel).click()` | `TBox Click` | `Element` parameter |
| `cy.get(sel).type(text)` | `TBox Enter Text` | Not used in this suite |
| `cy.get(sel).should('be.visible')` | `TBox Verify Attribute` | `Attribute=Visible`, `ExpectedValue=True` |
| `cy.get(sel).should('not.exist')` | `TBox Verify Attribute` | `Attribute=Exists`, `ExpectedValue=False` |
| `cy.get(sel).should('exist')` | `TBox Verify Attribute` | `Attribute=Exists`, `ExpectedValue=True` |
| `cy.get(sel).should('contain', text)` | `TBox Verify Text` | `ExpectedText` parameter |
| `cy.get(sel).should('have.attr', attr, val)` | `TBox Verify Attribute` | `Attribute={attr}`, `ExpectedValue={val}` |
| `cy.get(sel).should('have.attr', attr).and('include', val)` | `TBox Verify Attribute` | `Attribute={attr}`, `Operator=Contains`, `ExpectedValue={val}` |
| `cy.url().should('include', path)` | `TBox Verify Attribute` | `module=Browser`, `Attribute=URL`, `Operator=Contains` |
| `cy.title().should('contain', text)` | `TBox Verify Attribute` | `module=Browser`, `Attribute=Title`, `Operator=Contains` |
| `cy.intercept(...)` | **Not migrated** | Manual Migration Items #1 and #2 |
| `cy.wait('@alias')` | **Not migrated** | Tied to intercept; replaced with element-existence wait |
| `cy.screenshot()` | No equivalent | Informational only; Tosca captures screenshots automatically on failure |
| `.scrollIntoView()` | Implicit | `TBox Verify Attribute` scrolls to the element in most Tosca engines |
| `.should('have.length.greaterThan', 0)` | **Approximated** | `TBox Verify Attribute` `Exists=True`; Manual Migration Item #8 |

---

## 5. Patterns With No Direct Tosca Equivalent

| Pattern | Cypress Usage | Tosca Limitation | Recommended Approach |
|---|---|---|---|
| `cy.intercept()` network stubs | Global `beforeEach` in spec | Tosca does not intercept at HTTP layer | Tosca Service Virtualization or controlled test environment |
| `cy.wait('@alias')` | Global `beforeEach` in spec | Depends on intercept alias | Replace with `TBox Verify Attribute` (element existence check) |
| Conditional `if/else` in commands | `acceptCookieBanner`, `declineCookieBanner` | No native branching in TestSteps | Tosca Script module, TBox Optional Step, or deterministic preconditions |
| Dynamic element lookup from string variable | `navigateToSection`, `verifyExternalLink`, `verifySectionVisible` | ModuleAttributes must be statically declared | Resolve to specific attribute names at design time; use separate TestCases per variation |
| Element count assertion | `newsArticles.should('have.length.greaterThan', 0)` | No count ActionWord | Tosca Script module with JavaScript `querySelectorAll().length` check |
| Gherkin `Background` | Feature file | No native Background | Inline setup steps in every TestCase |
| Gherkin `Scenario Outline` | Navigation feature | Tosca supports data-driven via TestCaseDesign | Static expansion used here; optionally convert to a single parameterized TestCase with a data table |

---

## 6. Recommended Next Steps

1. **Resolve item #1** — add a `TBox Verify Attribute` (logo, `Exists=True`) after every `TBox Navigate` step to replace the `cy.wait('@homepageLoad')` synchronization.
2. **Resolve item #2** — engage the test environment team to configure stable news API data, or evaluate Tosca Service Virtualization for the news endpoint.
3. **Resolve items #3–4** — decide on the cookie banner handling strategy (always-present precondition vs. TBox Optional Step).
4. **Resolve items #5–7** — review every calling TestCase to ensure `{sectionName}`, `{linkElement}`, and `{sectionElement}` placeholders have been replaced with concrete ModuleAttribute names before importing into Tosca Commander.
5. **Resolve item #8** — implement a Tosca Script module for the news article count assertion if a strict count check is required.
6. **Spot-check** — after import, run `TC-SPEC-05` (navigates to Who We Are) and `FTC-03` (hero section) against the live `https://www.centene.com/` environment to validate selector accuracy.
7. **Scenario Outline parameterization** — optionally refactor FTC-04 through FTC-08 into a single parameterized Tosca TestCase backed by a data table for easier maintenance.
