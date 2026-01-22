<script lang="ts">
  export let variant: "default" | "success" | "muted" = "default";
</script>

<span
  class={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold
  ${variant === "default" ? "bg-blue-600 text-white" : ""}
  ${variant === "success" ? "bg-green-100 text-green-700" : ""}
  ${variant === "muted" ? "bg-gray-200 text-gray-600" : ""}`}
>
  <slot />
</span>
