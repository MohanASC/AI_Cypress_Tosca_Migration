/// <reference types="cypress" />

/**
 * Page Object Model — Centene Homepage
 * URL: https://www.centene.com/
 */
export class CenteneHomePage {
  readonly url = 'https://www.centene.com/';

  // ── Cookie Banner ──────────────────────────────────────────────
  get cookieBanner()       { return cy.get('[class*="cookie"]').first(); }
  get cookieAcceptBtn()    { return cy.contains('button', 'Accept'); }
  get cookieDeclineBtn()   { return cy.contains('button', 'Decline'); }

  // ── Navigation ─────────────────────────────────────────────────
  get skipToMainContent()  { return cy.contains('a', 'Skip to Main Content'); }
  get navWhoWeAre()        { return cy.contains('nav a', 'Who We Are'); }
  get navWhyDifferent()    { return cy.contains('nav a', "Why We're Different"); }
  get navProductsServices(){ return cy.contains('nav a', 'Products & Services'); }
  get navCareers()         { return cy.contains('nav a', 'Careers'); }
  get navInvestors()       { return cy.contains('nav a', 'Investors'); }
  get navNews()            { return cy.contains('nav a', 'News'); }
  get navContact()         { return cy.contains('nav a', 'CONTACT'); }
  get logo()               { return cy.get('a[href="/"]').first(); }

  // ── Hero Section ───────────────────────────────────────────────
  get heroHeading()        { return cy.contains('h1', 'This is Centene'); }
  get heroTagline()        { return cy.contains('Transforming the health of the communities we serve'); }
  get whoWeAreLink()       { return cy.contains('a', 'Who We Are >'); }

  // ── Featured Stories ───────────────────────────────────────────
  get featuredStoriesSection() { return cy.contains('h2', 'Featured Stories').parent(); }
  get viewAllNewsLink()    { return cy.contains('a', 'View All News >'); }
  get newsArticles()       { return cy.get('[class*="news"] a, [class*="story"] a'); }

  // ── Serving Our Members ────────────────────────────────────────
  get servingMembersSection()  { return cy.contains('h2', 'Serving our Members').parent(); }
  get productsServicesLink()   { return cy.contains('a', 'Products & Services >'); }

  // ── Careers ────────────────────────────────────────────────────
  get careersSection()     { return cy.contains('h2', 'Careers').parent(); }
  get joinOurTeamLink()    { return cy.contains('a', 'Join our Team'); }

  // ── Investor Relations ─────────────────────────────────────────
  get investorSection()    { return cy.contains('h2', 'Centene Investor Relations').parent(); }
  get visitInvestorSiteLink() { return cy.contains('a', 'Visit Investor Site'); }

  // ── Social Media ───────────────────────────────────────────────
  get linkedInLink()       { return cy.get('a[href*="linkedin.com/company/centene"]'); }
  get facebookLink()       { return cy.get('a[href*="facebook.com/CenteneCorporation"]'); }
  get twitterLink()        { return cy.get('a[href*="x.com/Centene"]'); }
  get youtubeLink()        { return cy.get('a[href*="youtube.com/user/CenteneCorp"]'); }

  // ── Footer ─────────────────────────────────────────────────────
  get footerPrivacyPolicy()  { return cy.contains('footer a', 'PRIVACY POLICY'); }
  get footerTerms()          { return cy.contains('footer a', 'TERMS & CONDITIONS'); }
  get footerAccessibility()  { return cy.contains('footer a', 'ACCESSIBILITY'); }
  get footerCopyright()      { return cy.contains('© Copyright 2026 Centene Corporation'); }

  // ── Actions ────────────────────────────────────────────────────
  visit() {
    cy.visit(this.url);
  }

  acceptCookies() {
    this.cookieAcceptBtn.click();
  }

  declineCookies() {
    this.cookieDeclineBtn.click();
  }

  navigateTo(section: 'whoWeAre' | 'whyDifferent' | 'products' | 'careers' | 'investors' | 'news' | 'contact') {
    const linkMap = {
      whoWeAre:     this.navWhoWeAre,
      whyDifferent: this.navWhyDifferent,
      products:     this.navProductsServices,
      careers:      this.navCareers,
      investors:    this.navInvestors,
      news:         this.navNews,
      contact:      this.navContact,
    };
    linkMap[section].click();
  }
}
