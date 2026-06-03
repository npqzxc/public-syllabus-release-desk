export function renderVendorSummary(payload) {
  const filters = Object.entries(payload.filters || {})
    .map(([key, value]) => `<div class="insight-row"><strong>${key}</strong><p>${value}</p></div>`)
    .join("");

  return `
    <div class="panel-header"><h3>筛选摘要</h3><span>${payload.items?.length || 0} 家</span></div>
    <div class="insight-list">${filters || '<p>当前没有启用筛选条件。</p>'}</div>
  `;
}
