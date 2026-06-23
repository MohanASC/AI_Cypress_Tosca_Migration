/// <reference types="cypress" />
import { CenteneHomePage } from '../pages/CenteneHomePage';

const page = new CenteneHomePage();

describe('Centene Homepage', () => {

  beforeEach(() => {
    cy.intercept('GET', '**/centene.com/', (req) => {
      req.continue();
    }).as('homepageLoad');

    cy.intercept('GET', '**/news/**', {
      statusCode: 200,
      body: { articles: [] },
    }).as('newsApiStub');

    page.visit();
    cy.wait('@homepageLoad');
  });

  // ── Cookie Banner ──────────────────────────────────────────────
  context('Cookie Consent Banner', () => {
    it('displays the cookie consent banner on first visit', () => {
      page.cookieBanner.should('be.visible');
      page.cookieAcceptBtn.should('be.visible');
      page.cookieDeclineBtn.should('be.visible');
    });

    it('dismisses the banner when user accepts cookies', () => {
      page.acceptCookies();
      page.cookieBanner.should('not.exist');
    });

    it('dismisses the banner when user declines cookies', () => {
      page.declineCookies();
      page.cookieBanner.should('not.exist');
    });
  });

  // ── Navigation ─────────────────────────────────────────────────
  context('Top Navigation', () => {
    beforeEach(() => {
      page.acceptCookies();
    });

    it('displays the Centene logo', () => {
      page.logo.should('be.visible');
    });

    it('navigates to Who We Are page', () => {
      page.navigateTo('whoWeAre');
      cy.url().should('include', '/who-we-are');
    });

    it("navigates to Why We're Different page", () => {
      page.navigateTo('whyDifferent');
      cy.url().should('include', '/why-were-different');
    });

    it('navigates to Products & Services page', () => {
      page.navigateTo('products');
      cy.url().should('include', '/products-and-services');
    });

    it('navigates to News page', () => {
      page.navigateTo('news');
      cy.url().should('include', '/news');
    });

    it('navigates to Contact page', () => {
      page.navigateTo('contact');
      cy.url().should('include', '/contact');
    });
  });

  // ── Hero Section ───────────────────────────────────────────────
  context('Hero Section', () => {
    beforeEach(() => {
      page.acceptCookies();
    });

    it('displays the main heading "This is Centene"', () => {
      page.heroHeading.should('be.visible');
    });

    it('displays the mission tagline', () => {
      page.heroTagline.should('be.visible').and('contain', 'Transforming the health of the communities we serve');
    });

    it('has a working "Who We Are >" link', () => {
      page.whoWeAreLink.should('have.attr', 'href').and('include', '/who-we-are');
    });
  });

  // ── Featured Stories ───────────────────────────────────────────
  context('Featured Stories', () => {
    beforeEach(() => {
      page.acceptCookies();
    });

    it('displays the Featured Stories section', () => {
      page.featuredStoriesSection.should('be.visible');
    });

    it('renders at least one news article link', () => {
      page.newsArticles.should('have.length.greaterThan', 0);
    });

    it('has a "View All News >" link pointing to /news.html', () => {
      page.viewAllNewsLink
        .should('be.visible')
        .and('have.attr', 'href', 'https://www.centene.com/news.html');
    });
  });

  // ── Serving Our Members ────────────────────────────────────────
  context('Serving Our Members Section', () => {
    beforeEach(() => {
      page.acceptCookies();
    });

    it('displays the Serving our Members section', () => {
      page.servingMembersSection.should('be.visible');
    });

    it('has a "Products & Services >" link', () => {
      page.productsServicesLink
        .should('have.attr', 'href')
        .and('include', '/products-and-services');
    });
  });

  // ── Careers ────────────────────────────────────────────────────
  context('Careers Section', () => {
    beforeEach(() => {
      page.acceptCookies();
    });

    it('displays the Careers section', () => {
      page.careersSection.should('be.visible');
    });

    it('"Join our Team" link opens the external careers site', () => {
      page.joinOurTeamLink
        .should('have.attr', 'href', 'https://jobs.centene.com/us/en')
        .and('have.attr', 'target', '_blank');
    });
  });

  // ── Investor Relations ─────────────────────────────────────────
  context('Investor Relations Section', () => {
    beforeEach(() => {
      page.acceptCookies();
    });

    it('displays the Centene Investor Relations section', () => {
      page.investorSection.should('be.visible');
    });

    it('"Visit Investor Site" is an external link', () => {
      page.visitInvestorSiteLink
        .should('have.attr', 'href')
        .and('include', 'investors.centene.com');
    });
  });

  // ── Social Media ───────────────────────────────────────────────
  context('Social Media Links', () => {
    beforeEach(() => {
      page.acceptCookies();
    });

    it('has all four social media links', () => {
      page.linkedInLink.should('exist');
      page.facebookLink.should('exist');
      page.twitterLink.should('exist');
      page.youtubeLink.should('exist');
    });

    it('LinkedIn link has correct href', () => {
      page.linkedInLink.should('have.attr', 'href', 'https://www.linkedin.com/company/centene-corporation');
    });
  });

  // ── Footer ─────────────────────────────────────────────────────
  context('Footer', () => {
    beforeEach(() => {
      page.acceptCookies();
    });

    it('displays copyright notice', () => {
      page.footerCopyright.should('be.visible');
    });

    it('footer has Privacy Policy link', () => {
      page.footerPrivacyPolicy
        .should('be.visible')
        .and('have.attr', 'href')
        .and('include', '/privacy-policy');
    });

    it('footer has Terms & Conditions link', () => {
      page.footerTerms
        .should('be.visible')
        .and('have.attr', 'href')
        .and('include', '/terms-conditions');
    });

    it('footer has Accessibility link', () => {
      page.footerAccessibility
        .should('be.visible')
        .and('have.attr', 'href')
        .and('include', '/accessibility');
    });
  });

  // ── Accessibility ──────────────────────────────────────────────
  context('Accessibility', () => {
    it('"Skip to Main Content" link is present in the DOM', () => {
      page.skipToMainContent.should('exist');
    });

    it('page title contains "Centene"', () => {
      cy.title().should('contain', 'Centene');
    });
  });

});
