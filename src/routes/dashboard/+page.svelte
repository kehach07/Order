<script lang="ts">
  import { onMount } from "svelte";
  import { getDashboardService } from "$lib/services/dashboard.service";

  let stats: any = null;
  let recentOrders: any[] = [];
  let loading = true;

  onMount(async () => {
    const data = await getDashboardService();
    stats = data;
    recentOrders = data.recent_orders;
    loading = false;
  });

  function formatDate(date: string) {
    return new Date(date).toLocaleDateString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric"
    });
  }

  function money(value: number) {
    return `₹${Number(value).toLocaleString("en-IN")}`;
  }
</script>

{#if loading}
  <p class="text-gray-500">Loading dashboard…</p>
{:else}

<!-- ================= HEADER ================= -->
<div class="mb-8 ml-4">
  <h1 class="text-3xl font-bold">Dashboard</h1>
  <p class="text-gray-500 mt-1">
    Overview of your orders and activity
  </p>
</div>

<!-- ================= STATS ================= -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
  <div class="p-5 rounded-xl border bg-white">
    <p class="text-sm text-gray-500">Total Orders</p>
    <p class="text-2xl font-bold mt-1">{stats.total_orders}</p>
  </div>

  <div class="p-5 rounded-xl border bg-white">
    <p class="text-sm text-gray-500">Active Orders</p>
    <p class="text-2xl font-bold mt-1 text-green-600">
      {stats.active_orders}
    </p>
  </div>

  <div class="p-5 rounded-xl border bg-white">
    <p class="text-sm text-gray-500">Completed</p>
    <p class="text-2xl font-bold mt-1 text-blue-600">
      {stats.completed_orders}
    </p>
  </div>

  <div class="p-5 rounded-xl border bg-white">
    <p class="text-sm text-gray-500">Cancelled</p>
    <p class="text-2xl font-bold mt-1 text-red-600">
      {stats.cancelled_orders}
    </p>
  </div>
</div>

<!-- ================= TOTAL AMOUNT ================= -->
<div class="mt-6 p-5 rounded-xl border bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
  <p class="text-sm opacity-80">Total Order Value</p>
  <p class="text-3xl font-bold mt-1">
    {money(stats.total_amount)}
  </p>
</div>

<!-- ================= RECENT ORDERS ================= -->
<div class="mt-10">
  <div class="flex justify-between items-center mb-4">
    <h2 class="text-xl font-semibold">Recent Orders</h2>
  </div>

  {#if recentOrders.length === 0}
    <p class="text-sm text-gray-500">No orders yet</p>
  {:else}

  <div class="space-y-4">
    {#each recentOrders as o}
      <div class="border rounded-xl p-5 bg-white">
        <!-- ORDER HEADER -->
        <div class="flex justify-between items-start">
          <div>
            <p class="font-mono font-medium">{o.order_id}</p>
            <p class="text-sm text-gray-500">
              {formatDate(o.created_at)}
            </p>
          </div>

          <div class="text-right">
            <p class="font-semibold">
              {money(o.net_amount)}
            </p>

            <span
              class={`inline-block mt-1 text-xs px-3 py-1 rounded-full
                ${o.status === "active" ? "bg-green-100 text-green-700" : ""}
                ${o.status === "completed" ? "bg-blue-100 text-blue-700" : ""}
                ${o.status === "cancelled" ? "bg-red-100 text-red-700" : ""}
              `}
            >
              {o.status}
            </span>
          </div>
        </div>

        <!-- ITEMS -->
        <div class="mt-4 border-t pt-3">
          <p class="text-sm font-medium mb-2">Items</p>
          <ul class="text-sm text-gray-600 space-y-1">
            {#each o.items as item}
              <li class="flex justify-between">
                <span>
                  {item.product_name} × {item.quantity}
                </span>
                <span>
                  {money(item.price * item.quantity)}
                </span>
              </li>
            {/each}
          </ul>
        </div>
      </div>
    {/each}
  </div>

  {/if}
</div>

{/if}
