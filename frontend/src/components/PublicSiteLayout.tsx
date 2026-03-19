/* Copyright (c) Dario Pizzolante */
import type { ReactNode } from "react";
import { Linkedin } from "lucide-react";

import { PUBLIC_NAV_LINKS } from "@/lib/publicSite";

type PublicSiteLayoutProps = {
  children: ReactNode;
};

export function PublicSiteLayout({ children }: PublicSiteLayoutProps) {
  return (
    <div className="public-site">
      <header className="site-header">
        <a aria-label="Stratevia home" className="site-brand" href="/">
          <img
            alt=""
            className="site-brand__logo"
            src="/stratevia-logo.png"
          />
        </a>
        <nav className="site-nav" aria-label="Public site navigation">
          {PUBLIC_NAV_LINKS.map((link) => (
            <a key={link.href} href={link.href}>
              {link.label}
            </a>
          ))}
        </nav>
      </header>

      <main className="site-main">{children}</main>

      <footer className="site-footer">
        <div className="site-footer__identity">
          <img alt="" className="site-footer__mark" src="/stratevia-logo.png" />
          <div className="site-footer__copy">
            <p>© 2026 Stratevia</p>
            <span>Independent advisory for AI, digital transformation, and technology leadership.</span>
          </div>
        </div>
        <div className="site-footer__links">
          <a href="https://www.linkedin.com/in/dariopizzolante" rel="noreferrer" target="_blank">
            <Linkedin className="size-4" />
            LinkedIn
          </a>
          <a href="mailto:dario.pizzolante@stratevia.eu">dario.pizzolante@stratevia.eu</a>
        </div>
      </footer>
    </div>
  );
}
