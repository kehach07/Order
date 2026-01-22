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

    /* ---------- SIGNIN ---------- */
    signin: async (payload: { email: string; password: string }) => {
      update((s) => ({ ...s, loading: true, error: null }));

      const data = await signinService(payload);

      // ✅ STORE JWT
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
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
      const access = localStorage.getItem("access");
      if (!access) throw new Error("No access token");

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

    /* ---------- UPDATE PROFILE (✅ FIXED) ---------- */
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
      if (user) {
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
    },
  };
}

export const authStore = createAuthStore();
