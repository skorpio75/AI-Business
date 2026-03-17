/* Copyright (c) Dario Pizzolante */
import { ArrowRight } from "lucide-react";

import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import {
  ABOUT_FACTS,
  ABOUT_SUMMARY,
  BOOKING_PATH,
  CAREER_MILESTONES,
  EXPERIENCE_PILLS,
  PROGRAMME_HIGHLIGHTS,
} from "@/lib/publicSite";

export function PublicAboutPage() {
  return (
    <PublicSiteLayout>
      <section className="page-hero page-hero--about">
        <div className="page-hero__content">
          <a className="back-link" href="/">
            Home
          </a>
          <p className="site-kicker">About</p>
          <h1>Dario Pizzolante</h1>
          <p className="page-lead">
            IT leadership, modernization, and AI-enabled business transformation.
          </p>
          {ABOUT_SUMMARY.map((paragraph) => (
            <p key={paragraph} className="page-copy">
              {paragraph}
            </p>
          ))}
        </div>
        <div className="page-hero__panel page-hero__panel--portrait">
          <div className="about-portrait-wrap">
            <img alt="Portrait of Dario Pizzolante" className="about-portrait" src="/dario-pizzolante.jpg" />
          </div>
          <a className="site-button site-button--primary" href={BOOKING_PATH}>
            Book a first conversation
            <ArrowRight className="size-4" />
          </a>
        </div>
      </section>

      <section className="page-section page-section--about-grid">
        <article className="detail-card">
          <p className="detail-card__eyebrow">Experience</p>
          <h2>Core focus areas</h2>
          <div className="experience-pill-list experience-pill-list--roomy">
            {EXPERIENCE_PILLS.map((pill) => (
              <span key={pill} className="experience-pill experience-pill--panel">
                {pill}
              </span>
            ))}
          </div>
        </article>

        <article className="detail-card">
          <p className="detail-card__eyebrow">Strengths</p>
          <h2>How that experience translates into client value</h2>
          <ul className="detail-list">
            {ABOUT_FACTS.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>
      </section>

      <section className="page-section">
        <article className="detail-card detail-card--wide">
          <p className="detail-card__eyebrow">Selected programmes</p>
          <h2>Representative leadership and transformation work</h2>
          <div className="highlight-grid">
            {PROGRAMME_HIGHLIGHTS.map((item) => (
              <article key={item.org} className="highlight-card">
                <strong>{item.org}</strong>
                <p>{item.summary}</p>
              </article>
            ))}
          </div>
        </article>
      </section>

      <section className="page-section">
        <article className="detail-card detail-card--wide">
          <p className="detail-card__eyebrow">Career path</p>
          <h2>Selected milestones</h2>
          <div className="timeline-list">
            {CAREER_MILESTONES.map((item) => (
              <article key={`${item.role}-${item.period}`} className="timeline-card">
                <div className="timeline-card__top">
                  <strong>{item.role}</strong>
                  <span>{item.period}</span>
                </div>
                <p>{item.summary}</p>
              </article>
            ))}
          </div>
        </article>
      </section>
    </PublicSiteLayout>
  );
}
