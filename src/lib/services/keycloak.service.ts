import { apiRequest } from "./api";

export function getProductsService() {
  return apiRequest("/products/", {
    method: "GET",
  });
}
