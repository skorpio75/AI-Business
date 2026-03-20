/* Copyright (c) Dario Pizzolante */
export type ServiceSlug =
  | "ai-strategy-roadmapping"
  | "automation-digital-operations"
  | "delivery-pmo-project-service-management"
  | "fractional-cio-transformation-advisory";

export const ABOUT_PATH = "/about";
export const CONTACT_PATH = "/contact";
export const LEGACY_BOOKING_PATH = "/booking";
export const CASE_STUDIES_PATH = "/case-studies";
export const PROJECTS_PATH = "/projects";
export const INSIGHTS_PATH = "/insights";

export type PublicSectionKey = "services" | "case-studies" | "projects" | "insights";

export type PublicSectionItem = {
  id: string;
  label: string;
  href: string;
  summary: string;
};

export type PublicSectionDefinition = {
  key: PublicSectionKey;
  label: string;
  path: string;
  shortLabel: string;
  description: string;
  items: PublicSectionItem[];
};

export type ServiceDefinition = {
  slug: ServiceSlug;
  title: string;
  shortTitle: string;
  tagline: string;
  summary: string;
  intro: string;
  bestFor: string;
  clientProblems: string[];
  outcomes: string[];
  engagements: string[];
  fit: string[];
  proofPoints: string[];
};

export type AcademicEducationItem = {
  title: string;
  institution: string;
  period: string;
};

export type CertificationItem = {
  title: string;
  provider: string;
  period: string;
};

export type HighlightItem = {
  title: string;
  summary: string;
  href?: string;
};

export type ExperienceItem = {
  organization: string;
  role: string;
  summary: string;
};

export const PUBLIC_NAV_LINKS = [
  { href: ABOUT_PATH, label: "About" },
  { href: CONTACT_PATH, label: "Contact" },
] as const;

export const HOME_HERO = {
  eyebrow: "Independent advisory for transformation and practical AI",
  title: "Strategy. Transformation. Execution.",
  summary:
    "Improve governance and delivery, turn technology + AI into practical business value.",
  focusAreas: [
    "Strategy and governance",
    "Technology, AI and automation",
    "Delivery and transformation support",
  ],
};

export const HOME_SERVICE_PILLARS = [
  {
    title: "Technology & transformation advisory",
    summary: "Clarify priorities, structure initiatives, and move forward with a realistic path.",
    href: "/services/fractional-cio-transformation-advisory",
  },
  {
    title: "AI & automation enablement",
    summary: "Turn AI and process improvement into focused use cases with clear business value.",
    href: "/services/ai-strategy-roadmapping",
  },
  {
    title: "Delivery governance & fractional leadership",
    summary: "Bring senior structure to programmes, PMO needs, and execution pressure points.",
    href: "/services/delivery-pmo-project-service-management",
  },
] as const;

export const HOW_I_WORK_STEPS = [
  {
    title: "Assess",
    summary: "Understand the context, blockers, and objectives.",
  },
  {
    title: "Prioritise",
    summary: "Define the most valuable path forward.",
  },
  {
    title: "Deliver",
    summary: "Support execution with structure and senior guidance.",
  },
] as const;

export const STRATEVIA_PROOF_POINTS = [
  {
    title: "Senior executive experience",
    summary: "Leadership across IT, transformation, governance, and operating environments.",
  },
  {
    title: "Business + technology perspective",
    summary: "Advice shaped around outcomes, not technology for its own sake.",
  },
  {
    title: "Practical execution focus",
    summary: "Clear decisions, realistic sequencing, and support that helps work move.",
  },
] as const;

export const SELECTED_BACKGROUND = [
  "Microsoft",
  "Unified Patent Court",
  "Societe Electrique de l'Our",
  "Net Service Lux",
] as const;

export const SELECTED_BACKGROUND_SUMMARY =
  "Experience spanning leadership, modernization, governance, and operational transformation.";

export const SERVICES_HERO_REASONS = [
  "Unclear transformation priorities",
  "AI interest but no roadmap",
  "Manual or fragmented operations",
  "Need senior guidance without a full-time hire",
] as const;

export const ENGAGEMENT_FORMATS = [
  {
    title: "Strategic advisory",
    summary: "Short, focused support for decisions, direction, and prioritisation.",
  },
  {
    title: "Transformation support",
    summary: "Hands-on guidance to shape and stabilise change initiatives.",
  },
  {
    title: "Fractional leadership",
    summary: "Senior technology and transformation input without a permanent executive hire.",
  },
  {
    title: "PMO / delivery reinforcement",
    summary: "Added governance, cadence, and follow-through for pressured delivery work.",
  },
] as const;

export const ABOUT_LEAD =
  "I work with organisations that need senior guidance across transformation, technology decisions, delivery, and practical AI adoption.";

export const ABOUT_HERO_HIGHLIGHTS = [
  {
    title: "20+ years",
    summary: "leadership, transformation, delivery",
  },
  {
    title: "Ex-Microsoft",
    summary: "big-tech & enterprise grounding",
  },
  {
    title: "International",
    summary: "multi-stakeholder programmes",
  },
] as const;

export const ABOUT_SUMMARY = [
  "My background combines more than two decades of IT leadership, digital transformation, service management, and operational improvement across international environments.",
  "Clients typically engage when they need clarity, stronger governance, better execution structure, or senior advisory support without adding unnecessary complexity.",
];

export const ABOUT_CORE_STRENGTHS = [
  {
    title: "Transformation leadership",
    summary: "From modernization roadmaps to operating-model decisions and programme structure.",
  },
  {
    title: "Governance and delivery",
    summary: "Senior support for PMO, service management, stakeholder alignment, and follow-through.",
  },
  {
    title: "Practical AI enablement",
    summary: "Applying AI and automation where they support delivery, operations, and business value.",
  },
] as const;

export const REPRESENTATIVE_EXPERIENCE: ExperienceItem[] = [
  {
    organization: "Microsoft",
    role: "Technology consulting and operational leadership",
    summary: "Executive-level perspective across governance, service management, and enterprise delivery.",
  },
  {
    organization: "Unified Patent Court",
    role: "IT coordination and programme setup",
    summary: "Supported the IT function and programme structure of a new European jurisdiction.",
  },
  {
    organization: "Societe Electrique de l'Our",
    role: "Head of IT",
    summary: "Owned modernization planning, cloud transition, governance, and service improvement.",
  },
  {
    organization: "Net Service Lux",
    role: "Managing Director",
    summary: "Led local growth, digitalization delivery, and AI-enabled service expansion.",
  },
] as const;

export const ACADEMIC_EDUCATION: AcademicEducationItem[] = [
  {
    title: "Master of Science, Computer Science",
    institution: "Oxford Brookes University",
    period: "2003 to 2005",
  },
  {
    title: "Bachelor of Science, Software Engineering",
    institution: "University of Bedfordshire",
    period: "2002 to 2003",
  },
  {
    title: "Diploma of Technology, Business Computing",
    institution: "University of Luxembourg",
    period: "1998 to 2001",
  },
] as const;

export const SELECTED_CREDENTIALS: CertificationItem[] = [
  {
    title: "IBM RAG and Agentic AI",
    provider: "Coursera",
    period: "2026",
  },
  {
    title: "Creating an AI Adoption Strategy for Businesses",
    provider: "LinkedIn",
    period: "2025",
  },
  {
    title: "Strategic Organization Design",
    provider: "Coursera",
    period: "2018",
  },
] as const;

export const CONTACT_REASONS = [
  "A transformation initiative needs structure",
  "AI opportunity needs prioritisation",
  "Delivery is slipping",
  "Senior support is needed without a full-time hire",
] as const;

export const CONTACT_NEXT_STEPS = [
  "Your request is reviewed directly.",
  "The first reply focuses on fit and next step.",
  "There is no obligation.",
] as const;

export const CONTACT_TIMING_OPTIONS = [
  "As soon as possible",
  "Within the next 2 weeks",
  "Within the next month",
  "Just exploring for now",
] as const;

export const SERVICE_DEFINITIONS: ServiceDefinition[] = [
  {
    slug: "ai-strategy-roadmapping",
    title: "AI Strategy & Roadmapping",
    shortTitle: "Technology & AI Strategy",
    tagline: "Move from AI interest to a focused, realistic business plan.",
    summary: "Clarify the use cases, priorities, and roadmap before investing in the wrong direction.",
    intro:
      "This service helps organisations approach AI with clarity, realism, and a business-led sequence instead of scattered experimentation.",
    bestFor: "Best for organisations that need structure before committing time and budget to AI initiatives.",
    clientProblems: [
      "AI interest exists, but priorities are unclear",
      "Use cases feel disconnected from business value",
      "Leadership wants a practical roadmap before moving further",
    ],
    outcomes: [
      "A clearer view of where AI can create value",
      "A practical roadmap with priorities and next steps",
      "Better alignment across leadership, operations, and technology",
    ],
    engagements: [
      "Executive workshop",
      "Diagnostic and prioritisation",
      "Roadmap and action plan",
      "Follow-up advisory support",
    ],
    fit: [
      "Leadership teams exploring AI seriously",
      "Organisations modernising operations and decision-making",
      "Businesses that want a structured starting point",
    ],
    proofPoints: [
      "Business-led use-case framing",
      "Governance and delivery awareness",
      "Practical sequencing over hype",
    ],
  },
  {
    slug: "automation-digital-operations",
    title: "Automation & Digital Operations",
    shortTitle: "Automation",
    tagline: "Reduce friction, simplify operations, and improve the way work gets done.",
    summary: "Identify manual bottlenecks, redesign workflows, and support more efficient day-to-day operations.",
    intro:
      "This service focuses on operational efficiency first, using automation and better process design to make work simpler and more reliable.",
    bestFor: "Best for organisations dealing with repetitive effort, fragmented workflows, or operational drag.",
    clientProblems: [
      "Too much manual coordination across teams",
      "Processes are fragmented or inconsistent",
      "Digital operations need simplification before scaling further",
    ],
    outcomes: [
      "Less manual effort and fewer bottlenecks",
      "Clearer process flow and execution discipline",
      "A stronger operational base for future digital or AI work",
    ],
    engagements: [
      "Operational review",
      "Diagnostic and prioritisation",
      "Workflow design and action plan",
      "Implementation support",
    ],
    fit: [
      "Teams overloaded by manual tasks",
      "Businesses looking for practical efficiency gains",
      "Organisations modernising operations without overengineering",
    ],
    proofPoints: [
      "Process-first approach",
      "Practical automation opportunities",
      "Operational clarity before tool sprawl",
    ],
  },
  {
    slug: "delivery-pmo-project-service-management",
    title: "Delivery Governance, PMO & Service Management",
    shortTitle: "Delivery Governance",
    tagline: "Add structure, visibility, and follow-through to critical initiatives.",
    summary: "Strengthen governance, cadence, and coordination when delivery work needs more control.",
    intro:
      "This service supports programmes, projects, and service environments that need better structure, clearer visibility, and stronger follow-through.",
    bestFor: "Best for organisations under delivery pressure that need structure without adding unnecessary bureaucracy.",
    clientProblems: [
      "Initiatives are moving, but coordination is weak",
      "Priorities and ownership are not clear enough",
      "Leaders need better visibility across delivery and service issues",
    ],
    outcomes: [
      "Clearer governance and reporting cadence",
      "Better coordination across stakeholders and dependencies",
      "Stronger execution discipline around active work",
    ],
    engagements: [
      "Executive workshop",
      "Diagnostic and delivery stabilisation",
      "Governance model and action plan",
      "Ongoing PMO or service advisory support",
    ],
    fit: [
      "Programmes with multiple stakeholders or vendors",
      "Teams that need stronger project or service management discipline",
      "Leaders who want more control and clearer reporting",
    ],
    proofPoints: [
      "Governance and checkpoint design",
      "PMO and service management support",
      "Execution focus with practical cadence",
    ],
  },
  {
    slug: "fractional-cio-transformation-advisory",
    title: "Fractional CIO / Transformation Advisory",
    shortTitle: "Fractional CIO",
    tagline: "Bring senior technology leadership into critical decisions and delivery moments.",
    summary: "Access senior advisory support across strategy, modernization, governance, and executive decision-making.",
    intro:
      "This service is designed for organisations that need experienced technology and transformation guidance without making a full-time executive hire.",
    bestFor: "Best for organisations that need senior direction, but not a permanent executive role.",
    clientProblems: [
      "Technology decisions need stronger business alignment",
      "Modernization pressure is rising without enough senior guidance",
      "Leadership needs a steady advisory counterpart for critical choices",
    ],
    outcomes: [
      "Stronger technology and transformation decisions",
      "Clearer governance around delivery and modernization",
      "Senior support for leadership, vendors, and execution priorities",
    ],
    engagements: [
      "Executive workshop",
      "Strategic diagnostic",
      "Roadmap and action plan",
      "Fractional leadership or advisory follow-through",
    ],
    fit: [
      "Growing organisations that need senior technology perspective",
      "Leadership teams navigating modernization or vendor decisions",
      "Businesses needing guidance across strategy and execution",
    ],
    proofPoints: [
      "Executive-level guidance",
      "Business and technology alignment",
      "Flexible support model",
    ],
  },
] as const;

export const CASE_STUDY_ITEMS = [
  {
    id: "transformation-governance",
    label: "Transformation governance",
    href: `${CASE_STUDIES_PATH}#transformation-governance`,
    summary: "Examples of modernization work structured around governance, sequencing, and executive alignment.",
  },
  {
    id: "operational-efficiency",
    label: "Operational efficiency",
    href: `${CASE_STUDIES_PATH}#operational-efficiency`,
    summary: "Selected examples focused on simplification, delivery discipline, and day-to-day operational improvement.",
  },
  {
    id: "ai-enablement",
    label: "AI enablement",
    href: `${CASE_STUDIES_PATH}#ai-enablement`,
    summary: "Illustrative cases showing how AI and automation can be framed around practical business value.",
  },
] as const;

export const PROJECT_ITEMS = [
  {
    id: "fractional-leadership",
    label: "Fractional leadership",
    href: `${PROJECTS_PATH}#fractional-leadership`,
    summary: "Mission formats that bring senior technology and transformation guidance into critical periods.",
  },
  {
    id: "delivery-reinforcement",
    label: "Delivery reinforcement",
    href: `${PROJECTS_PATH}#delivery-reinforcement`,
    summary: "Project and PMO-oriented support for organisations under execution pressure.",
  },
  {
    id: "roadmaps-diagnostics",
    label: "Roadmaps and diagnostics",
    href: `${PROJECTS_PATH}#roadmaps-diagnostics`,
    summary: "Focused assessments used to clarify priorities, risks, and realistic next steps.",
  },
] as const;

export const INSIGHT_ITEMS = [
  {
    id: "advisory-notes",
    label: "Advisory notes",
    href: `${INSIGHTS_PATH}#advisory-notes`,
    summary: "Short perspectives on strategy, transformation, and technology leadership.",
  },
  {
    id: "ai-automation",
    label: "AI and automation",
    href: `${INSIGHTS_PATH}#ai-automation`,
    summary: "Views on practical adoption, operating-model impact, and business value.",
  },
  {
    id: "news-updates",
    label: "News and updates",
    href: `${INSIGHTS_PATH}#news-updates`,
    summary: "Selected updates on current work, themes, and evolving priorities.",
  },
] as const;

export const PUBLIC_SECTION_DEFINITIONS: PublicSectionDefinition[] = [
  {
    key: "services",
    label: "Services",
    shortLabel: "Services",
    path: "/services",
    description: "Core advisory offers across technology, delivery, transformation, and practical AI.",
    items: SERVICE_DEFINITIONS.map((service) => ({
      id: service.slug,
      label: service.shortTitle,
      href: `/services/${service.slug}`,
      summary: service.summary,
    })),
  },
  {
    key: "case-studies",
    label: "Case studies",
    shortLabel: "Case studies",
    path: CASE_STUDIES_PATH,
    description: "Illustrative examples of how advisory work translates into clearer decisions and stronger execution.",
    items: [...CASE_STUDY_ITEMS],
  },
  {
    key: "projects",
    label: "Projects",
    shortLabel: "Projects",
    path: PROJECTS_PATH,
    description: "Engagement shapes and project formats designed to support concrete delivery and change needs.",
    items: [...PROJECT_ITEMS],
  },
  {
    key: "insights",
    label: "Blog / News",
    shortLabel: "Blog / News",
    path: INSIGHTS_PATH,
    description: "Perspectives, notes, and updates across transformation, governance, technology, and AI.",
    items: [...INSIGHT_ITEMS],
  },
] as const;

const SECTION_PATHS: Array<[PublicSectionKey, string]> = [
  ["services", "/services"],
  ["case-studies", CASE_STUDIES_PATH],
  ["projects", PROJECTS_PATH],
  ["insights", INSIGHTS_PATH],
];

const LEGACY_SERVICE_SLUGS: Record<string, ServiceSlug> = {
  "fractional-cio/cdo-transformation-advisory": "fractional-cio-transformation-advisory",
};

export function normalizeServiceSlug(slug: string): ServiceSlug | null {
  if (slug in LEGACY_SERVICE_SLUGS) {
    return LEGACY_SERVICE_SLUGS[slug];
  }

  return SERVICE_DEFINITIONS.some((service) => service.slug === slug) ? (slug as ServiceSlug) : null;
}

export function getServiceDefinition(slug: ServiceSlug) {
  return SERVICE_DEFINITIONS.find((service) => service.slug === slug);
}

export function getSectionDefinition(key: PublicSectionKey) {
  return PUBLIC_SECTION_DEFINITIONS.find((section) => section.key === key);
}

export function getSectionKeyForPath(pathname: string): PublicSectionKey | null {
  for (const [key, path] of SECTION_PATHS) {
    if (pathname === path || pathname.startsWith(`${path}/`)) {
      return key;
    }
  }

  return null;
}
