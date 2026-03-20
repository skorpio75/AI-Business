/* Copyright (c) Dario Pizzolante */
import { ArrowRight } from "lucide-react";

import { PublicImageHero } from "@/components/PublicImageHero";
import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import {
  ABOUT_LEAD,
  ABOUT_SUMMARY,
  ACADEMIC_EDUCATION,
  ABOUT_CORE_STRENGTHS,
  CONTACT_PATH,
  REPRESENTATIVE_EXPERIENCE,
  SELECTED_CREDENTIALS,
} from "@/lib/publicSite";

export function PublicAboutPage() {
  return (
    <PublicSiteLayout>
      <PublicImageHero
        backHref="/"
        backLabel="Home"
        kicker="About"
        title="Dario Pizzolante"
        lead={ABOUT_LEAD}
        actions={
          <>
            <a className="site-button site-button--primary" href={CONTACT_PATH}>
              Book a call
              <ArrowRight className="size-4" />
            </a>
          </>
        }
      />

      <section className="page-section page-section--light">
        <article className="detail-card detail-card--light about-background-card">
          <div className="about-background-card__media">
            <div className="image-hero__portrait-wrap">
              <img alt="Portrait of Dario Pizzolante" className="image-hero__portrait" src="/dario-pizzolante.jpg" />
            </div>
          </div>
          <div className="about-background-card__content">
            <p className="detail-card__eyebrow detail-card__eyebrow--dark">Representative background</p>
            <h2>Senior support across leadership, transformation, and practical delivery.</h2>
            <ul className="detail-list detail-list--dark">
              {ABOUT_CORE_STRENGTHS.map((item) => (
                <li key={item.title}>{item.title}</li>
              ))}
            </ul>
          </div>
        </article>
      </section>

      <section className="page-section page-section--light">
        <article className="content-block">
          <p className="site-kicker">Professional summary</p>
          <div className="content-block__copy">
            {ABOUT_SUMMARY.map((paragraph) => (
              <p key={paragraph}>{paragraph}</p>
            ))}
          </div>
        </article>
      </section>

      <section className="page-section page-section--light">
        <div className="section-heading">
          <p className="site-kicker">Core strengths</p>
          <h2>Senior support grounded in structure and execution.</h2>
        </div>
        <div className="trust-grid">
          {ABOUT_CORE_STRENGTHS.map((item) => (
            <article key={item.title} className="trust-card">
              <h3>{item.title}</h3>
              <p>{item.summary}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="page-section page-section--light">
        <div className="section-heading">
          <p className="site-kicker">Representative experience</p>
          <h2>Selected roles and environments.</h2>
        </div>
        <div className="experience-grid">
          {REPRESENTATIVE_EXPERIENCE.map((item) => (
            <article key={item.organization} className="experience-card">
              <p className="experience-card__org">{item.organization}</p>
              <h3>{item.role}</h3>
              <p>{item.summary}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="page-section page-section--light page-section--credentials">
        <article className="detail-card detail-card--light">
          <p className="detail-card__eyebrow detail-card__eyebrow--dark">Education</p>
          <h2>Academic background</h2>
          <div className="timeline-list timeline-list--light">
            {ACADEMIC_EDUCATION.map((item) => (
              <article key={`${item.title}-${item.period}`} className="timeline-card timeline-card--light">
                <div className="timeline-card__top">
                  <strong>{item.title}</strong>
                  <span>{item.period}</span>
                </div>
                <p>{item.institution}</p>
              </article>
            ))}
          </div>
        </article>

        <article className="detail-card detail-card--light">
          <p className="detail-card__eyebrow detail-card__eyebrow--dark">Selected credentials</p>
          <h2>Relevant ongoing development</h2>
          <div className="timeline-list timeline-list--light">
            {SELECTED_CREDENTIALS.map((item) => (
              <article key={`${item.title}-${item.period}`} className="timeline-card timeline-card--light">
                <div className="timeline-card__top">
                  <strong>{item.title}</strong>
                  <span>{item.period}</span>
                </div>
                <p>{item.provider}</p>
              </article>
            ))}
          </div>
        </article>
      </section>

      <section className="page-section page-section--light">
        <article className="cta-band cta-band--compact">
          <div>
            <p className="site-kicker">Contact</p>
            <h2>If your organisation needs senior advisory support, let&apos;s talk.</h2>
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
