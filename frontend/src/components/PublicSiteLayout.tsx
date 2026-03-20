/* Copyright (c) Dario Pizzolante */
import { useEffect, useState, type ReactNode } from "react";
import { ArrowRight, CircleUserRound, Mail, Menu, MessageCircleMore, X } from "lucide-react";

import {
  PUBLIC_NAV_LINKS,
  PUBLIC_SECTION_DEFINITIONS,
  getSectionDefinition,
  getSectionKeyForPath,
  type PublicSectionKey,
} from "@/lib/publicSite";

type PublicSiteLayoutProps = {
  children: ReactNode;
};

const DEFAULT_SECTION_KEY: PublicSectionKey = "services";
const STORAGE_KEY = "public-nav-section";

export function PublicSiteLayout({ children }: PublicSiteLayoutProps) {
  const pathname =
    typeof window === "undefined" ? "/" : window.location.pathname.replace(/\/+$/, "") || "/";
  const currentHash = typeof window === "undefined" ? "" : window.location.hash;
  const isHome = pathname === "/";
  const routeSectionKey = getSectionKeyForPath(pathname);
  const [menuOpen, setMenuOpen] = useState(false);
  const [preferredSectionKey, setPreferredSectionKey] = useState<PublicSectionKey>(() => {
    if (typeof window === "undefined") {
      return DEFAULT_SECTION_KEY;
    }

    const stored = window.localStorage.getItem(STORAGE_KEY) as PublicSectionKey | null;
    return stored ?? DEFAULT_SECTION_KEY;
  });

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }

    if (routeSectionKey) {
      setPreferredSectionKey(routeSectionKey);
      window.localStorage.setItem(STORAGE_KEY, routeSectionKey);
    }
  }, [routeSectionKey]);

  const activeSectionKey = routeSectionKey ?? preferredSectionKey;
  const activeSection = getSectionDefinition(activeSectionKey) ?? getSectionDefinition(DEFAULT_SECTION_KEY)!;

  function isActiveLink(href: string) {
    return pathname === href || pathname.startsWith(`${href}/`);
  }

  function isContextItemActive(href: string) {
    const [basePath, hashFragment] = href.split("#");

    if (hashFragment) {
      return pathname === basePath && currentHash === `#${hashFragment}`;
    }

    return pathname === basePath || pathname.startsWith(`${basePath}/`);
  }

  function handleSectionSelect(sectionKey: PublicSectionKey) {
    setPreferredSectionKey(sectionKey);
    setMenuOpen(false);

    if (typeof window !== "undefined") {
      window.localStorage.setItem(STORAGE_KEY, sectionKey);
    }
  }

  function handleDrawerLinkClick(sectionKey: PublicSectionKey) {
    handleSectionSelect(sectionKey);
  }

  return (
    <div className="public-site">
      <header className={`site-header ${isHome ? "site-header--overlay" : ""}`}>
        <div className="site-header__left">
          <button
            aria-controls="public-sections-drawer"
            aria-expanded={menuOpen}
            aria-label={menuOpen ? "Close sections menu" : "Open sections menu"}
            className="section-switcher"
            type="button"
            onClick={() => setMenuOpen((value) => !value)}
          >
            {menuOpen ? <X className="size-5" /> : <Menu className="size-5" />}
          </button>

          <a aria-label="Stratevia home" className="site-brand" href="/">
            <img alt="" className="site-brand__logo" src="/logo_black_cropped.png" />
          </a>
        </div>

        <div className="site-header__center">
          <p className="context-label">{activeSection.label}</p>
          <nav className="context-nav" aria-label={`${activeSection.label} navigation`}>
            {activeSection.items.map((item) => (
              <a
                key={item.id}
                className={isContextItemActive(item.href) ? "is-active" : undefined}
                href={item.href}
              >
                {item.label}
              </a>
            ))}
          </nav>
        </div>

        <div className="site-header__right">
          <nav className="site-nav" aria-label="Public site navigation">
            {PUBLIC_NAV_LINKS.map((link) => (
              <a
                key={link.href}
                className={isActiveLink(link.href) ? "is-active" : undefined}
                href={link.href}
                aria-label={link.label}
                title={link.label}
              >
                {link.label === "About" ? <CircleUserRound className="size-5" /> : null}
                {link.label === "Contact" ? <MessageCircleMore className="size-5" /> : null}
              </a>
            ))}
          </nav>
        </div>
      </header>

      {menuOpen ? (
        <div className="section-drawer-scrim" onClick={() => setMenuOpen(false)}>
          <aside
            aria-label="Public sections menu"
            className="section-drawer"
            id="public-sections-drawer"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="section-drawer__rail">
              <div className="section-drawer__brand">
                <button
                  aria-label="Close sections menu"
                  className="section-switcher section-switcher--drawer"
                  type="button"
                  onClick={() => setMenuOpen(false)}
                >
                  <X className="size-5" />
                </button>
                <img alt="" className="section-drawer__logo" src="/logo_black_cropped.png" />
              </div>

              <nav className="section-family-nav" aria-label="Section families">
                {PUBLIC_SECTION_DEFINITIONS.map((section) => (
                  <a
                    key={section.key}
                    className={section.key === activeSection.key ? "is-active" : undefined}
                    href={section.path}
                    onClick={() => handleDrawerLinkClick(section.key)}
                  >
                    <span>{section.label}</span>
                    <ArrowRight className="size-4" />
                  </a>
                ))}
              </nav>

              <nav className="section-drawer__utility-nav" aria-label="General pages">
                {PUBLIC_NAV_LINKS.map((link) => (
                  <a
                    key={link.href}
                    className={isActiveLink(link.href) ? "is-active" : undefined}
                    href={link.href}
                    onClick={() => setMenuOpen(false)}
                  >
                    {link.label}
                  </a>
                ))}
              </nav>
            </div>

            <div className="section-drawer__panel">
              <div className="section-drawer__intro">
                <p className="site-kicker">{activeSection.label}</p>
                <h2>{activeSection.label}</h2>
                <p>{activeSection.description}</p>
              </div>
              <div className="section-drawer__grid">
                {activeSection.items.map((item) => (
                  <a
                    key={item.id}
                    className="section-drawer__item"
                    href={item.href}
                    onClick={() => handleDrawerLinkClick(activeSection.key)}
                  >
                    <strong>{item.label}</strong>
                    <span>{item.summary}</span>
                  </a>
                ))}
              </div>
            </div>
          </aside>
        </div>
      ) : null}

      <main className="site-main">{children}</main>

      <footer className="site-footer">
        <div className="site-footer__identity">
          <img alt="" className="site-footer__mark" src="/logo_black_cropped.png" />
          <div className="site-footer__copy">
            <p>&copy; 2026 Stratevia - All rights reserved</p>
            <span>Independent advisory for transformation, AI, and technology leadership.</span>
          </div>
        </div>
        <div className="site-footer__links">
          <a className="site-footer__link site-footer__link--linkedin" href="https://www.linkedin.com/in/dariopizzolante" rel="noreferrer" target="_blank">
            <span className="site-footer__linkedin-badge" aria-hidden="true">
              <span>in</span>
            </span>
          </a>
          <a className="site-footer__link site-footer__link--mail" href="mailto:contact@stratevia.eu">
            <Mail className="size-4" />
          </a>
        </div>
      </footer>
    </div>
  );
}
