/* Copyright (c) Dario Pizzolante */
import { startTransition, useEffect, useState } from "react";
import {
  Activity,
  Bot,
  CheckCheck,
  Inbox,
  Mail,
  Menu,
  Network,
  RefreshCcw,
  Search,
  Sparkles,
  X,
} from "lucide-react";

import { Button } from "./components/ui/button";
import { AgentActivityPage } from "./pages/AgentActivityPage";
import { AgentsOrgPage } from "./pages/AgentsOrgPage";
import { EmailOperationsPage } from "./pages/EmailOperationsPage";
import { InboxCalendarPage } from "./pages/InboxCalendarPage";
import { KnowledgeQnaPage } from "./pages/KnowledgeQnaPage";
import { ProposalGenerationPage } from "./pages/ProposalGenerationPage";
import { ApprovalQueuePage } from "./pages/ApprovalQueuePage";
import { ChiefAiStrategyPage } from "./pages/ChiefAiStrategyPage";
import { CtoCioPage } from "./pages/CtoCioPage";
import { FinanceCockpitPage } from "./pages/FinanceCockpitPage";
import { WorkflowMonitorPage } from "./pages/WorkflowMonitorPage";
import type { ViewKey } from "./types";

type ViewDefinition = {
  id: ViewKey;
  label: string;
  description: string;
  icon: typeof Network;
};

const VIEW_GROUPS: Array<{
  id: string;
  title: string;
  description: string;
  views: ViewDefinition[];
}> = [
  {
    id: "oversight",
    title: "Oversight",
    description: "Stay on top of live work, approvals, and intervention points.",
    views: [
      {
        id: "workflow-monitor",
        label: "Workflow Monitor",
        description: "Track workflow throughput, model routing, and escalations.",
        icon: Network,
      },
      {
        id: "approval-queue",
        label: "Approval Queue",
        description: "Review pending decisions and resolve them from the UI.",
        icon: CheckCheck,
      },
    ],
  },
  {
    id: "communications",
    title: "Communications",
    description: "Handle inbox-driven work and manual email drafting in one place.",
    views: [
      {
        id: "inbox-calendar",
        label: "Inbox + Calendar",
        description: "Read live Outlook context and launch reply workflows from real messages.",
        icon: Inbox,
      },
      {
        id: "email-operations",
        label: "Manual Email Draft",
        description: "Run the email workflow from scratch when there is no live inbox source.",
        icon: Mail,
      },
    ],
  },
  {
    id: "knowledge-delivery",
    title: "Knowledge and Delivery",
    description: "Research internal context and build first-pass client material.",
    views: [
      {
        id: "knowledge-qna",
        label: "Knowledge Q&A",
        description: "Run grounded internal Q&A against the knowledge store.",
        icon: Search,
      },
      {
        id: "proposal-generation",
        label: "Proposal Drafts",
        description: "Create a baseline consulting proposal from opportunity context.",
        icon: Sparkles,
      },
      {
        id: "cto-cio",
        label: "CTO/CIO",
        description: "Review architecture guidance, strategy options, and internal tech priorities.",
        icon: Sparkles,
      },
      {
        id: "finance-cockpit",
        label: "Finance Cockpit",
        description: "Review accounting exceptions, close readiness, and CFO scenario cards.",
        icon: Sparkles,
      },
      {
        id: "chief-ai-strategy",
        label: "AI Strategy",
        description: "Review AI opportunity maps, delivery blueprinting, and maturity signals.",
        icon: Sparkles,
      },
    ],
  },
  {
    id: "agents",
    title: "Agents",
    description: "Inspect the roster, runtime state, and operating model of available agents.",
    views: [
      {
        id: "agent-activity",
        label: "Agent Activity",
        description: "Inspect registered agents, runtime states, and deployment policies.",
        icon: Activity,
      },
      {
        id: "agents-org",
        label: "Agent Directory",
        description: "See corporate and delivery agents as an operating roster.",
        icon: Bot,
      },
    ],
  },
];

const NAV_COMPACT_BREAKPOINT = 960;

export default function App() {
  const [activeView, setActiveView] = useState<ViewKey>("workflow-monitor");
  const [refreshToken, setRefreshToken] = useState(0);
  const [isCompactNav, setIsCompactNav] = useState(
    () => typeof window !== "undefined" && window.innerWidth <= NAV_COMPACT_BREAKPOINT,
  );
  const [isNavOpen, setIsNavOpen] = useState(
    () => typeof window === "undefined" || window.innerWidth > NAV_COMPACT_BREAKPOINT,
  );

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }

    const mediaQuery = window.matchMedia(`(max-width: ${NAV_COMPACT_BREAKPOINT}px)`);
    const syncLayout = (matches: boolean) => {
      setIsCompactNav(matches);
      setIsNavOpen(matches ? false : true);
    };

    syncLayout(mediaQuery.matches);

    const handleChange = (event: MediaQueryListEvent) => {
      syncLayout(event.matches);
    };

    mediaQuery.addEventListener("change", handleChange);
    return () => {
      mediaQuery.removeEventListener("change", handleChange);
    };
  }, []);

  function handleViewSelect(viewId: ViewKey) {
    startTransition(() => {
      setActiveView(viewId);
    });
    if (isCompactNav) {
      setIsNavOpen(false);
    }
  }

  return (
    <div className="app-shell">
      {isCompactNav && isNavOpen ? (
        <button
          aria-label="Close navigation"
          className="nav-scrim"
          type="button"
          onClick={() => setIsNavOpen(false)}
        />
      ) : null}

      <header className="app-header">
        <div>
          <p className="eyebrow">Enterprise Agent Platform</p>
          <h1>Mission Control</h1>
        </div>
        <div className="header-actions">
          {isCompactNav ? (
            <Button
              aria-controls="mission-control-nav"
              aria-expanded={isNavOpen}
              className="nav-toggle"
              type="button"
              variant="secondary"
              onClick={() => setIsNavOpen((value) => !value)}
            >
              {isNavOpen ? <X className="size-4" /> : <Menu className="size-4" />}
              {isNavOpen ? "Close menu" : "Open menu"}
            </Button>
          ) : null}
          <Button className="refresh-button" type="button" onClick={() => setRefreshToken((value) => value + 1)}>
            <RefreshCcw className="size-4" />
            Refresh data
          </Button>
        </div>
      </header>

      <main className="app-main">
        <aside
          className={`nav-panel ${isCompactNav ? "nav-panel--compact" : ""} ${isNavOpen ? "nav-panel--open" : ""}`}
          id="mission-control-nav"
        >
          <div className="nav-panel__intro">
            <p className="eyebrow">Operator views</p>
            <h2>Control surface</h2>
            <p>
              The cockpit is grouped by operating task so communication, oversight, and agent
              views are easier to scan.
            </p>
          </div>
          <nav className="view-nav-groups" aria-label="Mission control views">
            {VIEW_GROUPS.map((group) => (
              <section key={group.id} className="view-nav__group" aria-labelledby={`nav-group-${group.id}`}>
                <div className="view-nav__group-header">
                  <p id={`nav-group-${group.id}`} className="view-nav__group-title">
                    {group.title}
                  </p>
                  <span className="view-nav__group-copy">{group.description}</span>
                </div>
                <div className="view-nav">
                  {group.views.map((view) => {
                    const Icon = view.icon;

                    return (
                      <Button
                        key={view.id}
                        className={`view-nav__item ${activeView === view.id ? "view-nav__item--active" : ""}`}
                        variant="ghost"
                        type="button"
                        onClick={() => handleViewSelect(view.id)}
                      >
                        <span className="view-nav__icon">
                          <Icon className="size-4" />
                        </span>
                        <span className="view-nav__copy">
                          <strong>{view.label}</strong>
                          <span>{view.description}</span>
                        </span>
                      </Button>
                    );
                  })}
                </div>
              </section>
            ))}
          </nav>
          <div className="nav-panel__footer">
            <span>API base</span>
            <code>{import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"}</code>
          </div>
        </aside>

        <div className="view-panel">
          {activeView === "workflow-monitor" ? (
            <WorkflowMonitorPage refreshToken={refreshToken} />
          ) : null}
          {activeView === "approval-queue" ? (
            <ApprovalQueuePage refreshToken={refreshToken} />
          ) : null}
          {activeView === "agent-activity" ? (
            <AgentActivityPage refreshToken={refreshToken} />
          ) : null}
          {activeView === "agents-org" ? <AgentsOrgPage refreshToken={refreshToken} /> : null}
          {activeView === "inbox-calendar" ? (
            <InboxCalendarPage
              refreshToken={refreshToken}
              onDrafted={() => setRefreshToken((value) => value + 1)}
            />
          ) : null}
          {activeView === "email-operations" ? (
            <EmailOperationsPage onCreated={() => setRefreshToken((value) => value + 1)} />
          ) : null}
          {activeView === "knowledge-qna" ? <KnowledgeQnaPage /> : null}
          {activeView === "proposal-generation" ? <ProposalGenerationPage /> : null}
          {activeView === "cto-cio" ? <CtoCioPage refreshToken={refreshToken} /> : null}
          {activeView === "finance-cockpit" ? <FinanceCockpitPage refreshToken={refreshToken} /> : null}
          {activeView === "chief-ai-strategy" ? <ChiefAiStrategyPage refreshToken={refreshToken} /> : null}
        </div>
      </main>
    </div>
  );
}
