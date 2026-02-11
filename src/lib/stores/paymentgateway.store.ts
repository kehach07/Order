import { writable } from "svelte/store";
import { signupService, signinService } from "$lib/services/auth.service";
import {
  getProfileService,
  updateProfileService,
} from "$lib/services/profile.service";

export interface User {
  id: number;
  email: string;
  full_name: string;
  company: string;
  gst_number?: string;
  user_id: string;
  is_verified: boolean;
}

interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  loading: false,
  error: null,
};

function createAuthStore() {
  const { subscribe, update, set } = writable<AuthState>(initialState);

  return {
    subscribe,

    /* ---------- SIGNUP ---------- */
    signup: async (payload: {
      email: string;
      full_name: string;
      company: string;
      password: string;
    }) => {
      update((s) => ({ ...s, loading: true, error: null }));
      const res = await signupService(payload);
      update((s) => ({ ...s, loading: false }));
      return res;
    },

    /* ---------- SIGNIN (🔥 MAIN FIX) ---------- */
    signin: async (payload: { email: string; password: string }) => {
      update((s) => ({ ...s, loading: true, error: null }));

      const data = await signinService(payload);

      // ✅ STORE KEYCLOAK TOKENS
      localStorage.setItem("kc_access_token", data.access_token);
      localStorage.setItem("kc_refresh_token", data.refresh_token);

      // ✅ STORE USER
      localStorage.setItem("user", JSON.stringify(data.user));

      update((s) => ({
        ...s,
        user: data.user,
        loading: false,
      }));

      return data;
    },

    /* ---------- LOAD PROFILE ---------- */
    loadProfile: async () => {
      const token = localStorage.getItem("kc_access_token");
      if (!token) throw new Error("No access token");

      update((s) => ({ ...s, loading: true }));

      const data = await getProfileService();

      localStorage.setItem("user", JSON.stringify(data));

      update((s) => ({
        ...s,
        user: data,
        loading: false,
      }));

      return data;
    },

    /* ---------- UPDATE PROFILE ---------- */
    updateProfile: async (payload: {
      full_name: string;
      company: string;
      gst_number?: string;
    }) => {
      update((s) => ({ ...s, loading: true }));

      const data = await updateProfileService(payload);

      localStorage.setItem("user", JSON.stringify(data));

      update((s) => ({
        ...s,
        user: data,
        loading: false,
      }));

      return data;
    },

    /* ---------- HYDRATE ---------- */
    hydrate: () => {
      const user = localStorage.getItem("user");
      const token = localStorage.getItem("kc_access_token");

      if (user && token) {
        set({
          user: JSON.parse(user),
          loading: false,
          error: null,
        });
      }
    },

    /* ---------- LOGOUT ---------- */
    logout: () => {
      localStorage.clear();
      set(initialState);
      window.location.href = "/signin";
    },
  };
}

export const authStore = createAuthStore();
