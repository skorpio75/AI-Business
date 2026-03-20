/* Copyright (c) Dario Pizzolante */
import { ArrowRight } from "lucide-react";

import { PublicImageHero } from "@/components/PublicImageHero";
import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import { CONTACT_PATH, type ServiceDefinition } from "@/lib/publicSite";

type PublicServiceDetailPageProps = {
  service: ServiceDefinition;
};

export function PublicServiceDetailPage({ service }: PublicServiceDetailPageProps) {
  return (
    <PublicSiteLayout>
      <PublicImageHero
        backHref="/services"
        backLabel="All services"
        kicker={service.shortTitle}
        title={service.title}
        lead={service.tagline}
        body={
          <>
            <p>{service.intro}</p>
            <p className="image-hero__accent-copy">{service.bestFor}</p>
          </>
        }
        panel={
          <>
            <p className="image-hero__panel-eyebrow">What this service brings</p>
            <p className="image-hero__panel-summary">{service.summary}</p>
            <ul className="image-hero__list">
            {service.proofPoints.map((item) => (
              <li key={item}>{item}</li>
            ))}
            </ul>
          </>
        }
      />

      <section className="page-section page-section--light page-section--service-detail">
        <article className="detail-card detail-card--light">
          <p className="detail-card__eyebrow detail-card__eyebrow--dark">The challenge</p>
          <h2>Common situations where this service helps</h2>
          <ul className="detail-list detail-list--dark">
            {service.clientProblems.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>

        <article className="detail-card detail-card--light">
          <p className="detail-card__eyebrow detail-card__eyebrow--dark">What this engagement delivers</p>
          <h2>Clear outcomes you can work with</h2>
          <ul className="detail-list detail-list--dark">
            {service.outcomes.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>

        <article className="detail-card detail-card--light">
          <p className="detail-card__eyebrow detail-card__eyebrow--dark">Typical engagement</p>
          <h2>How support is usually structured</h2>
          <ul className="detail-list detail-list--dark">
            {service.engagements.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>

        <article className="detail-card detail-card--light">
          <p className="detail-card__eyebrow detail-card__eyebrow--dark">Best fit</p>
          <h2>Who this is for</h2>
          <ul className="detail-list detail-list--dark">
            {service.fit.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>
      </section>

      <section className="page-section page-section--light">
        <article className="cta-band cta-band--compact">
          <div>
            <p className="site-kicker">Contact</p>
            <h2>Want to see if this is the right fit?</h2>
            <p>Book a first conversation.</p>
          </div>
          <div className="cta-band__actions">
            <a className="site-button site-button--primary" href={CONTACT_PATH}>
              Book a call
              <ArrowRight className="size-4" />
            </a>
          </div>
        </article>
      </section>
    </PublicSiteLayout>
  );
}
