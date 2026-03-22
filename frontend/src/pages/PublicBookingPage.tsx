/* Copyright (c) Dario Pizzolante */
import { type FormEvent, useState } from "react";
import { ArrowRight, LoaderCircle } from "lucide-react";

import { PublicImageHero } from "@/components/PublicImageHero";
import { PublicSiteLayout } from "@/components/PublicSiteLayout";
import { apiClient } from "@/lib/api";
import {
  CONTACT_NEXT_STEPS,
  CONTACT_PATH,
  CONTACT_REASONS,
  CONTACT_TIMING_OPTIONS,
  SERVICE_PILLARS,
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
  preferredTiming: CONTACT_TIMING_OPTIONS[0],
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
        website_path: typeof window === "undefined" ? CONTACT_PATH : window.location.pathname,
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
      <PublicImageHero
        backHref="/"
        backLabel="Home"
        kicker="Contact"
        title="Start with a focused conversation."
        lead="A first discussion to understand whether your needs are mainly about transformation priorities, AI and digital operations, or delivery governance support."
      />

      <section className="page-section page-section--light band-section band-section--soft">
        <div className="band-shell">
          <div className="contact-layout">
            <aside className="contact-reasons">
              <p className="site-kicker">Where I can help</p>
              <h2>Typical reasons organisations get in touch.</h2>
              {CONTACT_REASONS.map((reason) => (
                <p key={reason}>{reason}</p>
              ))}
            </aside>

            <article className="detail-card detail-card--light booking-form-panel">
              <div className="booking-panel__head">
                <strong>Request a conversation</strong>
                <p>
                  Share a bit of context and, if useful, indicate whether this is mainly about
                  assessment and transformation, AI and digital operations, or delivery support.
                </p>
              </div>

              <form className="booking-form booking-form--light" onSubmit={handleSubmit}>
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
                    <span>Service area or topic of interest</span>
                    <select
                      name="serviceInterest"
                      value={form.serviceInterest}
                      onChange={(event) => updateField("serviceInterest", event.target.value)}
                    >
                      <option value="">Choose if you already know</option>
                      <optgroup label="Service pillars">
                        {SERVICE_PILLARS.map((pillar) => (
                          <option key={pillar.key} value={pillar.title}>
                            {pillar.title}
                          </option>
                        ))}
                      </optgroup>
                      <optgroup label="Detailed services">
                        {SERVICE_DEFINITIONS.map((service) => (
                          <option key={service.slug} value={service.title}>
                            {service.title}
                          </option>
                        ))}
                      </optgroup>
                    </select>
                  </label>
                  <label className="booking-field">
                    <span>Preferred timing</span>
                    <select
                      name="preferredTiming"
                      value={form.preferredTiming}
                      onChange={(event) => updateField("preferredTiming", event.target.value)}
                    >
                      {CONTACT_TIMING_OPTIONS.map((option) => (
                        <option key={option} value={option}>
                          {option}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>

                <label className="booking-field booking-field--full">
                  <span>Briefly describe your context</span>
                  <textarea
                    name="challengeSummary"
                    placeholder="What are you trying to assess, improve, or stabilise right now?"
                    required
                    rows={5}
                    value={form.challengeSummary}
                    onChange={(event) => updateField("challengeSummary", event.target.value)}
                  />
                </label>

                <label className="booking-consent booking-consent--light">
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
                    View services
                    <ArrowRight className="size-4" />
                  </a>
                </div>
              </form>

              {responseMessage ? (
                <p className={`booking-note ${status === "success" ? "booking-note--success" : "booking-note--error"}`}>
                  {responseMessage}
                </p>
              ) : null}
            </article>
          </div>
        </div>
      </section>

      <section className="page-section page-section--light band-section">
        <div className="band-shell">
          <div className="section-heading section-heading--band">
            <p className="site-kicker">What happens next</p>
            <h2>Simple, direct, and obligation-free.</h2>
          </div>
          <div className="next-step-grid">
            {CONTACT_NEXT_STEPS.map((step) => (
              <article key={step} className="next-step-card">
                <p>{step}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="page-section page-section--light band-section band-section--tint">
        <div className="band-shell">
          <article className="direct-contact-card band-panel">
            <div>
              <p className="site-kicker">Direct contact</p>
              <h2>Prefer a direct introduction?</h2>
            </div>
            <div className="direct-contact-card__links">
              <a href="mailto:contact@stratevia.eu">contact@stratevia.eu</a>
              <a href="https://www.linkedin.com/in/dariopizzolante" rel="noreferrer" target="_blank">
                LinkedIn
              </a>
            </div>
          </article>
        </div>
      </section>
    </PublicSiteLayout>
  );
}
