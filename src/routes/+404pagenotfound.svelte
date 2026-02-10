<script>
  import { page } from "$app/stores";
  import { onMount } from "svelte";

  // Log 404 path (same as useEffect + useLocation)
  onMount(() => {
    console.error(
      "404 Error: User attempted to access non-existent route:",
      $page.url.pathname
    );
  });
</script>

<div class="flex min-h-screen items-center justify-center bg-muted">
  <div class="text-center">
    <h1 class="mb-4 text-4xl font-bold">404</h1>
    <p class="mb-4 text-xl text-muted-foreground">
      Oops! Page not found
    </p>
    <a
      href="/"
      class="text-primary underline hover:text-primary/90"
    >
      Return to Home
    </a>
  </div>
</div>
