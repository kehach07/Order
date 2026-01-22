<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import Search from "lucide-svelte/icons/search";
  import Package from "lucide-svelte/icons/package";
  import ChevronDown from "lucide-svelte/icons/chevron-down";

  import { getOrdersService } from "$lib/services/order.service";

  type OrderItem = {
    product_name: string;
    quantity: number;
    price: number;
  };

  type Order = {
    id: number;
    order_id: string;
    status: "active" | "completed" | "cancelled";
    items: OrderItem[];
    total_amount: number;
    gst_amount: number;
    net_amount: number;
    created_at: string;
  };

  let orders: Order[] = [];
  let expanded: number | null = null;
  let loading = true;
  let error = "";
  let search = "";

  onMount(async () => {
    try {
      orders = await getOrdersService();
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  });

  function toggle(id: number) {
    expanded = expanded === id ? null : id;
  }

  function formatDate(date: string) {
    return new Date(date).toLocaleDateString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric"
    });
  }

  $: filtered = orders.filter(o =>
    o.order_id.toLowerCase().includes(search.toLowerCase())
  );
</script>

<div class="space-y-6 ml-6">

  <!-- HEADER -->
  <div class="flex justify-between items-center">
    <div>
      <h1 class="text-3xl font-bold">Orders</h1>
      <p class="text-muted-foreground">Your purchase history</p>
    </div>

    <button
      class="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2"
      on:click={() => goto("/dashboard/form")}
    >
      <Package class="h-4 w-4" />
      New Order
    </button>
  </div>

  <!-- SEARCH -->
  <div class="relative max-w-md">
    <Search class="absolute left-3 top-3 h-4 w-4 text-gray-400" />
    <input
      class="pl-10 py-2 border rounded-lg w-full"
      placeholder="Search by Order ID"
      bind:value={search}
    />
  </div>

  {#if loading}
    <p class="text-gray-500">Loading orders…</p>
  {:else if error}
    <p class="text-red-500">{error}</p>
  {:else}

  {#each filtered as o}
    <div class="border rounded-lg p-4 space-y-3">

      <!-- ORDER HEADER -->
      <div
        class="flex justify-between items-center cursor-pointer"
        on:click={() => toggle(o.id)}
      >
        <div>
          <p class="font-mono font-medium">{o.order_id}</p>
          <p class="text-sm text-gray-500">{formatDate(o.created_at)}</p>
        </div>

        <div class="flex items-center gap-6">
          <div class="font-semibold">
            ₹{Number(o.net_amount).toLocaleString("en-IN")}
          </div>

          <span class={`px-3 py-1 rounded-full text-xs
            ${o.status === "active" ? "bg-green-100 text-green-700" : ""}
            ${o.status === "completed" ? "bg-blue-100 text-blue-700" : ""}
            ${o.status === "cancelled" ? "bg-red-100 text-red-700" : ""}
          `}>
            {o.status}
          </span>

          <ChevronDown
            class={`h-4 w-4 transition-transform
              ${expanded === o.id ? "rotate-180" : ""}
            `}
          />
        </div>
      </div>

      <!-- ITEMS -->
      {#if expanded === o.id}
        <div class="border-t pt-3 space-y-2">
          {#each o.items as item}
            <div class="flex justify-between text-sm">
              <span>
                {item.product_name} × {item.quantity}
              </span>
              <span>
                ₹{(item.price * item.quantity).toLocaleString("en-IN")}
              </span>
            </div>
          {/each}

          <hr />

          <div class="flex justify-between text-sm">
            <span>Subtotal</span>
            <span>₹{Number(o.total_amount).toLocaleString("en-IN")}</span>
          </div>

          <div class="flex justify-between text-sm">
            <span>GST (18%)</span>
            <span>₹{Number(o.gst_amount).toLocaleString("en-IN")}</span>
          </div>

          <div class="flex justify-between font-semibold">
            <span>Total</span>
            <span>₹{Number(o.net_amount).toLocaleString("en-IN")}</span>
          </div>
        </div>
      {/if}
    </div>
  {/each}


  {/if}
</div>
