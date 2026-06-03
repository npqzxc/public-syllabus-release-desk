export function renderContractRiskPanel(contract) {
  const flags = (contract.flags || [])
    .map(
      (flag) => `
      <article class="mini-card">
        <strong>${flag.severity} · ${flag.title}</strong>
        <p>${flag.description}</p>
        <span>${flag.created_at}</span>
      </article>
    `,
    )
    .join("");

  return `
    <div class="panel-header"><h2>风险旗标</h2><span>${contract.flags?.length || 0} 条</span></div>
    ${flags || "<p>当前没有风险旗标。</p>"}
  `;
}
