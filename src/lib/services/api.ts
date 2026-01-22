const BASE_URL = "http://127.0.0.1:8000/api";

export async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const access = localStorage.getItem("access");

  console.log("JWT ACCESS TOKEN 👉", access); // ✅ DEBUG

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(access ? { Authorization: `Bearer ${access}` } : {}),
  };

  console.log("REQUEST HEADERS 👉", headers); // ✅ DEBUG

  const res = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      ...headers,
      ...(options.headers || {}),
    },
  });

  if (!res.ok) {
    const error = await res.json();
    console.error("API ERROR 👉", error);
    throw new Error(error.detail || "Request failed");
  }

  return res.json();
}
