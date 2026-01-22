import { apiRequest } from "./api";

export function getAddressesService() {
  return apiRequest("/addresses/", { method: "GET" });
}

export function createAddressService(address: string) {
  return apiRequest("/addresses/", {
    method: "POST",
    body: JSON.stringify({ address })
  });
}

export function updateAddressService(id: number, address: string) {
  return apiRequest(`/addresses/${id}/`, {
    method: "PUT",
    body: JSON.stringify({ address })
  });
}
