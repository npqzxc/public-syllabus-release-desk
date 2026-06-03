import { renderRenewalFeed } from "../components/renewal-feed.js";
import { renderRiskSummary } from "../components/risk-summary.js";
import { qs, setHtml } from "../utils/dom.js";

export async function mountDashboard({ api, bootstrap }) {
  const payload = await api.getDashboard().catch(() => bootstrap);
  setHtml(qs("#renewal-feed-panel"), renderRenewalFeed(payload));
  setHtml(qs("#risk-summary-panel"), renderRiskSummary(payload));
}
