<script lang="ts">
  import { onMount } from "svelte";
  import { authStore } from "$lib/stores/auth.store";

  import Button from "$lib/components/ui/Button.svelte";
  import Input from "$lib/components/ui/Input.svelte";

  import { Edit2, Shield, X } from "lucide-svelte";

  let showEditModal = false;
  let error = "";

  let form = {
    full_name: "",
    company: "",
    gst_number: "",
  };

  // Load logged-in user's profile
  onMount(async () => {
    try {
      await authStore.loadProfile();
    } catch (e) {
      console.error(e);
      error = "Authentication failed. Please sign in again.";
    }
  });

  function openEdit(user) {
    form = {
      full_name: user.full_name,
      company: user.company,
      gst_number: user.gst_number || "",
    };
    showEditModal = true;
  }

  async function saveProfile() {
    try {
      await authStore.updateProfile(form);
      showEditModal = false;
    } catch (e) {
      console.error(e);
      error = "Failed to update profile.";
    }
  }
</script>

<!-- ================= LOADING / ERROR ================= -->

{#if $authStore.loading}
  <p class="text-gray-500">Loading profile...</p>
{:else if error}
  <p class="text-red-500">{error}</p>
{:else if $authStore.user}

<!-- ================= PROFILE PAGE ================= -->

<div class="space-y-8 ml-6">

  <!-- HEADER -->
  <div class="flex items-center justify-between">
    <div>
      <h1 class="text-3xl font-bold">Profile</h1>
      <p class="text-gray-500 mt-1">Manage your account information</p>
    </div>

    <Button variant="outline" on:click={() => openEdit($authStore.user)}>
      <Edit2 class="w-4 h-4 mr-2" />
      Edit Profile
    </Button>
  </div>

  <!-- PROFILE GRID -->
  <div class="grid gap-6 lg:grid-cols-3">

    <!-- LEFT CARD -->
    <div class="bg-white rounded-xl shadow p-6 text-center">
      <div
        class="h-24 w-24 mx-auto rounded-full bg-blue-600 text-white
               flex items-center justify-center text-2xl font-bold mb-4"
      >
        {$authStore.user.full_name.slice(0, 2).toUpperCase()}
      </div>

      <h3 class="text-xl font-bold">{$authStore.user.full_name}</h3>
      <p class="text-sm text-gray-500">{$authStore.user.email}</p>
      <p class="text-sm text-blue-600 font-medium mt-1">
        {$authStore.user.company}
      </p>

      {#if $authStore.user.is_verified}
        <div
          class="inline-flex items-center gap-2 mt-4 px-3 py-1.5
                 rounded-full bg-green-100 text-green-700 text-sm"
        >
          <Shield class="w-4 h-4" />
          Verified Account
        </div>
      {/if}
    </div>

    <!-- RIGHT DETAILS -->
    <div class="bg-white rounded-xl shadow p-6 space-y-4 lg:col-span-2">

      <div class="grid grid-cols-3 gap-4">
        <p class="text-sm text-gray-500">User ID</p>
        <p class="col-span-2 font-mono">{$authStore.user.user_id}</p>
      </div>

      <div class="grid grid-cols-3 gap-4">
        <p class="text-sm text-gray-500">Full Name</p>
        <p class="col-span-2">{$authStore.user.full_name}</p>
      </div>

      <div class="grid grid-cols-3 gap-4">
        <p class="text-sm text-gray-500">Email</p>
        <p class="col-span-2">{$authStore.user.email}</p>
      </div>

      <div class="grid grid-cols-3 gap-4">
        <p class="text-sm text-gray-500">Company</p>
        <p class="col-span-2">{$authStore.user.company}</p>
      </div>

      <div class="grid grid-cols-3 gap-4">
        <p class="text-sm text-gray-500">GST Number</p>
        <p class="col-span-2 font-mono">
          {$authStore.user.gst_number || "—"}
        </p>
      </div>

    </div>
  </div>
</div>
{/if}

<!-- ================= EDIT PROFILE MODAL ================= -->

{#if showEditModal}
  <div class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
    <div class="bg-white rounded-xl w-full max-w-lg p-6 relative">

      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-bold">Edit Profile</h2>
        <button on:click={() => (showEditModal = false)}>
          <X class="w-5 h-5 text-gray-500" />
        </button>
      </div>

      <div class="space-y-4">
        <div>
          <label class="text-sm text-gray-500">Full Name</label>
          <Input bind:value={form.full_name} />
        </div>

        <div>
          <label class="text-sm text-gray-500">Company</label>
          <Input bind:value={form.company} />
        </div>

        <div>
          <label class="text-sm text-gray-500">GST Number</label>
          <Input bind:value={form.gst_number} />
        </div>
      </div>

      <div class="flex justify-end gap-3 mt-8">
        <Button variant="outline" on:click={() => (showEditModal = false)}>
          Cancel
        </Button>

        <Button variant="outline" class="bg-blue-600 text-white hover:bg-blue-700" on:click={saveProfile}>
          Save Changes
        </Button>
      </div>
    </div>
  </div>
{/if}
