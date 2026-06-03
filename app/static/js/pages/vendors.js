import { renderVendorSummary } from "../components/vendor-summary.js";
import { qs, setHtml } from "../utils/dom.js";

export async function mountVendors({ api }) {
  const payload = await api.getVendors(window.location.search);
  setHtml(qs("#vendor-filter-panel"), renderVendorSummary(payload));
}
