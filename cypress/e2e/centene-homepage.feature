@centene @homepage
Feature: Centene Homepage
  As a visitor to centene.com
  I want to browse the homepage
  So that I can learn about Centene's mission, services, and career opportunities

  Background:
    Given I navigate to the Centene homepage

  # ── Cookie Banner ──────────────────────────────────────────────
  @cookie
  Scenario: Visitor accepts the cookie consent banner
    Then the cookie consent banner is displayed
    When I accept the cookie banner
    Then the cookie consent banner is no longer visible

  @cookie
  Scenario: Visitor declines the cookie consent banner
    Then the cookie consent banner is displayed
    When I decline the cookie banner
    Then the cookie consent banner is no longer visible

  # ── Hero Section ───────────────────────────────────────────────
  @hero @smoke
  Scenario: Homepage hero section displays correctly
    Given I have accepted the cookie banner
    Then the page heading "This is Centene" is visible
    And the tagline "Transforming the health of the communities we serve, one person at a time" is visible
    And the "Who We Are >" link is present

  # ── Navigation ─────────────────────────────────────────────────
  @navigation @smoke
  Scenario Outline: User navigates to main sections via top navigation
    Given I have accepted the cookie banner
    When I click the "<NavLink>" navigation link
    Then the URL contains "<UrlPath>"

    Examples:
      | NavLink              | UrlPath                  |
      | Who We Are           | /who-we-are              |
      | Why We're Different  | /why-were-different      |
      | Products & Services  | /products-and-services   |
      | News                 | /news                    |
      | CONTACT              | /contact                 |

  # ── Featured Stories ───────────────────────────────────────────
  @news
  Scenario: Featured Stories section renders news articles
    Given I have accepted the cookie banner
    Then the "Featured Stories" section is visible
    And at least one news article link is displayed
    And the "View All News >" link points to "https://www.centene.com/news.html"

  # ── Serving Our Members ────────────────────────────────────────
  @members @smoke
  Scenario: Serving Our Members section is accessible
    Given I have accepted the cookie banner
    Then the "Serving our Members" section is visible
    And the "Products & Services >" link is present and points to the products page

  # ── Careers ────────────────────────────────────────────────────
  @careers
  Scenario: Careers section links to external jobs site
    Given I have accepted the cookie banner
    Then the "Careers" section is visible
    And the "Join our Team" link opens "https://jobs.centene.com/us/en" in a new tab

  # ── Investor Relations ─────────────────────────────────────────
  @investors
  Scenario: Investor Relations section links to investor site
    Given I have accepted the cookie banner
    Then the "Centene Investor Relations" section is visible
    And the "Visit Investor Site" link opens an external URL containing "investors.centene.com"

  # ── Social Media ───────────────────────────────────────────────
  @social
  Scenario: All social media links are present on the homepage
    Given I have accepted the cookie banner
    Then the LinkedIn link points to "https://www.linkedin.com/company/centene-corporation"
    And the Facebook link points to "https://www.facebook.com/CenteneCorporation"
    And the X (Twitter) link points to "https://x.com/Centene"
    And the YouTube link points to "https://www.youtube.com/user/CenteneCorp"

  # ── Footer ─────────────────────────────────────────────────────
  @footer
  Scenario: Footer displays legal links and copyright
    Given I have accepted the cookie banner
    Then the footer displays "© Copyright 2026 Centene Corporation"
    And the "PRIVACY POLICY" footer link points to a URL containing "/privacy-policy"
    And the "TERMS & CONDITIONS" footer link points to a URL containing "/terms-conditions"
    And the "ACCESSIBILITY" footer link points to a URL containing "/accessibility"

  # ── Accessibility ──────────────────────────────────────────────
  @accessibility @smoke
  Scenario: Page meets basic accessibility requirements
    Then the "Skip to Main Content" link is present in the DOM
    And the page title contains "Centene"
