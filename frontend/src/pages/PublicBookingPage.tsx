/* Copyright (c) Dario Pizzolante */
import { ArrowRight, CalendarDays, Check, Mail, MessageSquareText } from "lucide-react";

import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import { BOOKING_OPTIONS, BOOKING_POINTS } from "@/lib/publicSite";

export function PublicBookingPage() {
  return (
    <PublicSiteLayout>
      <section className="page-hero page-hero--booking">
        <div className="page-hero__content">
          <a className="back-link" href="/">
            Home
          </a>
          <p className="site-kicker">Booking</p>
          <h1>Start with a focused, practical conversation.</h1>
          <p className="page-lead">
            The first step is a short discussion designed to clarify your context, identify the
            right priority, and decide what kind of support makes the most sense.
          </p>
          <div className="booking-points">
            {BOOKING_POINTS.map((point) => (
              <div key={point} className="booking-point">
                <Check className="size-4" />
                <span>{point}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="page-hero__panel">
          <div className="booking-panel__head">
            <strong>Best for</strong>
            <p>
              Leaders and teams exploring modernization, operational improvement, AI opportunities,
              or ongoing technology advisory support.
            </p>
          </div>
          <div className="booking-actions">
            <a className="site-button site-button--primary" href="mailto:contact@stratevia.com">
              <Mail className="size-4" />
              Request a conversation
            </a>
            <a className="site-button site-button--secondary" href="/services">
              <ArrowRight className="size-4" />
              Review services first
            </a>
          </div>
          <p className="booking-note">
            This page is ready to connect to your AI lead flow later through a form, scheduling
            tool, or intake workflow.
          </p>
        </div>
      </section>

      <section className="page-section">
        <div className="booking-option-grid">
          {BOOKING_OPTIONS.map((option, index) => (
            <article key={option.title} className="booking-option">
              <div className="booking-option__index">0{index + 1}</div>
              <h2>{option.title}</h2>
              <p>{option.summary}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="page-section">
        <article className="detail-card detail-card--wide">
          <p className="detail-card__eyebrow">Next step</p>
          <h2>How booking can evolve</h2>
          <div className="timeline-list">
            <article className="timeline-card">
              <div className="timeline-card__top">
                <strong>Now</strong>
                <CalendarDays className="size-4" />
              </div>
              <p>A clear booking page with a direct entry point for inquiries and first discussions.</p>
            </article>
            <article className="timeline-card">
              <div className="timeline-card__top">
                <strong>Next</strong>
                <MessageSquareText className="size-4" />
              </div>
              <p>Wire a form or scheduler into your hidden AI platform for lead intake and follow-up.</p>
            </article>
          </div>
        </article>
      </section>
    </PublicSiteLayout>
  );
}
