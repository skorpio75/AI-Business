/* Copyright (c) Dario Pizzolante */
import { type FormEvent, useState } from "react";
import {
  ArrowRight,
  CalendarDays,
  Check,
  LoaderCircle,
  MessageSquareText,
} from "lucide-react";

import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import { apiClient } from "@/lib/api";
import {
  BOOKING_OPTIONS,
  BOOKING_POINTS,
  BOOKING_TIMING_OPTIONS,
  SERVICE_DEFINITIONS,
} from "@/lib/publicSite";

type BookingFormState = {
  fullName: string;
  email: string;
  company: string;
  roleTitle: string;
  serviceInterest: string;
  challengeSummary: string;
  preferredTiming: string;
  consentToContact: boolean;
};

const INITIAL_FORM: BookingFormState = {
  fullName: "",
  email: "",
  company: "",
  roleTitle: "",
  serviceInterest: "",
  challengeSummary: "",
  preferredTiming: BOOKING_TIMING_OPTIONS[0],
  consentToContact: true,
};

export function PublicBookingPage() {
  const [form, setForm] = useState(INITIAL_FORM);
  const [status, setStatus] = useState<"idle" | "submitting" | "success" | "error">("idle");
  const [responseMessage, setResponseMessage] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatus("submitting");
    setResponseMessage("");

    try {
      const response = await apiClient.submitPublicBookingRequest({
        full_name: form.fullName,
        email: form.email,
        company: form.company || undefined,
        role_title: form.roleTitle || undefined,
        service_interest: form.serviceInterest || undefined,
        challenge_summary: form.challengeSummary,
        preferred_timing: form.preferredTiming || undefined,
        website_path: typeof window === "undefined" ? "/booking" : window.location.pathname,
        consent_to_contact: form.consentToContact,
      });
      setStatus("success");
      setResponseMessage(response.message);
      setForm(INITIAL_FORM);
    } catch {
      setStatus("error");
      setResponseMessage("The request could not be submitted right now. Please try again in a moment.");
    }
  }

  function updateField<Key extends keyof BookingFormState>(field: Key, value: BookingFormState[Key]) {
    setForm((current) => ({ ...current, [field]: value }));
  }

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

        <div className="page-hero__panel booking-form-panel">
          <div className="booking-panel__head">
            <strong>Request a conversation</strong>
            <p>
              Share a bit of context and your request will go directly into Stratevia&apos;s private
              intake workflow.
            </p>
          </div>
          <form className="booking-form" onSubmit={handleSubmit}>
            <div className="booking-form__grid">
              <label className="booking-field">
                <span>Name</span>
                <input
                  autoComplete="name"
                  name="fullName"
                  required
                  type="text"
                  value={form.fullName}
                  onChange={(event) => updateField("fullName", event.target.value)}
                />
              </label>
              <label className="booking-field">
                <span>Email</span>
                <input
                  autoComplete="email"
                  name="email"
                  required
                  type="email"
                  value={form.email}
                  onChange={(event) => updateField("email", event.target.value)}
                />
              </label>
              <label className="booking-field">
                <span>Company</span>
                <input
                  autoComplete="organization"
                  name="company"
                  type="text"
                  value={form.company}
                  onChange={(event) => updateField("company", event.target.value)}
                />
              </label>
              <label className="booking-field">
                <span>Role</span>
                <input
                  autoComplete="organization-title"
                  name="roleTitle"
                  type="text"
                  value={form.roleTitle}
                  onChange={(event) => updateField("roleTitle", event.target.value)}
                />
              </label>
              <label className="booking-field">
                <span>Service of interest</span>
                <select
                  name="serviceInterest"
                  value={form.serviceInterest}
                  onChange={(event) => updateField("serviceInterest", event.target.value)}
                >
                  <option value="">Choose if you already know</option>
                  {SERVICE_DEFINITIONS.map((service) => (
                    <option key={service.slug} value={service.title}>
                      {service.title}
                    </option>
                  ))}
                </select>
              </label>
              <label className="booking-field">
                <span>Timing</span>
                <select
                  name="preferredTiming"
                  value={form.preferredTiming}
                  onChange={(event) => updateField("preferredTiming", event.target.value)}
                >
                  {BOOKING_TIMING_OPTIONS.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            <label className="booking-field booking-field--full">
              <span>What would you like to discuss?</span>
              <textarea
                name="challengeSummary"
                required
                rows={5}
                value={form.challengeSummary}
                onChange={(event) => updateField("challengeSummary", event.target.value)}
              />
            </label>

            <label className="booking-consent">
              <input
                checked={form.consentToContact}
                name="consentToContact"
                type="checkbox"
                onChange={(event) => updateField("consentToContact", event.target.checked)}
              />
              <span>I agree to be contacted about this inquiry.</span>
            </label>

            <div className="booking-actions">
              <button className="site-button site-button--primary" disabled={status === "submitting"} type="submit">
                {status === "submitting" ? <LoaderCircle className="size-4 animate-spin" /> : null}
                {status === "submitting" ? "Sending request" : "Send request"}
              </button>
              <a className="site-button site-button--secondary" href="/services">
                <ArrowRight className="size-4" />
                Review services first
              </a>
            </div>
          </form>
          <p className={`booking-note ${status === "success" ? "booking-note--success" : ""}`}>
            {responseMessage ||
              "This form routes into the private platform so visitors see only the website, not the internal AI workspace."}
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
              <p>A live booking form routes advisory inquiries into the private intake platform.</p>
            </article>
            <article className="timeline-card">
              <div className="timeline-card__top">
                <strong>Next</strong>
                <MessageSquareText className="size-4" />
              </div>
              <p>Add scheduler sync, qualification steps, and follow-up automation behind the same hidden workflow.</p>
            </article>
          </div>
        </article>
      </section>
    </PublicSiteLayout>
  );
}
