import { apiRequest } from "./api";

export function signupService(payload: {
  email: string;
  full_name: string;
  company: string;
  password: string;
}) {
  return apiRequest("/signup/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function signinService(payload: {
  email: string;
  password: string;
}) {
  return apiRequest("/signin/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
