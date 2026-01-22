<script lang="ts">
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import { authStore } from "$lib/stores/auth.store";

  import {
    Menu,
    User,
    Package,
    CreditCard,
    FileText,
    LogOut,
    Home
  } from "lucide-svelte";

  let sidebarOpen = false;

  const menuItems = [
    { icon: Home, label: "Dashboard", path: "/dashboard" },
    { icon: User, label: "Profile", path: "/dashboard/profile" },
    { icon: Package, label: "Orders", path: "/dashboard/orders" },
    { icon: CreditCard, label: "Payments", path: "/dashboard/payments" },
    { icon: FileText, label: "Order Form", path: "/dashboard/form" }
  ];

  function logout() {
    authStore.logout();
    goto("/signin");
  }
</script>

<div class="min-h-screen bg-gray-50">
  <!-- ================= MOBILE HEADER ================= -->
  <header
    class="lg:hidden h-16 flex items-center justify-between px-4 border-b bg-white"
  >
    <button on:click={() => (sidebarOpen = true)}>
      <Menu class="w-6 h-6" />
    </button>

    <div class="flex items-center gap-2">
      <img
        src="/src/lib/assets/images/logo1.png"
        alt="Logo"
        class="h-6 w-6"
      />
      <span class="font-bold text-lg">Order</span>
    </div>

    <div class="w-8" />
  </header>

  <!-- MOBILE OVERLAY -->
  {#if sidebarOpen}
    <div
      class="fixed inset-0 bg-black/40 z-40 lg:hidden"
      on:click={() => (sidebarOpen = false)}
    ></div>
  {/if}

  <!-- ================= SIDEBAR ================= -->
  <aside
    class={`fixed inset-y-0 left-0 z-50 w-72 bg-[#0b1f4b] text-white
    transform transition-transform
    ${sidebarOpen ? "translate-x-0" : "-translate-x-full"} lg:translate-x-0`}
  >
    <div class="flex flex-col h-full">
      <!-- BRAND -->
      <div
        class="h-16 flex items-center gap-3 px-6 border-b border-white/10"
      >
        <img
          src="/src/lib/assets/images/logo1.png"
          alt="Logo"
          class="h-10 w-10"
        />

        <div>
          <div class="font-bold text-lg">Order Menu</div>
          <div class="text-xs text-white/70">
            {#if $authStore.user}
              Welcome, {$authStore.user.full_name}
            {:else}
              Welcome
            {/if}
          </div>
        </div>
      </div>

      <!-- MENU -->
      <nav class="flex-1 px-3 py-4 space-y-1">
        {#each menuItems as item}
          <a
            href={item.path}
            class={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm
              ${
                $page.url.pathname === item.path
                  ? "bg-blue-600 text-white"
                  : "text-white/80 hover:bg-white/10"
              }`}
            on:click={() => (sidebarOpen = false)}
          >
            <item.icon class="w-5 h-5" />
            {item.label}
          </a>
        {/each}
      </nav>

      <!-- LOGOUT -->
      <div class="border-t border-white/10 p-4">
        <button
          class="flex items-center gap-3 text-sm text-white/80 hover:text-white"
          on:click={logout}
        >
          <LogOut class="w-5 h-5" />
          Logout
        </button>
      </div>
    </div>
  </aside>

  <!-- ================= MAIN CONTENT ================= -->
  <main class="lg:pl-72 p-6 lg:p-10 ml-4">
    <slot />
  </main>
</div>
