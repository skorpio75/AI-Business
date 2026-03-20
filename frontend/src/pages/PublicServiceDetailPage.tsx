/* Copyright (c) Dario Pizzolante */
import { ArrowRight } from "lucide-react";

import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import { CONTACT_PATH, type ServiceDefinition } from "@/lib/publicSite";

type PublicServiceDetailPageProps = {
  service: ServiceDefinition;
};

export function PublicServiceDetailPage({ service }: PublicServiceDetailPageProps) {
  return (
    <PublicSiteLayout>
      <section className="page-hero page-hero--light">
        <div className="page-hero__content">
          <a className="back-link back-link--dark" href="/services">
            All services
          </a>
          <p className="site-kicker">{service.shortTitle}</p>
          <h1>{service.title}</h1>
          <p className="page-lead page-lead--dark">{service.tagline}</p>
          <p className="page-copy page-copy--dark">{service.intro}</p>
          <p className="page-copy page-copy--dark page-copy--accent">{service.bestFor}</p>
        </div>
        <div className="page-hero__panel page-hero__panel--light">
          <strong>What this service brings</strong>
          <p>{service.summary}</p>
          <ul className="detail-list detail-list--dark">
            {service.proofPoints.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      </section>

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
