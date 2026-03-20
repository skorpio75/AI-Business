/* Copyright (c) Dario Pizzolante */
import { ArrowRight } from "lucide-react";

import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import {
  CONTACT_PATH,
  ENGAGEMENT_FORMATS,
  SERVICES_HERO_REASONS,
  SERVICE_DEFINITIONS,
} from "@/lib/publicSite";

export function PublicServicesPage() {
  return (
    <PublicSiteLayout>
      <section className="page-hero page-hero--light">
        <div className="page-hero__content">
          <a className="back-link back-link--dark" href="/">
            Home
          </a>
          <p className="site-kicker">Services</p>
          <h1>Services for organisations facing change, complexity, or execution pressure.</h1>
          <p className="page-lead page-lead--dark">
            Stratevia works at the intersection of business priorities, technology decisions,
            delivery structure, and practical AI opportunity.
          </p>
        </div>
        <div className="page-hero__panel page-hero__panel--light">
          <strong>Typical reasons clients engage</strong>
          <ul className="detail-list detail-list--dark">
            {SERVICES_HERO_REASONS.map((reason) => (
              <li key={reason}>{reason}</li>
            ))}
          </ul>
        </div>
      </section>

      <section className="page-section page-section--light">
        <div className="service-summary-grid">
          {SERVICE_DEFINITIONS.map((service) => (
            <article key={service.slug} className="service-summary-card">
              <p className="service-summary-card__eyebrow">{service.shortTitle}</p>
              <h2>{service.title}</h2>
              <p>{service.summary}</p>
              <div className="service-summary-card__meta">
                <strong>Best for</strong>
                <span>{service.bestFor.replace(/^Best for /, "")}</span>
              </div>
              <a className="text-link" href={`/services/${service.slug}`}>
                View service
                <ArrowRight className="size-4" />
              </a>
            </article>
          ))}
        </div>
      </section>

      <section className="page-section page-section--light">
        <div className="section-heading">
          <p className="site-kicker">Engagement formats</p>
          <h2>Different ways to bring in senior support.</h2>
        </div>
        <div className="format-grid">
          {ENGAGEMENT_FORMATS.map((format) => (
            <article key={format.title} className="format-card">
              <h3>{format.title}</h3>
              <p>{format.summary}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="page-section page-section--light">
        <article className="cta-band cta-band--compact">
          <div>
            <p className="site-kicker">Contact</p>
            <h2>Not sure which service fits?</h2>
            <p>Start with a short discovery conversation.</p>
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
