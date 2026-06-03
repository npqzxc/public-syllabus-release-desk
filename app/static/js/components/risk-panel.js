export function renderRiskPanel(contract) {
  const items = (contract.risks || [])
    .map(
      (risk) => `
      <article class="insight-row">
        <strong>${risk.severity} · ${risk.title}</strong>
        <p>${risk.description}</p>
      </article>
    `,
    )
    .join("");

  return `
    <div class="panel-header"><h3>风险事项</h3><span>${contract.risks?.length || 0} 条</span></div>
    <div class="insight-list">${items || "<p>当前没有风险事项。</p>"}</div>
  `;
}
