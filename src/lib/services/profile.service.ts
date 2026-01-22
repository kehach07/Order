import { apiRequest } from "./api";

export function getProfileService() {
  return apiRequest("/profile/", {
    method: "GET",
  });
}

export function updateProfileService(payload: {
  full_name: string;
  company: string;
  gst_number?: string;
}) {
  return apiRequest("/profile/", {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}
