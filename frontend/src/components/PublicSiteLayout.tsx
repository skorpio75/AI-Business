/* Copyright (c) Dario Pizzolante */
import type { ReactNode } from "react";
import { Linkedin, Mail } from "lucide-react";

import { CONTACT_PATH, PUBLIC_NAV_LINKS } from "@/lib/publicSite";

type PublicSiteLayoutProps = {
  children: ReactNode;
};

export function PublicSiteLayout({ children }: PublicSiteLayoutProps) {
  const pathname =
    typeof window === "undefined" ? "/" : window.location.pathname.replace(/\/+$/, "") || "/";
  const isHome = pathname === "/";

  function isActiveLink(href: string) {
    if (href === "/") {
      return pathname === "/";
    }

    return pathname === href || pathname.startsWith(`${href}/`);
  }

  return (
    <div className="public-site">
      <header className={`site-header ${isHome ? "site-header--overlay" : ""}`}>
        <a aria-label="Stratevia home" className="site-brand" href="/">
          <img alt="" className="site-brand__logo" src="/logo_black_cropped.png" />
        </a>
        <div className="site-header__actions">
          <nav className="site-nav" aria-label="Public site navigation">
            {PUBLIC_NAV_LINKS.map((link) => (
              <a
                key={link.href}
                className={`${isActiveLink(link.href) ? "is-active " : ""}${link.href === CONTACT_PATH ? "site-nav__cta" : ""}`.trim()}
                href={link.href}
              >
                {link.label}
              </a>
            ))}
          </nav>
        </div>
      </header>

      <main className="site-main">{children}</main>

      <footer className="site-footer">
        <div className="site-footer__identity">
          <img alt="" className="site-footer__mark" src="/stratevia-logo.png" />
          <div className="site-footer__copy">
            <p>&copy; 2026 Stratevia - All rights reserved</p>
            <span>Independent advisory for transformation, AI, and technology leadership.</span>
          </div>
        </div>
        <div className="site-footer__links">
          <a href="https://www.linkedin.com/in/dariopizzolante" rel="noreferrer" target="_blank">
            <Linkedin className="size-4" />
          </a>
          <a href="mailto:dario.pizzolante@stratevia.eu">
            <Mail className="size-4" />
          </a>
        </div>
      </footer>
    </div>
  );
}
