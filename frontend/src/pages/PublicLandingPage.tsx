/* Copyright (c) Dario Pizzolante */
import { ArrowRight } from "lucide-react";

import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import {
  ABOUT_PATH,
  CONTACT_PATH,
  HOME_HERO,
  HOME_SERVICE_PILLARS,
  HOW_I_WORK_STEPS,
  SELECTED_BACKGROUND,
  SELECTED_BACKGROUND_SUMMARY,
  STRATEVIA_PROOF_POINTS,
} from "@/lib/publicSite";

export function PublicLandingPage() {
  return (
    <PublicSiteLayout>
      <section className="site-hero site-hero--home">
        <div className="site-hero__content">
          <p className="site-kicker site-kicker--light">{HOME_HERO.eyebrow}</p>
          <h1>{HOME_HERO.title}</h1>
          <p className="site-hero__lead">{HOME_HERO.summary}</p>
          <div className="site-hero__actions">
            <a className="site-button site-button--primary" href={CONTACT_PATH}>
              Book a call
              <ArrowRight className="size-4" />
            </a>
            <a className="site-button site-button--ghost" href="/services">
              View services
            </a>
          </div>
        </div>

        <aside className="hero-visual-card" aria-label="Stratevia advisory focus">
          <h2>One advisory partner across strategy, technology, and delivery.</h2>
          <ul className="hero-bullet-list">
            {HOME_HERO.focusAreas.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </aside>
      </section>

      <section className="site-section site-section--light">
        <div className="section-heading">
          <p className="site-kicker">What I help with</p>
          <h2>3 focused ways to support change.</h2>
        </div>
        <div className="pillar-grid">
          {HOME_SERVICE_PILLARS.map((pillar) => (
            <article key={pillar.title} className="pillar-card">
              <h3>{pillar.title}</h3>
              <p>{pillar.summary}</p>
              <a className="text-link" href={pillar.href}>
                Learn more
                <ArrowRight className="size-4" />
              </a>
            </article>
          ))}
        </div>
      </section>

      <section className="site-section site-section--light">
        <div className="section-heading">
          <p className="site-kicker">How I work</p>
          <h2>3 clear, pragmatic steps.</h2>
        </div>
        <div className="process-simple-grid">
          {HOW_I_WORK_STEPS.map((step, index) => (
            <article key={step.title} className="process-simple-card">
              <span className="process-simple-card__index">0{index + 1}</span>
              <h3>{step.title}</h3>
              <p>{step.summary}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="site-section site-section--light">
        <div className="section-heading">
          <p className="site-kicker">Why Stratevia</p>
          <h2>Senior, pragmatic, and built for execution.</h2>
        </div>
        <div className="trust-grid">
          {STRATEVIA_PROOF_POINTS.map((point) => (
            <article key={point.title} className="trust-card">
              <h3>{point.title}</h3>
              <p>{point.summary}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="site-section site-section--light">
        <article className="background-strip">
          <div>
            <p className="site-kicker">Selected background</p>
            <h2>Experience across leadership, modernization, and delivery.</h2>
          </div>
          <div className="background-strip__list">
            {SELECTED_BACKGROUND.map((item) => (
              <span key={item}>{item}</span>
            ))}
          </div>
          <p className="background-strip__summary">{SELECTED_BACKGROUND_SUMMARY}</p>
        </article>
      </section>

      <section className="site-section site-section--light">
        <article className="cta-band">
          <div>
            <p className="site-kicker">Contact</p>
            <h2>Need clarity on transformation, AI, or delivery?</h2>
            <p>Start with a focused conversation.</p>
          </div>
          <div className="cta-band__actions">
            <a className="site-button site-button--primary" href={CONTACT_PATH}>
              Book a call
              <ArrowRight className="size-4" />
            </a>
            <a className="site-button site-button--secondary" href={ABOUT_PATH}>
              About Stratevia
            </a>
          </div>
        </article>
      </section>
    </PublicSiteLayout>
  );
}
