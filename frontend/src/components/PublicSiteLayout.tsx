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
        <p>Stratevia, independent advisory for AI, digital transformation, and technology leadership.</p>
      </footer>
    </div>
  );
}
