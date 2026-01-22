import { apiRequest } from "./api";

export function getDashboardService() {
  return apiRequest("/dashboard/", { method: "GET" });
}
