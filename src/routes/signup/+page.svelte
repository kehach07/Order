<script lang="ts">
  import { goto } from "$app/navigation";
  import {
    Eye,
    EyeOff,
    Mail,
    Lock,
    User,
    Building,
    ArrowRight
  } from "lucide-svelte";

  import { authStore } from "$lib/stores/auth.store";

  let showPassword = false;
  let loading = false;
  let error = "";

  let formData = {
    full_name: "",
    company: "",
    gst_number: "",
    email: "",
    password: ""
  };

  /* ================= REGEX ================= */
  const nameRegex = /^[A-Za-z ]{3,}$/;
  const companyRegex = /^[A-Za-z0-9 .,&-]{2,}$/;
  const gstRegex =
    /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$/;
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const passwordRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/;

  function validate() {
    if (!nameRegex.test(formData.full_name)) {
      error = "Enter a valid full name (min 3 letters).";
      return false;
    }
    if (formData.company && !companyRegex.test(formData.company)) {
      error = "Invalid company name.";
      return false;
    }
    if (!emailRegex.test(formData.email)) {
      error = "Invalid email address.";
      return false;
    }
    if (!passwordRegex.test(formData.password)) {
      error =
        "Password must be at least 8 characters with uppercase, lowercase, and number.";
      return false;
    }
    if (
      formData.gst_number &&
      !gstRegex.test(formData.gst_number.toUpperCase())
    ) {
      error = "Invalid GST number format.";
      return false;
    }
    return true;
  }

  async function submit() {
    error = "";
    if (!validate()) return;

    loading = true;
    try {
      await authStore.signup(formData);
      goto("/signin");
    } catch (e: any) {
      error = e.message || "Signup failed";
    } finally {
      loading = false;
    }
  }
</script>

<div class="min-h-screen flex">
  <!-- LEFT -->
  <div
    class="hidden lg:flex lg:w-1/2 items-center justify-center p-12
           bg-gradient-to-br from-[#0b1f4b] via-[#0a2a66] to-[#0a3b8a] text-white"
  >
    <div class="max-w-md text-center">
      <h1 class="text-5xl font-bold mb-6">Order</h1>
      <p class="text-white/80">
        Join thousands of businesses managing their orders efficiently.
      </p>
    </div>
  </div>

  <!-- RIGHT -->
  <div class="flex-1 flex items-center justify-center bg-gray-50 p-6">
    <div class="w-full max-w-md bg-white rounded-xl shadow-xl p-8">
      <h2 class="text-2xl font-bold text-center mb-1">Create an account</h2>
      <p class="text-sm text-gray-500 text-center mb-6">
        Get started with Order today
      </p>

      <form class="space-y-4" on:submit|preventDefault={submit}>
        <!-- Full Name -->
        <div>
          <label class="label">Full Name</label>
          <div class="field">
            <span class="icon-box"><User size={18} /></span>
            <input bind:value={formData.full_name} placeholder="John Doe" />
          </div>
        </div>

        <!-- Company 
        <div>
          <label class="label">Company Name</label>
          <div class="field">
            <span class="icon-box"><Building size={18} /></span>
            <input bind:value={formData.company} placeholder="Acme Inc." />
          </div>
        </div>
               -->
        <!-- GST 
        <div>
          <label class="label">GST Number</label>
          <div class="field">
            <span class="icon-box"><Building size={18} /></span>
            <input
              bind:value={formData.gst_number}
              placeholder="27AABCU9603R1ZM"
              on:input={() =>
                (formData.gst_number = formData.gst_number.toUpperCase())
              }
            />
          </div>
        </div>-->

        <!-- Email -->
        <div>
          <label class="label">Email</label>
          <div class="field">
            <span class="icon-box"><Mail size={18} /></span>
            <input
              type="email"
              bind:value={formData.email}
              placeholder="name@company.com"
            />
          </div>
        </div>

        <!-- Password -->
        <div>
          <label class="label">Password</label>
          <div class="field">
            <span class="icon-box"><Lock size={18} /></span>
            <input
              type={showPassword ? "text" : "password"}
              bind:value={formData.password}
              placeholder="••••••••"
            />
            <button
              type="button"
              class="eye"
              on:click={() => (showPassword = !showPassword)}
            >
              {#if showPassword}
                <EyeOff size={18} />
              {:else}
                <Eye size={18} />
              {/if}
            </button>
          </div>
        </div>

        {#if error}
          <p class="text-red-500 text-sm">{error}</p>
        {/if}

        <button
          type="submit"
          class="w-full h-12 bg-blue-600 text-white rounded-lg
                 flex items-center justify-center gap-2
                 hover:bg-blue-700 transition"
          disabled={loading}
        >
          {#if loading}
            Creating...
          {:else}
            Create Account <ArrowRight size={18} />
          {/if}
        </button>
      </form>

      <p class="text-sm text-center mt-6 text-gray-500">
        Already have an account?
        <a href="/signin" class="text-blue-600 hover:underline">Sign in</a>
      </p>
    </div>
  </div>
</div>

<style>
  .label {
    font-size: 0.875rem;
    font-weight: 500;
  }

  .field {
    position: relative;
    height: 48px;
  }

  .field input {
    width: 100%;
    height: 100%;
    padding-left: 48px;
    padding-right: 48px;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    outline: none;
    font-size: 14px;
  }

  .field input:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.25);
  }

  .icon-box {
    position: absolute;
    left: 0;
    top: 0;
    width: 48px;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #9ca3af;
    pointer-events: none;
  }

  .eye {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: #9ca3af;
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
