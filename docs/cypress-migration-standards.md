# Cypress Coding Standards for Accurate Tosca Migration

> Follow these standards when writing (or refactoring) Cypress tests.
> Every rule here directly maps to a higher accuracy confidence level in the Tosca Migrator agent output.

---

## Rule 1 — Always Use `data-testid` Attributes (Critical)

**Why:** `data-testid` maps to Tosca's `TestID` technique — the most stable, intent-clear selector.  
CSS classes and text content change with redesigns; `data-testid` is purely for automation.

```html
<!-- ✅ Good — in your HTML/component -->
<button data-testid="cookie-accept-btn">Accept</button>
<nav data-testid="main-nav">...</nav>
<section data-testid="careers-section">...</section>
```

```typescript
// ✅ Good — in Cypress
cy.get('[data-testid="cookie-accept-btn"]').click();

// ❌ Avoid — text-based selectors break on copy changes
cy.contains('button', 'Accept').click();
```

**Tosca output:**
```xml
<!-- ✅ High confidence — direct TestID technique -->
<ModuleAttribute name="cookieAcceptBtn" technique="TestID" value="cookie-accept-btn" />
```

---

## Rule 2 — Keep POM Getters Simple and Single-Element (Critical)

**Why:** POM getters with `.parent()`, `.children()`, chained `.find()` produce complex XPath that is fragile in Tosca.

```typescript
// ✅ Good — single stable selector
get cookieBanner() { return cy.get('[data-testid="cookie-banner"]'); }

// ⚠️ Acceptable — but use sparingly
get newsArticles() { return cy.get('[data-testid="news-list"] a'); }

// ❌ Avoid — chained traversal creates unmaintainable XPath
get featuredSection() { return cy.contains('h2', 'Featured Stories').parent().children('.card'); }
```

---

## Rule 3 — Avoid Dynamic Selectors in Custom Commands (Critical)

**Why:** `cy.contains(selector, runtimeString)` cannot be resolved to a static Tosca `ModuleAttribute` and becomes a manual migration item.

```typescript
// ❌ Avoid — runtime string lookup
Cypress.Commands.add('navigateToSection', (name: string) => {
  cy.contains('nav a', name).click();          // → MANUAL MIGRATION ITEM
});

// ✅ Good — split into specific commands or pass a data-testid
Cypress.Commands.add('navigateToWhoWeAre', () => {
  cy.get('[data-testid="nav-who-we-are"]').click();  // → TBox Click, auto-converted
});
```

---

## Rule 4 — Remove Conditional Guards from Custom Commands (High Impact)

**Why:** `if/else` and `.then($body => { if (...) })` patterns cannot be expressed as a Tosca TestStep natively. They become partial migrations requiring Tosca Optional Step or Tosca Script.

```typescript
// ❌ Avoid — conditional guard
Cypress.Commands.add('acceptCookieBanner', () => {
  cy.get('body').then(($body) => {
    if ($body.find('[data-testid="cookie-banner"]').length > 0) {
      cy.get('[data-testid="cookie-accept-btn"]').click();
    }
  });
});

// ✅ Good — set a test precondition that banner always appears,
//           OR split into two commands and call conditionally from the spec
Cypress.Commands.add('acceptCookieBanner', () => {
  cy.get('[data-testid="cookie-accept-btn"]').click();
  // Precondition: cookie banner is always present at test start
});
```

---

## Rule 5 — Use `cy.fixture()` for Test Data (High Impact)

**Why:** Fixtures map cleanly to Tosca `TestConfiguration` parameters, enabling data-driven test cases in Tosca.

```typescript
// ✅ Good — fixture maps to TestConfiguration
cy.fixture('centene-urls').then((data) => {
  cy.visit(data.homepageUrl);
});
```

```json
// cypress/fixtures/centene-urls.json
{
  "homepageUrl": "https://www.centene.com/",
  "newsUrl": "https://www.centene.com/news.html",
  "careersUrl": "https://jobs.centene.com/us/en"
}
```

**Tosca output (auto-converted):**
```xml
<TestConfiguration name="centene-urls">
  <Parameter name="homepageUrl" value="https://www.centene.com/" />
  <Parameter name="newsUrl" value="https://www.centene.com/news.html" />
  <Parameter name="careersUrl" value="https://jobs.centene.com/us/en" />
</TestConfiguration>
```

---

## Rule 6 — Isolate `cy.intercept()` from Test Logic (High Impact)

**Why:** `cy.intercept()` stubs are always Manual Migration Items. If your test logic depends on stubbed responses, the entire test becomes hard to migrate.

```typescript
// ❌ Avoid — intercept mixed into test assertions
it('shows news articles', () => {
  cy.intercept('GET', '**/news/**', { fixture: 'news.json' }).as('news');
  page.visit();
  cy.wait('@news');
  cy.get('[data-testid="news-card"]').should('have.length', 3);
});

// ✅ Good — separate tests that rely on real data from tests that need stubs
// Real environment test (migratable to Tosca):
it('news section renders', () => {
  page.visit();
  cy.get('[data-testid="featured-stories"]').should('be.visible');
});

// Stub test (keep in Cypress, do not migrate to Tosca):
it('[stub] shows empty state when no news', () => {
  cy.intercept('GET', '**/news/**', { body: [] }).as('emptyNews');
  // ... this test is Cypress-only
});
```

---

## Rule 7 — Use Sequential Steps, Not `.then()` Chains (Medium Impact)

**Why:** `.then()` chains with non-trivial callbacks create implicit control flow that cannot map to sequential Tosca TestSteps.

```typescript
// ❌ Avoid — callback chain with logic
cy.get('[data-testid="page-title"]').then(($el) => {
  const title = $el.text();
  cy.get('[data-testid="breadcrumb"]').should('contain', title);
});

// ✅ Good — sequential, each line is a Tosca TestStep
cy.get('[data-testid="page-title"]').should('contain', 'Centene');
cy.get('[data-testid="breadcrumb"]').should('be.visible');
```

---

## Rule 8 — Use `cy.each()` Only for Static Lists (Medium Impact)

**Why:** Dynamic `cy.each()` loops map to Tosca `TBox ForEach` but require a known element count. Static lists can be unrolled into individual TestSteps.

```typescript
// ✅ Acceptable — static list, can be unrolled in Tosca
const navLinks = ['Who We Are', 'Products & Services', 'News'];
navLinks.forEach((link) => {
  cy.get(`[data-testid="nav-${link.toLowerCase().replace(/ /g, '-')}"]`)
    .should('be.visible');
});

// ⚠️ Harder to migrate — dynamic count
cy.get('[data-testid="news-card"]').each(($card) => {
  cy.wrap($card).find('[data-testid="card-title"]').should('be.visible');
});
```

---

## Rule 9 — Name Custom Commands as Atomic Actions (Medium Impact)

**Why:** Commands named after specific actions (`clickAcceptCookies`, `verifyNavLinkVisible`) produce one ActionWord per command in Tosca. Generic commands (`performAction(type, target)`) are manual items.

```typescript
// ✅ Good — atomic, maps to one Tosca ActionWord with a clear purpose
Cypress.Commands.add('verifyFooterLinkExists', (linkTestId: string) => {
  cy.get(`footer [data-testid="${linkTestId}"]`).should('exist');
});

// ❌ Avoid — generic runtime dispatch
Cypress.Commands.add('verifyLink', (selector: string, attr: string, val: string) => {
  cy.get(selector).should('have.attr', attr, val);  // → MANUAL MIGRATION ITEM
});
```

---

## Rule 10 — Use Explicit `cy.url().should(...)` After Navigation (Low Impact)

**Why:** Explicit URL assertions produce `TBox Verify Attribute` on `Browser.URL` in Tosca — fully auto-converted. Implicit navigation without assertion produces no Tosca verification step.

```typescript
// ✅ Good — produces a Tosca URL verification step
cy.get('[data-testid="nav-news"]').click();
cy.url().should('include', '/news');

// ❌ Avoid — no verification, Tosca has nothing to assert
cy.get('[data-testid="nav-news"]').click();
// (test moves on without confirming navigation)
```

---

## Summary — Accuracy Impact per Rule

| Rule | Accuracy Gain | Effort |
|---|---|---|
| 1 — `data-testid` on all elements | +15% (Medium → High) | High (HTML changes needed) |
| 2 — Simple single-element POM getters | +8% | Low |
| 3 — No dynamic selectors in commands | +10% | Medium |
| 4 — No conditional guards | +8% | Medium |
| 5 — `cy.fixture()` for data | +5% | Low |
| 6 — Isolate `cy.intercept()` | +5% | Medium |
| 7 — Sequential steps vs `.then()` chains | +4% | Low |
| 8 — Static `cy.each()` or unroll | +3% | Low |
| 9 — Atomic command naming | +3% | Low |
| 10 — Explicit URL assertions | +2% | Low |
| **All rules applied** | **~63% total gain → ≥ 90% accuracy** | |

> **Baseline without any standards**: ~30–40% auto-conversion  
> **With Rules 1–4 alone**: ~75–80%  
> **With all 10 rules**: **≥ 90% High confidence across all output files**
