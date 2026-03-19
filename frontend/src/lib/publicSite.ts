/* Copyright (c) Dario Pizzolante */
export type ServiceSlug =
  | "ai-strategy-roadmapping"
  | "automation-digital-operations"
  | "fractional-cio-transformation-advisory";

export const ABOUT_PATH = "/about";
export const BOOKING_PATH = "/booking";

export type ServiceDefinition = {
  slug: ServiceSlug;
  title: string;
  shortTitle: string;
  tagline: string;
  summary: string;
  intro: string;
  outcomes: string[];
  engagements: string[];
  fit: string[];
};

export const PUBLIC_NAV_LINKS = [
  { href: "/", label: "Home" },
  { href: "/services", label: "Services" },
  { href: ABOUT_PATH, label: "About" },
  { href: BOOKING_PATH, label: "Booking" },
] as const;

export const ABOUT_SUMMARY = [
  "I bring more than two decades of experience across IT leadership, digital transformation, and operational management in international environments. My work has spanned energy, consulting, legal-tech, and public-sector programmes.",
  "The common thread is helping organizations modernize, structure delivery, improve governance, and adopt technology in ways that make day-to-day operations stronger.",
];

export const EXPERIENCE_PILLS = [
  "20+ years across IT leadership and delivery",
  "Energy, consulting, legal-tech, and public sector",
  "Executive leadership with hands-on programme delivery",
  "Modernization, governance, and practical AI adoption",
];

export const PROGRAMME_HIGHLIGHTS = [
  {
    org: "Societe Electrique de l'Our",
    summary: "Modernization roadmap, cloud transition, governance, and cost optimization.",
  },
  {
    org: "Unified Patent Court",
    summary: "IT operating model and programme coordination across 25 member states.",
  },
  {
    org: "Net Service Lux",
    summary: "Digitalization growth, local leadership, and AI-enabled solution expansion.",
  },
];

export const ABOUT_FACTS = [
  "IT strategy, governance, and modernization roadmaps",
  "Digital transformation with practical execution support",
  "Leadership across teams, budgets, and vendor ecosystems",
  "Applied AI and automation positioned around business value",
];

export const CAREER_MILESTONES = [
  {
    role: "Management Consulting",
    period: "2025 to present",
    summary:
      "Management consulting and digitalization support focused on operational efficiency and day-to-day business improvement.",
  },
  {
    role: "Managing Director, Net Service Lux",
    period: "2023 to 2025",
    summary:
      "Led the Luxembourg subsidiary, developed local operations, and expanded digitalization and AI-enabled delivery services.",
  },
  {
    role: "Head of IT, Societe Electrique de l'Our",
    period: "2021 to 2023",
    summary:
      "Owned IT strategy and operations, modernization planning, service improvement, and major transformation initiatives.",
  },
  {
    role: "IT Working Group Coordinator and IT Manager, Unified Patent Court",
    period: "2016 to 2019",
    summary:
      "Helped establish the IT function of a new European jurisdiction and coordinated a multi-workstream international programme.",
  },
];

export const BOOKING_POINTS = [
  "A focused first conversation about your business context and priorities",
  "Clear identification of the most valuable next step",
  "A practical view of where strategy, modernization, or AI can help",
];

export const BOOKING_OPTIONS = [
  {
    title: "Strategy conversation",
    summary: "A first discussion for leaders exploring transformation priorities, technology direction, or AI opportunities.",
  },
  {
    title: "Operational improvement discussion",
    summary: "A session centered on process friction, delivery bottlenecks, and practical modernization needs.",
  },
  {
    title: "Advisory fit check",
    summary: "A straightforward conversation to decide whether strategic advisory or fractional leadership support is the right fit.",
  },
];

export const BOOKING_TIMING_OPTIONS = [
  "As soon as possible",
  "Within the next 2 weeks",
  "Within the next month",
  "Just exploring for now",
] as const;

export const SERVICE_DEFINITIONS: ServiceDefinition[] = [
  {
    slug: "ai-strategy-roadmapping",
    title: "AI strategy and roadmapping",
    shortTitle: "AI Strategy",
    tagline: "Move from AI interest to a focused, realistic business plan.",
    summary:
      "Clarify the highest-value use cases, governance needs, delivery priorities, and practical sequence for adopting AI in your business.",
    intro:
      "This service is designed for organizations that want to explore AI seriously without rushing into scattered tools or vague experimentation.",
    outcomes: [
      "A clearer AI opportunity picture tied to business goals",
      "A practical roadmap with priorities, dependencies, and next steps",
      "Better alignment between leadership, operations, and technology decisions",
    ],
    engagements: [
      "Executive workshops and opportunity framing",
      "Use-case prioritization and roadmap design",
      "AI governance, delivery, and operating model guidance",
    ],
    fit: [
      "Leaders who want to understand where AI can create real value",
      "Teams planning modernization and process improvement",
      "Organizations that need a structured starting point before investing further",
    ],
  },
  {
    slug: "automation-digital-operations",
    title: "Automation and digital operations",
    shortTitle: "Automation",
    tagline: "Reduce friction, simplify operations, and improve the way work gets done.",
    summary:
      "Identify repetitive effort, streamline internal workflows, and support digital operations with better process design, automation, and practical tooling.",
    intro:
      "This service focuses on business efficiency first. The goal is to make daily operations easier, clearer, and more scalable.",
    outcomes: [
      "Less manual effort and fewer operational bottlenecks",
      "Cleaner process flow and better day-to-day execution",
      "A stronger foundation for future AI and digital initiatives",
    ],
    engagements: [
      "Process review and operational diagnosis",
      "Automation opportunity mapping and solution shaping",
      "Digital workflow design and implementation support",
    ],
    fit: [
      "Organizations with too much manual coordination or fragmented processes",
      "Teams looking to digitize internal operations without overcomplicating delivery",
      "Businesses that want practical wins before larger transformation programmes",
    ],
  },
  {
    slug: "fractional-cio-transformation-advisory",
    title: "Fractional CIO and transformation advisory",
    shortTitle: "Fractional CIO",
    tagline: "Bring senior technology leadership into critical decisions and delivery moments.",
    summary:
      "Get experienced support across technology direction, modernization choices, delivery structure, vendor coordination, and executive-level decision making.",
    intro:
      "This service is a strong fit when the business needs senior guidance but does not need, or does not yet want, a full-time executive hire.",
    outcomes: [
      "Stronger technology decisions with clearer business alignment",
      "Better structure around delivery, governance, and modernization work",
      "Senior guidance for leadership discussions, vendors, and execution priorities",
    ],
    engagements: [
      "Technology leadership on a fractional or advisory basis",
      "Roadmap and architecture guidance for modernization initiatives",
      "Executive support across delivery governance and transformation planning",
    ],
    fit: [
      "Growing businesses that need senior technology perspective",
      "Leaders navigating change, vendor decisions, or modernization pressure",
      "Organizations that want practical guidance across strategy and execution",
    ],
  },
];

export function getServiceDefinition(slug: ServiceSlug) {
  return SERVICE_DEFINITIONS.find((service) => service.slug === slug);
}
