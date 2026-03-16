/* Copyright (c) Dario Pizzolante */
export function formatDateTime(input: string): string {
  const value = new Date(input);
  if (Number.isNaN(value.getTime())) {
    return input;
  }

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(value);
}

export function formatConfidence(value: number): string {
  return `${Math.round(value * 100)}%`;
}

export function truncate(value: string, maxLength: number): string {
  if (value.length <= maxLength) {
    return value;
  }

  return `${value.slice(0, maxLength - 1)}...`;
}
