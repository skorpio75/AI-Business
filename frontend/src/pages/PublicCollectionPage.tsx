/* Copyright (c) Dario Pizzolante */
import { ArrowRight } from "lucide-react";

import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import { CONTACT_PATH, type PublicSectionDefinition } from "@/lib/publicSite";

type PublicCollectionPageProps = {
  section: PublicSectionDefinition;
};

export function PublicCollectionPage({ section }: PublicCollectionPageProps) {
  return (
    <PublicSiteLayout>
      <section className="page-hero page-hero--light">
        <div className="page-hero__content">
          <a className="back-link back-link--dark" href="/">
            Home
          </a>
          <p className="site-kicker">{section.label}</p>
          <h1>{section.label}</h1>
          <p className="page-lead page-lead--dark">{section.description}</p>
        </div>
      </section>

      <section className="page-section page-section--light">
        <div className="service-summary-grid">
          {section.items.map((item) => (
            <article key={item.id} className="service-summary-card" id={item.id}>
              <p className="service-summary-card__eyebrow">{section.shortLabel}</p>
              <h2>{item.label}</h2>
              <p>{item.summary}</p>
              <a className="text-link" href={CONTACT_PATH}>
                Discuss this area
                <ArrowRight className="size-4" />
              </a>
            </article>
          ))}
        </div>
      </section>
    </PublicSiteLayout>
  );
}
