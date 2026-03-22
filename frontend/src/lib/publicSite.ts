/* Copyright (c) Dario Pizzolante */
export type ServiceSlug =
  | "ai-strategy-roadmapping"
  | "automation-digital-operations"
  | "delivery-pmo-project-service-management"
  | "fractional-cio-transformation-advisory";

export type ServicePillarKey =
  | "assessment-transformation-advisory"
  | "ai-automation-digital-operations"
  | "delivery-governance-execution-support";

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
  pillarKey: ServicePillarKey;
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

export type ServicePillarDefinition = {
  key: ServicePillarKey;
  title: string;
  href: string;
  homeSummary: string;
  servicesSummary: string;
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
  eyebrow: "Technology, AI and transformation advisory",
  title: "Clarity for transformation. Structure for delivery.",
  summary:
    "Stratevia helps organisations assess priorities, design practical roadmaps, and strengthen execution across technology, operations, and AI.",
  focusAreas: [
    "Assessment and prioritisation",
    "AI, automation and digital operations",
    "Delivery governance and execution support",
  ],
};

export const SERVICE_PILLARS: ServicePillarDefinition[] = [
  {
    key: "assessment-transformation-advisory",
    title: "Assessment & Transformation Advisory",
    homeSummary: "Clarify the current state, identify priorities, and define the most valuable path forward.",
    servicesSummary: "Clarify the current state, align priorities, and define the roadmap for change.",
    href: "/services#assessment-transformation-advisory",
  },
  {
    key: "ai-automation-digital-operations",
    title: "AI, Automation & Digital Operations",
    homeSummary: "Identify practical AI and automation opportunities, simplify operations, and build a realistic roadmap.",
    servicesSummary: "Turn AI and digital operations into practical initiatives with clear business value.",
    href: "/services#ai-automation-digital-operations",
  },
  {
    key: "delivery-governance-execution-support",
    title: "Delivery Governance & Execution Support",
    homeSummary: "Strengthen PMO, governance, coordination, and follow-through on critical initiatives.",
    servicesSummary: "Bring structure, visibility, and execution discipline to programmes and initiatives under pressure.",
    href: "/services#delivery-governance-execution-support",
  },
] as const;

export const HOW_I_WORK_STEPS = [
  {
    title: "Assess",
    summary: "Understand the context, constraints, delivery issues, and business priorities.",
  },
  {
    title: "Design",
    summary: "Define the roadmap, governance, and practical next steps.",
  },
  {
    title: "Deliver",
    summary: "Support execution with structure, cadence, and senior guidance.",
  },
] as const;

export const STRATEVIA_PROOF_POINTS = [
  {
    title: "Senior transformation leadership",
    summary: "Experience across IT leadership, governance, modernization, and operational change.",
  },
  {
    title: "Business-led technology perspective",
    summary: "Advice grounded in outcomes, not technology for its own sake.",
  },
  {
    title: "Structured execution support",
    summary: "Clear prioritisation, delivery discipline, and practical follow-through.",
  },
] as const;

export const SELECTED_BACKGROUND = [
  "Microsoft",
  "Unified Patent Court",
  "Societe Electrique de l'Our",
  "Net Service Lux",
] as const;

export const SELECTED_BACKGROUND_SUMMARY =
  "Experience spanning executive leadership, modernization, governance, and delivery in complex environments.";

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
  "I work with organisations that need senior advisory support to assess transformation priorities, shape AI and digital operations, and strengthen delivery governance when execution matters.";

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

export const ABOUT_PROFILE_TITLE =
  "Independent advisor in IT leadership, digital transformation, and AI-enabled operational improvement.";

export const ABOUT_SUMMARY = [
  "My background combines more than two decades of IT leadership, digital transformation, service management, and operational improvement across energy, technology consulting, legal-tech, finance, and public-sector environments.",
  "Across that experience, I have worked at both executive and delivery level: defining technology roadmaps, structuring governance, leading complex programmes, managing IT operations and budgets, and guiding multidisciplinary teams in international settings where clarity, coordination, and follow-through matter.",
  "That includes helping establish the IT function and operating model for the Unified Patent Court across 25 member states, leading modernization and cloud-transition initiatives as Head of IT at Societe Electrique de l'Our, developing digitalization and AI-enabled offerings as Managing Director of Net Service Lux, and building a strong consulting and service-delivery foundation earlier in my career at Microsoft and other enterprise environments.",
  "Today, organisations typically engage when they need clearer transformation priorities, a practical roadmap for digitalization or AI adoption, stronger delivery governance, or senior support to improve operations without adding unnecessary complexity.",
  "My approach stays business-led, executive, and well rounded: I bring enough technical depth to work credibly with delivery teams, while keeping the focus on decision-making, governance, business efficiency, and practical adoption.",
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
    title: "Master of Business Administration (partially completed)",
    institution: "Imperial College London",
    period: "2011 to 2012",
  },
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

export const ABOUT_LANGUAGES = [
  "French: C2",
  "German: C1",
  "English: C2",
  "Italian: C1",
  "Luxembourgish: C2",
] as const;

export const ABOUT_ROTARY = {
  title: "Rotary Club Strassen-Bertrange-Mamer",
  period: "2023 to present",
  summary:
    "Founding member, committee member, and Chair of the Membership Committee.",
} as const;

export const CONTACT_REASONS = [
  "Transformation priorities or modernization choices need clarity",
  "AI or digital operations need a practical roadmap",
  "Delivery governance or PMO support is needed on a critical initiative",
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
    pillarKey: "ai-automation-digital-operations",
    title: "AI Strategy & Roadmapping",
    shortTitle: "AI Strategy",
    tagline: "Move from AI interest to a focused roadmap with practical business value.",
    summary: "Clarify the most valuable AI use cases, priorities, and delivery path before investing in disconnected ideas.",
    intro:
      "This service helps organisations approach AI with clarity, realism, and a business-led sequence so adoption supports operations, decision-making, and measurable outcomes.",
    bestFor: "Best for organisations that need a practical AI roadmap before committing time and budget to initiatives.",
    clientProblems: [
      "AI interest exists, but priorities are unclear",
      "Use cases feel disconnected from business priorities or operational reality",
      "Leadership wants a practical roadmap before moving further",
    ],
    outcomes: [
      "A clearer view of where AI can create business value",
      "A practical roadmap with priorities, sequencing, and next steps",
      "Better alignment across leadership, operations, and technology teams",
    ],
    engagements: [
      "Executive workshop",
      "AI opportunity diagnostic and prioritisation",
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
    pillarKey: "ai-automation-digital-operations",
    title: "Automation & Digital Operations",
    shortTitle: "Digital Operations",
    tagline: "Reduce friction, simplify operations, and improve the way work gets done.",
    summary: "Identify manual bottlenecks, simplify workflows, and improve day-to-day operations with practical automation.",
    intro:
      "This service focuses on operational efficiency first, using automation and better process design to make work simpler, more reliable, and easier to scale.",
    bestFor: "Best for organisations dealing with repetitive effort, fragmented workflows, or inefficient digital operations.",
    clientProblems: [
      "Too much manual coordination across teams",
      "Processes are fragmented or inconsistent",
      "Digital operations need simplification before scaling further",
    ],
    outcomes: [
      "Less manual effort and fewer operational bottlenecks",
      "Clearer workflows with stronger day-to-day execution discipline",
      "A stronger operational foundation for future digital or AI work",
    ],
    engagements: [
      "Operational review",
      "Operational diagnostic and prioritisation",
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
    pillarKey: "delivery-governance-execution-support",
    title: "Delivery Governance, PMO & Service Management",
    shortTitle: "Delivery Governance",
    tagline: "Add structure, visibility, and follow-through to critical initiatives.",
    summary: "Strengthen governance, cadence, and coordination when delivery work needs more visibility and control.",
    intro:
      "This service supports programmes, projects, and service environments that need better structure, clearer visibility, and stronger execution discipline.",
    bestFor: "Best for organisations under delivery pressure that need structure without adding unnecessary bureaucracy.",
    clientProblems: [
      "Initiatives are moving, but coordination is weak",
      "Priorities and ownership are not clear enough",
      "Leaders need better visibility across delivery and service issues",
    ],
    outcomes: [
      "Clearer governance and reporting cadence",
      "Better coordination across stakeholders and dependencies",
      "Stronger execution discipline across active work and service priorities",
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
    pillarKey: "assessment-transformation-advisory",
    title: "Fractional CIO / Transformation Advisory",
    shortTitle: "Transformation Advisory",
    tagline: "Bring senior transformation and technology leadership to assessment, prioritisation, and roadmap decisions.",
    summary: "Access senior advisory support to assess the current state, clarify priorities, and shape a practical transformation path.",
    intro:
      "This service is designed for organisations that need experienced technology and transformation guidance to assess where they are, decide what matters most, and move forward with a realistic roadmap without making a full-time executive hire.",
    bestFor: "Best for organisations that need senior transformation direction, but not a permanent executive role.",
    clientProblems: [
      "Transformation priorities are not yet clear enough",
      "Technology decisions need stronger business alignment",
      "Leadership needs a senior advisory counterpart for critical modernization choices",
    ],
    outcomes: [
      "A clearer view of priorities, risks, and transformation options",
      "Stronger technology and transformation decisions",
      "A practical roadmap for modernization, governance, and next steps",
    ],
    engagements: [
      "Executive workshop",
      "Current-state and strategic diagnostic",
      "Roadmap and action plan",
      "Fractional leadership or advisory follow-through",
    ],
    fit: [
      "Leadership teams navigating transformation or modernization decisions",
      "Organisations that need senior technology perspective without a full-time hire",
      "Businesses that need clearer direction before major execution commitments",
    ],
    proofPoints: [
      "Executive-level assessment and guidance",
      "Business and technology alignment",
      "Flexible advisory or fractional support model",
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
    description:
      "Three advisory pillars spanning assessment, AI and automation, and delivery governance support.",
    items: SERVICE_PILLARS.map((pillar) => ({
      id: pillar.key,
      label: pillar.title,
      href: pillar.href,
      summary: pillar.servicesSummary,
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

export function getServicesForPillar(pillarKey: ServicePillarKey) {
  return SERVICE_DEFINITIONS.filter((service) => service.pillarKey === pillarKey);
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
