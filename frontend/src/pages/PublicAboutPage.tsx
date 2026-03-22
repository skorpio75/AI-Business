/* Copyright (c) Dario Pizzolante */
import { useState } from "react";
import { ArrowRight } from "lucide-react";

import { PublicImageHero } from "@/components/PublicImageHero";
import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import {
  ABOUT_HERO_HIGHLIGHTS,
  ABOUT_LEAD,
  ABOUT_LANGUAGES,
  ABOUT_PROFILE_TITLE,
  ABOUT_ROTARY,
  ABOUT_SUMMARY,
  ACADEMIC_EDUCATION,
  ABOUT_CORE_STRENGTHS,
  CONTACT_PATH,
  REPRESENTATIVE_EXPERIENCE,
  SELECTED_CREDENTIALS,
} from "@/lib/publicSite";

type AboutProfileTab = "overview" | "resume";

const ABOUT_PROFILE_TABS: Array<{ id: AboutProfileTab; label: string }> = [
  { id: "overview", label: "Overview" },
  { id: "resume", label: "Resume" },
];

export function PublicAboutPage() {
  const [activeTab, setActiveTab] = useState<AboutProfileTab>("overview");

  return (
    <PublicSiteLayout>
      <PublicImageHero
        backHref="/"
        backLabel="Home"
        kicker="About"
        title="Stratevia"
        lead={ABOUT_LEAD}
        panel={
          <div className="about-hero-highlight-stack">
            {ABOUT_HERO_HIGHLIGHTS.map((item) => (
              <article key={item.title} className="about-hero-highlight-row">
                <h2>{item.title}</h2>
                <p>{item.summary}</p>
              </article>
            ))}
          </div>
        }
        panelClassName="image-hero__panel--about-highlights"
        actions={
          <>
            <a className="site-button site-button--primary" href={CONTACT_PATH}>
              Book a call
              <ArrowRight className="size-4" />
            </a>
          </>
        }
      />

      <section className="page-section page-section--light band-section band-section--soft">
        <div className="band-shell">
          <article className="profile-card band-panel">
            <aside className="profile-card__sidebar">
              <div className="profile-card__portrait">
                <img alt="Portrait of Dario Pizzolante" className="image-hero__portrait" src="/dario-pizzolante.jpg" />
              </div>
            </aside>

            <div className="profile-card__main">
              <div className="profile-card__header">
                <p className="site-kicker">Biography</p>
                <h2>Dario Pizzolante</h2>
                <p className="profile-card__title">{ABOUT_PROFILE_TITLE}</p>
              </div>

              <div aria-label="Profile sections" className="profile-tabs" role="tablist">
                {ABOUT_PROFILE_TABS.map((tab) => {
                  const isActive = activeTab === tab.id;

                  return (
                    <button
                      key={tab.id}
                      aria-controls={`about-panel-${tab.id}`}
                      aria-selected={isActive}
                      className={`profile-tabs__button${isActive ? " profile-tabs__button--active" : ""}`}
                      id={`about-tab-${tab.id}`}
                      role="tab"
                      type="button"
                      onClick={() => setActiveTab(tab.id)}
                    >
                      {tab.label}
                    </button>
                  );
                })}
              </div>

              <div
                aria-labelledby={`about-tab-${activeTab}`}
                className="profile-card__panel"
                id={`about-panel-${activeTab}`}
                role="tabpanel"
              >
                {activeTab === "overview" ? (
                  <div className="profile-biography">
                    {ABOUT_SUMMARY.map((paragraph) => (
                      <p key={paragraph}>{paragraph}</p>
                    ))}
                  </div>
                ) : (
                  <div className="profile-resume">
                    <div className="profile-resume__grid">
                      <section className="profile-resume__section">
                        <p className="detail-card__eyebrow detail-card__eyebrow--dark">Education</p>
                        <h3>Academic background</h3>
                        <div className="timeline-list timeline-list--light">
                          {ACADEMIC_EDUCATION.map((item) => (
                            <article key={`${item.title}-${item.period}`} className="timeline-card timeline-card--light">
                              <div className="timeline-card__header-stacked">
                                <strong>{item.title}</strong>
                                <span className="timeline-card__period">{item.period}</span>
                              </div>
                              <p>{item.institution}</p>
                            </article>
                          ))}
                        </div>
                      </section>

                      <section className="profile-resume__section">
                        <p className="detail-card__eyebrow detail-card__eyebrow--dark">Credentials</p>
                        <h3>Relevant ongoing development</h3>
                        <div className="timeline-list timeline-list--light">
                          {SELECTED_CREDENTIALS.map((item) => (
                            <article key={`${item.title}-${item.period}`} className="timeline-card timeline-card--light">
                              <div className="timeline-card__header-stacked">
                                <strong>{item.title}</strong>
                                <span className="timeline-card__period">{item.period}</span>
                              </div>
                              <p>{item.provider}</p>
                            </article>
                          ))}
                        </div>
                      </section>
                    </div>

                    <div className="profile-languages">
                      <p className="detail-card__eyebrow detail-card__eyebrow--dark">Languages</p>
                      <p>{ABOUT_LANGUAGES.join(" | ")}</p>
                    </div>

                    <section className="profile-affiliation">
                      <div className="profile-affiliation__logo">
                        <img alt="Rotary logo" src="/rotary-color.svg" />
                      </div>
                      <div className="profile-affiliation__content">
                        <p className="detail-card__eyebrow detail-card__eyebrow--dark">Rotary</p>
                        <h3>{ABOUT_ROTARY.title}</h3>
                        <p className="profile-affiliation__period">{ABOUT_ROTARY.period}</p>
                        <p>{ABOUT_ROTARY.summary}</p>
                      </div>
                    </section>
                  </div>
                )}
              </div>
            </div>
          </article>
        </div>
      </section>

      <section className="page-section page-section--light band-section">
        <div className="band-shell">
          <div className="section-heading section-heading--band">
            <p className="site-kicker">Core strengths</p>
            <h2>Senior support across leadership, transformation, and practical delivery.</h2>
          </div>
          <div className="trust-grid">
            {ABOUT_CORE_STRENGTHS.map((item) => (
              <article key={item.title} className="trust-card">
                <h3>{item.title}</h3>
                <p>{item.summary}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="page-section page-section--light band-section band-section--tint">
        <div className="band-shell">
          <div className="section-heading section-heading--band">
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
        </div>
      </section>

      <section className="page-section page-section--light band-section">
        <div className="band-shell">
          <article className="cta-band cta-band--compact band-panel">
            <div>
              <p className="site-kicker">Contact</p>
              <h2>If you need clarity on transformation, AI adoption, or delivery support, let&apos;s talk.</h2>
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
