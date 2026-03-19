/* Copyright (c) Dario Pizzolante */
import type { LucideIcon } from "lucide-react";
import { ArrowRight, BriefcaseBusiness, ExternalLink, Sparkles, Workflow } from "lucide-react";

import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import { BOOKING_PATH, SERVICE_DEFINITIONS, type ServiceSlug } from "@/lib/publicSite";

const SERVICE_ICONS: Record<ServiceSlug, LucideIcon> = {
  "ai-strategy-roadmapping": Sparkles,
  "automation-digital-operations": Workflow,
  "fractional-cio/cdo-transformation-advisory": BriefcaseBusiness,
};

export function PublicServicesPage() {
  return (
    <PublicSiteLayout>
      <section className="page-hero">
        <div className="page-hero__content">
          <a className="back-link" href="/">
            Home
          </a>
          <p className="site-kicker">Services</p>
          <h1>Focused support across strategy, automation, and technology leadership.</h1>
          <p className="page-lead">
            Explore the core services designed to help organizations modernize, improve operations,
            and move toward practical AI adoption with clarity.
          </p>
        </div>
        <div className="page-hero__panel">
          <strong>How I work</strong>
          <p>Senior advisory, practical framing, clear next steps, and delivery-minded guidance.</p>
          <a className="site-button site-button--primary" href={BOOKING_PATH}>
            Start a conversation
            <ArrowRight className="size-4" />
          </a>
        </div>
      </section>

      <section className="page-section">
        <div className="service-grid">
          {SERVICE_DEFINITIONS.map((service) => {
            const Icon = SERVICE_ICONS[service.slug];

            return (
              <article key={service.slug} className="service-card service-card--detailed">
                <span className="service-card__icon">
                  <Icon className="size-5" />
                </span>
                <h3>{service.title}</h3>
                <p>{service.summary}</p>
                <div className="service-card__meta">
                  <strong>Typical focus</strong>
                  <span>{service.engagements[0]}</span>
                </div>
                <a className="service-card__link" href={`/services/${service.slug}`}>
                  Open service page
                  <ExternalLink className="size-4" />
                </a>
              </article>
            );
          })}
        </div>
      </section>
    </PublicSiteLayout>
  );
}
