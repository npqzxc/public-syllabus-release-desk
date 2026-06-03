export function renderContractPreview(formState) {
  return `
    <div class="panel-header"><h3>提交预览</h3><span>${formState.status || "draft"}</span></div>
    <article class="preview-card">
      <strong>${formState.title || "未填写内容流程标题"}</strong>
      <p>课程 ID：${formState.vendor_id || "-"}</p>
      <p>年支出：${formState.annual_spend || "-"}</p>
      <p>续约日期：${formState.renewal_date || "-"}</p>
      <p>SLA：${formState.sla_level || "-"}</p>
    </article>
  `;
}
