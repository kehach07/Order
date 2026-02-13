<script lang="ts">
  export let type = "text";
  export let value: string | number = "";
  export let placeholder = "";
  export let className = "";
  export let disabled = false;
</script>
<input
  {type}
  bind:value
  {placeholder}
  {disabled}
  class="
    w-full
    h-12
    rounded-lg
    border
    border-input
    bg-background
    px-3
    py-2
    text-sm
    text-foreground
    placeholder:text-muted-foreground

    focus:outline-none
    focus:ring-2
    focus:ring-primary/40
    focus:border-primary

    hover:border-primary/60
    transition

    disabled:cursor-not-allowed
    disabled:opacity-50

    {className}
  "
/>
<input
  {type}
  bind:value
  {placeholder}
  {disabled}
  class="
    w-full
    h-12
    rounded-lg
    border
    border-input
    bg-background
    px-3
    py-2
    text-sm
    text-foreground
    placeholder:text-muted-foreground

    focus:outline-none
    focus:ring-2
    focus:ring-primary/40
    focus:border-primary

    hover:border-primary/60
    transition

    disabled:cursor-not-allowed
    disabled:opacity-50

    {className}
  "
/>
