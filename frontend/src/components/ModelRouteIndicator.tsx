import { StatusPill } from "./StatusPill";

type ModelRouteIndicatorProps = {
  providerUsed: string;
  modelUsed: string;
  localLlmInvoked: boolean;
  cloudLlmInvoked: boolean;
  compact?: boolean;
};

function finalRouteTone(providerUsed: string): "neutral" | "success" | "warning" | "critical" {
  if (providerUsed === "local") {
    return "success";
  }
  if (providerUsed === "cloud") {
    return "warning";
  }
  if (providerUsed === "fallback-rule") {
    return "critical";
  }
  return "neutral";
}

function finalRouteLabel(providerUsed: string): string {
  if (providerUsed === "local") {
    return "final route local";
  }
  if (providerUsed === "cloud") {
    return "final route cloud";
  }
  if (providerUsed === "fallback-rule") {
    return "final route fallback";
  }
  return `final route ${providerUsed}`;
}

function routingSummary(
  providerUsed: string,
  localLlmInvoked: boolean,
  cloudLlmInvoked: boolean,
): string {
  if (providerUsed === "cloud" && localLlmInvoked) {
    return "Local was invoked first, then the workflow routed to cloud.";
  }
  if (providerUsed === "local") {
    return cloudLlmInvoked
      ? "Local produced the final result after a cloud attempt failed."
      : "Local produced the final result.";
  }
  if (providerUsed === "fallback-rule") {
    if (localLlmInvoked || cloudLlmInvoked) {
      return "LLM execution was attempted, but the final output fell back to rules.";
    }
    return "The final output came from fallback rules without a successful LLM path.";
  }
  if (cloudLlmInvoked) {
    return "The final output came from a cloud model.";
  }
  return "Routing information is available for this result.";
}

export function ModelRouteIndicator({
  providerUsed,
  modelUsed,
  localLlmInvoked,
  cloudLlmInvoked,
  compact = false,
}: ModelRouteIndicatorProps) {
  return (
    <div className={`routing-indicator${compact ? " routing-indicator--compact" : ""}`}>
      <div className="tag-cloud">
        <StatusPill label={finalRouteLabel(providerUsed)} tone={finalRouteTone(providerUsed)} />
        <StatusPill
          label={localLlmInvoked ? "local llm invoked" : "local llm not invoked"}
          tone={localLlmInvoked ? "success" : "neutral"}
        />
        <StatusPill
          label={cloudLlmInvoked ? "cloud llm invoked" : "cloud llm not invoked"}
          tone={cloudLlmInvoked ? "warning" : "neutral"}
        />
      </div>
      {!compact ? (
        <div className="routing-indicator__copy">
          <p className="muted-note">{routingSummary(providerUsed, localLlmInvoked, cloudLlmInvoked)}</p>
          <p className="muted-note">Model path: {modelUsed}</p>
        </div>
      ) : null}
    </div>
  );
}
