export function createApiClient() {
  async function getJson(path) {
    const response = await fetch(path, { headers: { Accept: "application/json" } });
    if (!response.ok) {
      throw new Error(`Request failed: ${response.status}`);
    }
    return response.json();
  }

  return {
    getDashboard() {
      return getJson("/api/dashboard");
    },
    getVendors(search = "") {
      return getJson(`/api/vendors${search}`);
    },
    getContract(contractId) {
      return getJson(`/api/contracts/${contractId}`);
    },
  };
}
