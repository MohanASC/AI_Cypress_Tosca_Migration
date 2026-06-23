/// <reference types="cypress" />
import {
  Given,
  When,
  Then,
} from '@badeball/cypress-cucumber-preprocessor';
import { CenteneHomePage } from '../../pages/CenteneHomePage';

const page = new CenteneHomePage();

// ── Background ────────────────────────────────────────────────────────────────
Given('I navigate to the Centene homepage', () => {
  page.visit();
});

Given('I have accepted the cookie banner', () => {
  cy.acceptCookieBanner();
});

// ── Cookie Banner ─────────────────────────────────────────────────────────────
Then('the cookie consent banner is displayed', () => {
  page.cookieBanner.should('be.visible');
});

When('I accept the cookie banner', () => {
  page.cookieAcceptBtn.click();
});

When('I decline the cookie banner', () => {
  page.cookieDeclineBtn.click();
});

Then('the cookie consent banner is no longer visible', () => {
  page.cookieBanner.should('not.exist');
});

// ── Hero Section ──────────────────────────────────────────────────────────────
Then('the page heading {string} is visible', (heading: string) => {
  cy.contains('h1', heading).should('be.visible');
});

Then('the tagline {string} is visible', (tagline: string) => {
  cy.contains(tagline).should('be.visible');
});

Then('the {string} link is present', (linkText: string) => {
  cy.contains('a', linkText).should('exist');
});

// ── Navigation ────────────────────────────────────────────────────────────────
When('I click the {string} navigation link', (navLink: string) => {
  cy.contains('nav a', navLink).click();
});

Then('the URL contains {string}', (urlPath: string) => {
  cy.url().should('include', urlPath);
});

// ── Sections ──────────────────────────────────────────────────────────────────
Then('the {string} section is visible', (sectionHeading: string) => {
  cy.contains('h2', sectionHeading).scrollIntoView().should('be.visible');
});

Then('at least one news article link is displayed', () => {
  cy.get('[class*="news"] a, [class*="story"] a').should('have.length.greaterThan', 0);
});

Then(
  'the {string} link points to {string}',
  (linkText: string, expectedHref: string) => {
    cy.contains('a', linkText)
      .should('have.attr', 'href', expectedHref);
  }
);

Then(
  'the {string} link is present and points to the products page',
  (linkText: string) => {
    cy.contains('a', linkText)
      .should('have.attr', 'href')
      .and('include', '/products-and-services');
  }
);

// ── External Links ────────────────────────────────────────────────────────────
Then(
  'the {string} link opens {string} in a new tab',
  (linkText: string, expectedHref: string) => {
    cy.contains('a', linkText)
      .should('have.attr', 'href', expectedHref)
      .and('have.attr', 'target', '_blank');
  }
);

Then(
  'the {string} link opens an external URL containing {string}',
  (linkText: string, urlFragment: string) => {
    cy.contains('a', linkText)
      .should('have.attr', 'href')
      .and('include', urlFragment);
  }
);

// ── Social Media ──────────────────────────────────────────────────────────────
Then('the LinkedIn link points to {string}', (href: string) => {
  cy.get(`a[href="${href}"]`).should('exist');
});

Then('the Facebook link points to {string}', (href: string) => {
  cy.get(`a[href="${href}"]`).should('exist');
});

Then('the X (Twitter) link points to {string}', (href: string) => {
  cy.get(`a[href="${href}"]`).should('exist');
});

Then('the YouTube link points to {string}', (href: string) => {
  cy.get(`a[href="${href}"]`).should('exist');
});

// ── Footer ────────────────────────────────────────────────────────────────────
Then('the footer displays {string}', (text: string) => {
  cy.contains(text).should('be.visible');
});

Then(
  'the {string} footer link points to a URL containing {string}',
  (linkText: string, urlFragment: string) => {
    cy.contains('footer a', linkText)
      .should('have.attr', 'href')
      .and('include', urlFragment);
  }
);

// ── Accessibility ─────────────────────────────────────────────────────────────
Then('the {string} link is present in the DOM', (linkText: string) => {
  cy.contains('a', linkText).should('exist');
});

Then('the page title contains {string}', (titleFragment: string) => {
  cy.title().should('contain', titleFragment);
});
