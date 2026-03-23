/* Copyright (c) Dario Pizzolante */
import { ArrowRight } from "lucide-react";

import { PublicPillarAccordion } from "@/components/PublicPillarAccordion";
import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import {
  ABOUT_PATH,
  CONTACT_PATH,
  HOME_HERO,
  SERVICE_PILLARS,
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
          <h2>From assessment to execution support.</h2>
          <ul className="hero-bullet-list">
            {HOME_HERO.focusAreas.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </aside>
      </section>

      <section className="site-section site-section--light band-section band-section--soft">
        <div className="band-shell">
          <div className="section-heading section-heading--band">
            <p className="site-kicker">What I help with</p>
            <h2>3 focused ways to move transformation forward</h2>
          </div>
          <PublicPillarAccordion items={SERVICE_PILLARS} />
        </div>
      </section>

      <section className="site-section site-section--light band-section">
        <div className="band-shell">
          <div className="section-heading section-heading--band">
            <p className="site-kicker">How I work</p>
            <h2>3 clear steps from diagnosis to delivery</h2>
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
        </div>
      </section>

      <section className="site-section site-section--light band-section band-section--tint">
        <div className="band-shell">
          <div className="section-heading section-heading--band">
            <p className="site-kicker">Why Stratevia</p>
            <h2>Senior advisory with practical execution discipline</h2>
          </div>
          <div className="trust-grid">
            {STRATEVIA_PROOF_POINTS.map((point) => (
              <article key={point.title} className="trust-card">
                <h3>{point.title}</h3>
                <p>{point.summary}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="site-section site-section--light band-section">
        <div className="band-shell">
          <article className="background-strip band-panel">
            <div>
              <p className="site-kicker">Selected background</p>
              <h2>Experience across leadership, modernization, and delivery</h2>
            </div>
            <div className="background-strip__list">
              {SELECTED_BACKGROUND.map((item) => (
                <span key={item}>{item}</span>
              ))}
            </div>
            <p className="background-strip__summary">{SELECTED_BACKGROUND_SUMMARY}</p>
          </article>
        </div>
      </section>

      <section className="site-section site-section--light band-section band-section--soft">
        <div className="band-shell">
          <article className="cta-band band-panel">
            <div>
              <p className="site-kicker">Contact</p>
              <h2>Need clarity on priorities, delivery, or AI adoption?</h2>
              <p>Start with a focused conversation to assess fit and next steps</p>
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
        </div>
      </section>
    </PublicSiteLayout>
  );
}
