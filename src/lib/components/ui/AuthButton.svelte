<script lang="ts">
  export let type: "button" | "submit" = "submit";
  export let disabled = false;
</script>

<button
  {type}
  {disabled}
  class="
    w-full h-11
    inline-flex items-center justify-center gap-2
    rounded-lg
    bg-blue-600 text-white
    text-sm font-medium
    transition
    hover:bg-blue-700
    disabled:opacity-50 disabled:cursor-not-allowed
  "
>
  <slot />
</button>
