/* Copyright (c) Dario Pizzolante */
import { ArrowRight } from "lucide-react";

import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import { BOOKING_PATH, type ServiceDefinition } from "@/lib/publicSite";

type PublicServiceDetailPageProps = {
  service: ServiceDefinition;
};

export function PublicServiceDetailPage({ service }: PublicServiceDetailPageProps) {
  return (
    <PublicSiteLayout>
      <section className="page-hero">
        <div className="page-hero__content">
          <a className="back-link" href="/services">
            All services
          </a>
          <p className="site-kicker">{service.shortTitle}</p>
          <h1>{service.title}</h1>
          <p className="page-lead">{service.tagline}</p>
          <p className="page-copy">{service.intro}</p>
        </div>
        <div className="page-hero__panel">
          <strong>What this service brings</strong>
          <p>{service.summary}</p>
          <a className="site-button site-button--primary" href={BOOKING_PATH}>
            Book a first conversation
            <ArrowRight className="size-4" />
          </a>
        </div>
      </section>

      <section className="page-section page-section--service">
        <article className="detail-card">
          <p className="detail-card__eyebrow">Outcomes</p>
          <h2>What you can expect</h2>
          <ul className="detail-list">
            {service.outcomes.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>

        <article className="detail-card">
          <p className="detail-card__eyebrow">Typical engagement</p>
          <h2>How support is usually structured</h2>
          <ul className="detail-list">
            {service.engagements.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>

        <article className="detail-card">
          <p className="detail-card__eyebrow">Best fit</p>
          <h2>Who this is for</h2>
          <ul className="detail-list">
            {service.fit.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>
      </section>
    </PublicSiteLayout>
  );
}
