export function renderRenewalFeed(payload) {
  const items = (payload.upcoming_contracts || [])
    .map(
      (item) => `
      <article class="feed-item">
        <strong>${item.vendor_code} · ${item.title}</strong>
        <p>${item.vendor_name}</p>
        <span>${item.renewal_date} · ${item.status}</span>
      </article>
    `,
    )
    .join("");

  return `
    <div class="panel-header"><h3>即将续约内容流程</h3><span>${payload.upcoming_contracts?.length || 0} 项</span></div>
    <div class="feed-list">${items}</div>
  `;
}
