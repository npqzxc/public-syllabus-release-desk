import { money } from "../utils/format.js";

export function renderVendorFilterSummary(payload) {
  const filters = Object.entries(payload.filters || {})
    .map(([key, value]) => `<div class="stat-row"><span>${key}</span><strong>${value}</strong></div>`)
    .join("");

  const totalSpend = (payload.items || []).reduce((sum, item) => sum + (item.active_spend || 0), 0);

  return `
    <div class="panel-header"><h2>筛选汇总</h2><span>${payload.items?.length || 0} 家</span></div>
    <div class="stat-list">
      ${filters || "<p>当前未启用任何筛选条件。</p>"}
      <div class="stat-row"><span>筛选后总支出</span><strong>${money(totalSpend)}</strong></div>
    </div>
  `;
}
