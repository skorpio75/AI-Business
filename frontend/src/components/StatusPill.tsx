/* Copyright (c) Dario Pizzolante */
import { Badge } from "./ui/badge";

type StatusTone = "neutral" | "warning" | "success" | "critical";

type StatusPillProps = {
  label: string;
  tone?: StatusTone;
};

export function StatusPill({ label, tone = "neutral" }: StatusPillProps) {
  return <Badge className={`status-pill status-pill--${tone}`}>{label}</Badge>;
}
