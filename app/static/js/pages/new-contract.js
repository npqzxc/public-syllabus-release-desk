import { renderContractPreview } from "../components/contract-preview.js";
import { qs, setHtml } from "../utils/dom.js";

export function mountNewContract() {
  const form = qs("#contract-form");
  const panel = qs("#contract-preview-panel");
  if (!form || !panel) {
    return;
  }

  const update = () => {
    const values = Object.fromEntries(new FormData(form).entries());
    setHtml(panel, renderContractPreview(values));
  };

  form.addEventListener("input", update);
  form.addEventListener("change", update);
  update();
}
