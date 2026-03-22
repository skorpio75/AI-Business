/* Copyright (c) Dario Pizzolante */
import { useId, useState } from "react";
import { ArrowRight } from "lucide-react";

import { getServicesForPillar, type ServicePillarDefinition, type ServicePillarKey } from "@/lib/publicSite";

type PublicPillarAccordionProps = {
  items: readonly ServicePillarDefinition[];
  defaultExpandedKey?: ServicePillarKey | null;
};

export function PublicPillarAccordion({ items, defaultExpandedKey }: PublicPillarAccordionProps) {
  const [expandedPillar, setExpandedPillar] = useState<ServicePillarKey | null>(defaultExpandedKey ?? items[0]?.key ?? null);
  const accordionId = useId();

  return (
    <div className="pillar-accordion" role="list">
      {items.map((pillar) => (
        <article
          key={pillar.key}
          className={`pillar-accordion__item ${expandedPillar === pillar.key ? "is-open" : ""}`}
          role="listitem"
        >
          <button
            aria-controls={`${accordionId}-panel-${pillar.key}`}
            aria-expanded={expandedPillar === pillar.key}
            className="pillar-accordion__trigger"
            type="button"
            onClick={() => setExpandedPillar((current) => (current === pillar.key ? null : pillar.key))}
          >
            <h3>{pillar.title}</h3>
            <span aria-hidden="true" className="pillar-accordion__icon" />
          </button>
          <div
            className="pillar-accordion__content"
            hidden={expandedPillar !== pillar.key}
            id={`${accordionId}-panel-${pillar.key}`}
          >
            <p className="pillar-accordion__summary">{pillar.servicesSummary}</p>
            <div className="pillar-accordion__services">
              {getServicesForPillar(pillar.key).map((service) => (
                <article key={service.slug} className="service-summary-card service-summary-card--accordion">
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
          </div>
        </article>
      ))}
    </div>
  );
}
