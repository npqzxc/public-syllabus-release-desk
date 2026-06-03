import { renderRiskPanel } from "../components/risk-panel.js";
import { qs, setHtml } from "../utils/dom.js";

export async function mountContractDetail({ api, bootstrap }) {
  if (!bootstrap.id) {
    return;
  }
  const payload = await api.getContract(bootstrap.id);
  setHtml(qs("#risk-panel"), renderRiskPanel(payload));
}
