/* Copyright (c) Dario Pizzolante */
import type { GovernedMetadataSummary } from "../types";

type GovernedMetadataBlockProps = {
  metadata: GovernedMetadataSummary;
  showToolProfiles?: boolean;
};

export function GovernedMetadataBlock({
  metadata,
  showToolProfiles = true,
}: GovernedMetadataBlockProps) {
  return (
    <>
      <div className="callout callout--soft">
        <p className="eyebrow">Operating model</p>
        <strong>{metadata.operating_model_label}</strong>
        <span className="muted-note">{metadata.operating_model_summary}</span>
      </div>

      <div className="callout callout--soft">
        <p className="eyebrow">Governed routing posture</p>
        <strong>
          {metadata.routing_posture_label} ({metadata.routing_posture})
        </strong>
        <span className="muted-note">{metadata.routing_posture_summary}</span>
      </div>

      <div className="tag-cloud">
        {metadata.primary_track_label ? <span className="tag-chip">{metadata.primary_track_label}</span> : null}
        {metadata.pod_label ? <span className="tag-chip">{metadata.pod_label}</span> : null}
        {metadata.family_label ? <span className="tag-chip">{metadata.family_label}</span> : null}
        {metadata.replication_label ? <span className="tag-chip">{metadata.replication_label}</span> : null}
      </div>

      {showToolProfiles && metadata.tool_profiles.length > 0 ? (
        <div className="mini-list">
          <p className="eyebrow">Tool profiles</p>
          <ul>
            {metadata.tool_profiles.map((profile) => (
              <li key={`${profile.operating_mode}-${profile.profile_id}`}>
                <strong>{profile.operating_mode_label}</strong>: {profile.profile_id} - {profile.profile_summary}
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </>
  );
}
