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
