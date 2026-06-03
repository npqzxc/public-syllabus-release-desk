import { createApiClient } from "./api/client.js";
import { mountDashboard } from "./pages/dashboard.js";
import { mountVendors } from "./pages/vendors.js";
import { mountContractDetail } from "./pages/contract-detail.js";
import { mountNewContract } from "./pages/new-contract.js";
import { createStore } from "./utils/store.js";

const page = document.body.dataset.page;
const bootstrapElement = document.getElementById("page-bootstrap");
const bootstrap = bootstrapElement ? JSON.parse(bootstrapElement.textContent || "{}") : {};
const api = createApiClient();
const store = createStore({ page, bootstrap });

const mounts = {
  dashboard: mountDashboard,
  vendors: mountVendors,
  "contract-detail": mountContractDetail,
  "new-contract": mountNewContract,
};

if (mounts[page]) {
  mounts[page]({ api, store, bootstrap });
}
