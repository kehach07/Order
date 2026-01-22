<script lang="ts">
  export let value = "";
  export let options: { value: string; label: string }[] = [];
  export let placeholder = "Select";
</script>

<select
  bind:value
  class="w-full h-12 rounded-md border bg-background px-3"
>
  <option value="" disabled selected>{placeholder}</option>
  {#each options as opt}
    <option value={opt.value}>{opt.label}</option>
  {/each}
</select>
