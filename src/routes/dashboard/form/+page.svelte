<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  import Search from "lucide-svelte/icons/search";
  import Plus from "lucide-svelte/icons/plus";
  import Minus from "lucide-svelte/icons/minus";
  import Edit from "lucide-svelte/icons/edit";

  import { getProductsService } from "$lib/services/product.service";
  import {
    getAddressesService,
    createAddressService,
    updateAddressService
  } from "$lib/services/address.service";
  import { placeOrderService } from "$lib/services/order.service";

  /* ================= TYPES ================= */
  type Product = {
    id: number;
    name: string;
    price: number;
    category: string;
  };

  type Address = {
    id?: number;
    address_code?: string;
    address: string;
  };

  /* ================= STATE ================= */
  let products: Product[] = [];
  let cart: Array<Product & { qty: number }> = [];

  let loading = true;
  let error = "";
  let search = "";
  let showMessage = false;

  /* ================= ADDRESS ================= */
  let address: Address = {
    address: "No delivery address added yet.\nClick edit to add address."
  };

  let editing = false;
  let tempAddress = address.address;

  /* ================= LOAD DATA ================= */
  onMount(async () => {
    try {
      products = await getProductsService();

      const addresses = await getAddressesService();
      if (addresses.length > 0) {
        address = addresses[0];        // use first address
        tempAddress = address.address;
      }
    } catch (e: any) {
      error = e.message || "Failed to load data";
    } finally {
      loading = false;
    }
  });

  /* ================= CART ================= */
  function add(p: Product) {
    const item = cart.find(i => i.id === p.id);
    if (item) item.qty++;
    else cart = [...cart, { ...p, qty: 1 }];
  }

  function update(id: number, delta: number) {
    cart = cart
      .map(i =>
        i.id === id ? { ...i, qty: Math.max(0, i.qty + delta) } : i
      )
      .filter(i => i.qty > 0);
  }

  /* ================= ADDRESS SAVE ================= */
  async function saveAddress() {
    try {
      if (!tempAddress.trim()) {
        alert("Address cannot be empty");
        return;
      }

      if (address.id) {
        address = await updateAddressService(address.id, tempAddress);
      } else {
        address = await createAddressService(tempAddress);
      }
      editing = false;
    } catch (e: any) {
      alert(e.message || "Failed to save address");
    }
  }

  /* ================= ORDER ================= */
  async function placeOrder() {
    if (cart.length === 0) return;

    try {
      await placeOrderService(
        cart.map(i => ({
          product_id: i.id,
          quantity: i.qty
        })),
        address.id
      );

      showMessage = true;
      cart = [];

      setTimeout(() => goto("/dashboard/orders"), 1200);
    } catch (e: any) {
      alert(e.message || "Failed to place order");
    }
  }

  /* ================= DERIVED ================= */
  $: filteredProducts = products.filter(p =>
    p.name.toLowerCase().includes(search.toLowerCase()) ||
    p.category.toLowerCase().includes(search.toLowerCase())
  );

  $: subtotal = cart.reduce(
    (s, i) => s + Number(i.price) * i.qty,
    0
  );

  const GST_RATE = 0.18; // 🇮🇳 fixed GST
  $: gst = Math.round(subtotal * GST_RATE);
  $: total = subtotal + gst;
</script>

<!-- ================= PAGE ================= -->
<div class="space-y-8 ml-6">
  <h1 class="text-3xl font-bold">New Order</h1>
  <p class="text-muted-foreground">Search and add products to your order</p>

  {#if showMessage}
    <div class="bg-green-100 text-green-700 px-4 py-2 rounded">
      ✅ Order placed successfully!
    </div>
  {/if}

  {#if loading}
    <p class="text-gray-500">Loading...</p>
  {:else if error}
    <p class="text-red-500">{error}</p>
  {:else}

  <div class="grid grid-cols-3 gap-6">

    <!-- ================= PRODUCTS ================= -->
    <div class="col-span-2 space-y-4">

      <!-- SEARCH -->
      <div class="relative">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
        <input
          class="w-full pl-10 pr-3 py-2 border rounded"
          placeholder="Search products..."
          bind:value={search}
        />
      </div>

      {#each filteredProducts as p}
        <div class="p-4 border rounded-lg flex justify-between">
          <div>
            <p class="font-medium">{p.name}</p>
            <p class="text-sm text-gray-500">
              {p.category} · ₹{Number(p.price).toLocaleString()}
            </p>
          </div>

          <div class="flex items-center gap-2">
            {#if cart.find(i => i.id === p.id)}
              <button class="border px-2" on:click={() => update(p.id, -1)}>
                <Minus class="h-4 w-4" />
              </button>
              <span>{cart.find(i => i.id === p.id)?.qty}</span>
              <button class="border px-2" on:click={() => update(p.id, 1)}>
                <Plus class="h-4 w-4" />
              </button>
            {:else}
              <button class="border px-3 py-1 rounded" on:click={() => add(p)}>
                + Add
              </button>
            {/if}
          </div>
        </div>
      {/each}

      <!-- ================= ADDRESS ================= -->
      <div class="p-4 border rounded-lg space-y-2">
        <div class="flex justify-between items-center">
          <h2 class="font-semibold">Delivery Address</h2>
          <button on:click={() => (editing = true)}>
            <Edit class="h-4 w-4" />
          </button>
        </div>

        {#if editing}
          <textarea
            class="border w-full p-2 rounded"
            rows="4"
            bind:value={tempAddress}
          />
          <button class="mt-2 border px-3 py-1 rounded" on:click={saveAddress}>
            Save
          </button>
        {:else}
          <pre class="text-sm text-gray-500 whitespace-pre-line">
{address.address}
          </pre>
        {/if}
      </div>
    </div>

    <!-- ================= SUMMARY ================= -->
    <div class="border rounded-lg p-4 space-y-4">
      <h2 class="font-semibold">Order Summary</h2>

      {#each cart as i}
        <div class="flex justify-between text-sm">
          <span>{i.name} × {i.qty}</span>
          <span>₹{(Number(i.price) * i.qty).toLocaleString()}</span>
        </div>
      {/each}

      <hr />

      <div class="flex justify-between"><span>Subtotal</span><span>₹{subtotal}</span></div>
      <div class="flex justify-between"><span>GST (18%)</span><span>₹{gst}</span></div>

      <div class="flex justify-between font-bold text-lg">
        <span>Total</span><span>₹{total}</span>
      </div>

      <button
        class="w-full bg-blue-600 text-white py-2 rounded disabled:opacity-50"
        disabled={cart.length === 0}
        on:click={placeOrder}
      >
        Place Order
      </button>

      <button
        class="w-full border py-2 rounded"
        on:click={() => goto("/dashboard/orders")}
      >
        Cancel
      </button>
    </div>

  </div>
  {/if}
</div>
