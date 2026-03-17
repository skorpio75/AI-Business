/* Copyright (c) Dario Pizzolante */
import type { ReactNode } from "react";

import { PUBLIC_NAV_LINKS } from "@/lib/publicSite";

type PublicSiteLayoutProps = {
  children: ReactNode;
};

export function PublicSiteLayout({ children }: PublicSiteLayoutProps) {
  return (
    <div className="public-site">
      <header className="site-header">
        <a className="site-brand" href="/">
          <span className="site-brand__mark">S</span>
          <span>
            <strong>Stratevia</strong>
            <small>AI, transformation, and technology advisory</small>
          </span>
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
        <p>Stratevia, independent advisory for AI, digital transformation, and technology leadership.</p>
      </footer>
    </div>
  );
}
