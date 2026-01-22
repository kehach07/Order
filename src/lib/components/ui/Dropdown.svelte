<script lang="ts">
  export let open = false;

  function toggle() {
    open = !open;
  }

  function close() {
    open = false;
  }

  function clickOutside(node: HTMLElement) {
    function handle(event: MouseEvent) {
      if (!node.contains(event.target as Node)) {
        close();
      }
    }
    document.addEventListener("click", handle, true);
    return {
      destroy() {
        document.removeEventListener("click", handle, true);
      }
    };
  }
</script>

<div class="relative inline-block" use:clickOutside>
  <slot name="trigger" {toggle} />

  {#if open}
    <div class="absolute right-0 mt-2 min-w-[160px] rounded-md border bg-white shadow-lg z-50">
      <slot name="content" {close} />
    </div>
  {/if}
</div>
