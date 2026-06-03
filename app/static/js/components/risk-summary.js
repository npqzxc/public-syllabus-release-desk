import { money } from "../utils/format.js";

export function renderRiskSummary(payload) {
  const riskItems = (payload.risky_contracts || [])
    .map(
      (item) => `
      <article class="insight-row">
        <strong>${item.vendor_code} · ${item.title}</strong>
        <p>${item.severity} · ${item.created_at}</p>
      </article>
    `,
    )
    .join("");

  return `
    <div class="panel-header"><h3>风险概览</h3><span>${money(payload.annual_spend)}</span></div>
    <div class="insight-list">${riskItems}</div>
  `;
}
