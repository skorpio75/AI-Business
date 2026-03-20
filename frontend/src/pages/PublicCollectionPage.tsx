/* Copyright (c) Dario Pizzolante */
import { ArrowRight } from "lucide-react";

import { PublicImageHero } from "@/components/PublicImageHero";
import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import { CONTACT_PATH, type PublicSectionDefinition } from "@/lib/publicSite";

type PublicCollectionPageProps = {
  section: PublicSectionDefinition;
};

export function PublicCollectionPage({ section }: PublicCollectionPageProps) {
  return (
    <PublicSiteLayout>
      <PublicImageHero
        backHref="/"
        backLabel="Home"
        kicker={section.label}
        title={section.label}
        lead={section.description}
      />

      <section className="page-section page-section--light band-section band-section--soft">
        <div className="band-shell">
          <div className="section-heading section-heading--band">
            <p className="site-kicker">{section.label}</p>
            <h2>Key themes and areas of discussion.</h2>
          </div>
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
        </div>
      </section>
    </PublicSiteLayout>
  );
}
