/* Copyright (c) Dario Pizzolante */
import { ArrowRight } from "lucide-react";

import { PublicImageHero } from "@/components/PublicImageHero";
import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import {
  CONTACT_PATH,
  ENGAGEMENT_FORMATS,
  HOME_SERVICE_PILLARS,
  SERVICES_HERO_REASONS,
  SERVICES_PILLAR_SECTIONS,
  getServicesForPillar,
} from "@/lib/publicSite";

export function PublicServicesPage() {
  return (
    <PublicSiteLayout>
      <PublicImageHero
        backHref="/"
        backLabel="Home"
        kicker="Services"
        title="Services for organisations navigating transformation, delivery, and AI."
        lead="Stratevia helps organisations assess change, improve digital operations, and strengthen delivery through senior advisory support."
        panel={
          <>
            <p className="image-hero__panel-eyebrow">Typical reasons clients engage</p>
            <ul className="image-hero__list">
            {SERVICES_HERO_REASONS.map((reason) => (
              <li key={reason}>{reason}</li>
            ))}
            </ul>
          </>
        }
      />

      <section className="page-section page-section--light band-section band-section--soft">
        <div className="band-shell">
          <div className="section-heading section-heading--band">
            <p className="site-kicker">Service pillars</p>
            <h2>3 focused areas of advisory support.</h2>
          </div>
          <div className="pillar-grid">
            {HOME_SERVICE_PILLARS.map((pillar) => (
              <article key={pillar.key} className="pillar-card">
                <h3>{pillar.title}</h3>
                <p>{pillar.summary}</p>
                <a className="text-link" href={pillar.href}>
                  Explore pillar
                  <ArrowRight className="size-4" />
                </a>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="page-section page-section--light band-section">
        <div className="band-shell">
          <div className="section-heading section-heading--band">
            <p className="site-kicker">Detailed services</p>
            <h2>Specialist support grouped under each pillar.</h2>
          </div>
          <div className="service-group-stack">
            {SERVICES_PILLAR_SECTIONS.map((pillar) => (
              <section key={pillar.key} className="service-group-block" id={pillar.key}>
                <div className="service-group-block__header">
                  <p className="site-kicker">Service pillar</p>
                  <h2>{pillar.title}</h2>
                  <p>{pillar.summary}</p>
                </div>
                <div className="service-summary-grid">
                  {getServicesForPillar(pillar.key).map((service) => (
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
            ))}
          </div>
        </div>
      </section>

      <section className="page-section page-section--light band-section band-section--soft">
        <div className="band-shell">
          <div className="section-heading section-heading--band">
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
        </div>
      </section>

      <section className="page-section page-section--light band-section band-section--tint">
        <div className="band-shell">
          <article className="cta-band cta-band--compact band-panel">
            <div>
              <p className="site-kicker">Contact</p>
              <h2>Not sure which service or format fits?</h2>
              <p>Start with a short discovery conversation.</p>
            </div>
            <div className="cta-band__actions">
              <a className="site-button site-button--primary" href={CONTACT_PATH}>
                Book a call
                <ArrowRight className="size-4" />
              </a>
            </div>
          </article>
        </div>
      </section>
    </PublicSiteLayout>
  );
}
