/* Copyright (c) Dario Pizzolante */
export type ServiceSlug =
  | "ai-strategy-roadmapping"
  | "automation-digital-operations"
  | "fractional-cto-transformation-advisory";

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
  { href: "/#about", label: "About" },
  { href: "/#booking", label: "Booking" },
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
    slug: "fractional-cto-transformation-advisory",
    title: "Fractional CTO and transformation advisory",
    shortTitle: "Fractional CTO",
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
