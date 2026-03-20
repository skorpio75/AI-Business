/* Copyright (c) Dario Pizzolante */
import { type ReactNode } from "react";

type PublicImageHeroProps = {
  backHref: string;
  backLabel: string;
  kicker: string;
  title: string;
  lead: string;
  body?: ReactNode;
  actions?: ReactNode;
  panel?: ReactNode;
  heroClassName?: string;
  panelClassName?: string;
};

function joinClassNames(...values: Array<string | undefined>) {
  return values.filter(Boolean).join(" ");
}

export function PublicImageHero({
  backHref,
  backLabel,
  kicker,
  title,
  lead,
  body,
  actions,
  panel,
  heroClassName,
  panelClassName,
}: PublicImageHeroProps) {
  return (
    <section className={joinClassNames("image-hero", heroClassName)}>
      <div className="image-hero__content">
        <a className="back-link" href={backHref}>
          {backLabel}
        </a>
        <p className="site-kicker site-kicker--light">{kicker}</p>
        <h1>{title}</h1>
        <p className="image-hero__lead">{lead}</p>
        {body ? <div className="image-hero__body">{body}</div> : null}
        {actions ? <div className="image-hero__actions">{actions}</div> : null}
      </div>

      {panel ? (
        <aside className={joinClassNames("image-hero__panel", panelClassName)}>{panel}</aside>
      ) : null}
    </section>
  );
}
