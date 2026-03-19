/* Copyright (c) Dario Pizzolante */
import type { LucideIcon } from "lucide-react";
import {
  ArrowRight,
  Bot,
  BriefcaseBusiness,
  CalendarDays,
  CircuitBoard,
  ExternalLink,
  Layers3,
  ShieldCheck,
  Sparkles,
  Workflow,
} from "lucide-react";

import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import {
  ABOUT_PATH,
  ABOUT_SUMMARY,
  BOOKING_PATH,
  EXPERIENCE_PILLS,
  PROGRAMME_HIGHLIGHTS,
  SERVICE_DEFINITIONS,
} from "@/lib/publicSite";

type ServiceCard = {
  title: string;
  summary: string;
  icon: LucideIcon;
  href: string;
};

type ProcessStep = {
  title: string;
  summary: string;
  accent: "amber" | "blue" | "green" | "violet";
};

const SERVICE_ICONS: Record<string, LucideIcon> = {
  "AI Strategy": Sparkles,
  Automation: Workflow,
  Delivery: Layers3,
  "Fractional CIO/CDO": BriefcaseBusiness,
};

const SERVICES: ServiceCard[] = SERVICE_DEFINITIONS.map((service) => ({
  title: service.title,
  summary: service.summary,
  icon: SERVICE_ICONS[service.shortTitle] ?? Sparkles,
  href: `/services/${service.slug}`,
}));

const PROCESS: ProcessStep[] = [
  {
    title: "Assess",
    summary: "Clarify the business challenge, current friction points, and the real transformation opportunity.",
    accent: "amber",
  },
  {
    title: "Shape",
    summary: "Define the right mix of strategy, governance, automation, and delivery support for your context.",
    accent: "blue",
  },
  {
    title: "Deliver",
    summary: "Move from concept to implementation with practical execution, not slideware or over-designed plans.",
    accent: "green",
  },
  {
    title: "Improve",
    summary: "Embed continuous improvement so the business gains stay visible, measurable, and sustainable.",
    accent: "violet",
  },
];

export function PublicLandingPage() {
  return (
    <PublicSiteLayout>
      <section className="site-hero">
        <div className="site-hero__content">
          <p className="site-kicker">Independent advisory for modernization and practical AI</p>
          <h1>
            Strategy. Delivery.
            <br />
            Practical AI.
          </h1>
          <p className="site-hero__lead">
            I help organizations modernize operations, improve delivery, and apply AI where it
            creates real business value.
          </p>
          <div className="hero-inline-note">
            Senior support across strategy, transformation, and AI adoption with a practical
            delivery mindset.
          </div>
          <div className="site-hero__actions">
            <a className="site-button site-button--primary" href={BOOKING_PATH}>
              Book a strategy call
              <ArrowRight className="size-4" />
            </a>
            <a className="site-button site-button--secondary" href="/services">
              Explore services
            </a>
          </div>
          <div className="site-stat-strip" aria-label="Experience highlights">
            <article>
              <strong>20+</strong>
              <span>years of experience</span>
            </article>
            <article>
              <strong>4</strong>
              <span>core sectors served</span>
            </article>
            <article>
              <strong>25</strong>
              <span>member states coordinated in one programme</span>
            </article>
          </div>
        </div>

        <div className="site-hero__visual" aria-label="Advisory snapshot">
          <article className="hero-insight-card hero-insight-card--primary hero-insight-card--brand">
            <span className="hero-chip">
              <CircuitBoard className="size-4" />
              Stratevia advisory
            </span>
            <h2>Turn complex initiatives into clear next moves.</h2>
            <p>
              From technology roadmaps to AI-enabled process improvement, the emphasis stays on
              business clarity, governance, and execution.
            </p>
            <ul className="hero-checklist">
              <li>
                <ShieldCheck className="size-4" />
                Technology strategy and governance
              </li>
              <li>
                <Bot className="size-4" />
                Practical AI and automation opportunities
              </li>
              <li>
                <Layers3 className="size-4" />
                Delivery structure, modernization, and operating model support
              </li>
              <li>
                <BriefcaseBusiness className="size-4" />
                PMO, project management, and service management support for execution-focused delivery
              </li>
            </ul>
          </article>

          <article className="hero-insight-card hero-insight-card--secondary">
            <p className="hero-section-label">Selected background</p>
            <div className="hero-mini-grid">
              <div>
                <strong>IT leadership</strong>
                <span>Roadmaps, budgets, service improvement, and team leadership</span>
              </div>
              <div>
                <strong>Transformation</strong>
                <span>Modernization programmes, digitization, and operational structuring</span>
              </div>
              <div>
                <strong>AI enablement</strong>
                <span>Applied AI, process automation, and pragmatic business adoption</span>
              </div>
            </div>
          </article>
        </div>
      </section>

      <section className="site-section site-section--services" id="services">
        <div className="site-section__intro">
          <p className="site-kicker">Services</p>
          <h2>Senior support for organizations that need progress, not noise.</h2>
          <p>
            The offer is intentionally focused: strategic guidance, modernization support, and
            AI-enabled business improvement delivered in a practical way.
          </p>
        </div>
        <div className="service-grid">
          {SERVICES.map((service) => {
            const Icon = service.icon;

            return (
              <article key={service.title} className="service-card">
                <span className="service-card__icon">
                  <Icon className="size-5" />
                </span>
                <h3>{service.title}</h3>
                <p>{service.summary}</p>
                <a className="service-card__link" href={service.href}>
                  View service page
                  <ExternalLink className="size-4" />
                </a>
              </article>
            );
          })}
        </div>
      </section>

      <section className="site-section site-section--split site-section--about" id="about">
        <div className="site-section__intro">
          <p className="site-kicker">About</p>
          <h2>Experienced leadership with a practical delivery mindset.</h2>
          {ABOUT_SUMMARY.map((paragraph) => (
            <p key={paragraph}>{paragraph}</p>
          ))}
          <a className="site-button site-button--primary site-button--inline" href={ABOUT_PATH}>
            View full profile
            <ArrowRight className="size-4" />
          </a>
        </div>
        <div className="experience-panel">
          <div className="experience-panel__profile">
            <div className="experience-portrait-frame">
                <img
                  alt="Portrait of Dario Pizzolante"
                  className="experience-portrait"
                  src="/dario-pizzolante.jpg"
                />
              </div>
              <div className="experience-panel__header">
                <h3>Dario Pizzolante</h3>
                <p>IT leadership, modernization, and AI-enabled business transformation</p>
              </div>
            </div>
          <div className="experience-pill-list">
              {EXPERIENCE_PILLS.map((pill) => (
                <span key={pill} className="experience-pill">
                  {pill}
              </span>
            ))}
          </div>
          <div className="experience-highlights">
            {PROGRAMME_HIGHLIGHTS.map((item) => (
              <article key={item.org}>
                <strong>{item.org}</strong>
                <span>{item.summary}</span>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="site-section site-section--process" id="process">
        <div className="site-section__intro">
          <p className="site-kicker">Process</p>
          <h2>A clear path from challenge to measurable improvement.</h2>
          <p>
            The work is designed to be fast, grounded, and outcome-oriented so decisions move
            forward without unnecessary complexity.
          </p>
        </div>
        <div className="process-grid">
          {PROCESS.map((step) => (
            <article key={step.title} className={`process-card process-card--${step.accent}`}>
              <h3>{step.title}</h3>
              <p>{step.summary}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="site-section site-section--credibility">
        <div className="credibility-band">
          <article>
            <strong>Executive perspective</strong>
            <span>Leadership, budgets, governance, and operating model design.</span>
          </article>
          <article>
            <strong>Delivery credibility</strong>
            <span>Programmes, modernization work, and structured execution support.</span>
          </article>
          <article>
            <strong>AI with business sense</strong>
            <span>Automation and AI positioned as practical enablers, not hype.</span>
          </article>
        </div>
      </section>

      <section className="site-section site-section--booking" id="booking">
        <div className="booking-card">
          <div>
            <p className="site-kicker">Booking</p>
            <h2>Start with a focused conversation.</h2>
            <p>
              Whether you are shaping a transformation initiative, exploring AI use cases, or need
              senior technology guidance, the first step is a concise discovery call.
            </p>
          </div>
          <div className="booking-card__actions">
            <a className="site-button site-button--primary" href={BOOKING_PATH}>
              <CalendarDays className="size-4" />
              Go to booking page
            </a>
            <p>
              A first conversation can quickly clarify priorities, current blockers, and the most
              practical next step.
            </p>
          </div>
        </div>
      </section>
    </PublicSiteLayout>
  );
}
