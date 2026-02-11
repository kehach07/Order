const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function signupService(payload: {
  email: string;
  full_name: string;
  company: string;
  password: string;
}) {
  const res = await fetch(`${BASE_URL}/signup/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Signup failed");
  }

  return data;
}

export async function signinService(payload: {
  email: string;
  password: string;
}) {
  const res = await fetch(`${BASE_URL}/signin/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Signin failed");
  }

  // ✅ save tokens ONLY after successful signin
  localStorage.setItem("access", data.access);
  localStorage.setItem("refresh", data.refresh);

  return data;
}
export async function signinService(payload: {
  email: string;
  password: string;
}) {
  const res = await fetch(`${BASE_URL}/signin/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Signin failed");
  }

  // ✅ save tokens ONLY after successful signin
  localStorage.setItem("access", data.access);
  localStorage.setItem("refresh", data.refresh);

  return data;
}