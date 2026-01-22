import { apiRequest } from "./api";

export function placeOrderService(
  items: { product_id: number; quantity: number }[],
  addressId?: number
) {
  return apiRequest("/orders/", {
    method: "POST",
    body: JSON.stringify({
      items,
      address_id: addressId
    })
  });
}

export function getOrdersService() {
  return apiRequest("/orders/", { method: "GET" });
}