/// <reference types="cypress" />

/**
 * Custom Cypress Commands — Centene
 * `export {}` makes this a module so `declare global` augmentation is valid.
 */
export {};

// ── Type Declarations (must precede Cypress.Commands.add calls) ──
declare global {
  namespace Cypress {
    interface Chainable {
      acceptCookieBanner(): void;
      declineCookieBanner(): void;
      navigateToSection(sectionName: string): void;
      visitCenteneHome(): void;
      verifyExternalLink(linkText: string, expectedUrl: string): void;
      verifySectionVisible(sectionHeading: string): void;
    }
  }
}

// ── Cookie Handling ─────────────────────────────────────────────
Cypress.Commands.add('acceptCookieBanner', () => {
  cy.get('body').then(($body) => {
    if ($body.find('[class*="cookie"]').length > 0) {
      cy.contains('button', 'Accept').click();
    }
  });
});

Cypress.Commands.add('declineCookieBanner', () => {
  cy.get('body').then(($body) => {
    if ($body.find('[class*="cookie"]').length > 0) {
      cy.contains('button', 'Decline').click();
    }
  });
});

// ── Navigation ──────────────────────────────────────────────────
Cypress.Commands.add('navigateToSection', (sectionName: string) => {
  cy.contains('nav a', sectionName).click();
});

// ── Centene Homepage Setup ───────────────────────────────────────
Cypress.Commands.add('visitCenteneHome', () => {
  cy.visit('https://www.centene.com/');
  cy.acceptCookieBanner();
});

// ── Verify External Link ─────────────────────────────────────────
Cypress.Commands.add('verifyExternalLink', (linkText: string, expectedUrl: string) => {
  cy.contains('a', linkText)
    .should('have.attr', 'href', expectedUrl)
    .and('have.attr', 'target', '_blank');
});

// ── Verify Section Visible ───────────────────────────────────────
Cypress.Commands.add('verifySectionVisible', (sectionHeading: string) => {
  cy.contains('h2', sectionHeading)
    .scrollIntoView()
    .should('be.visible');
});
