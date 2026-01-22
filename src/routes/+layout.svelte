<script lang="ts">
  // Global styles
  import "../app.css";

  // If you later add toast / tooltip libraries,
  // this is the correct place to mount them.
</script>

<!--
  Root layout for the entire app.
  Replaces:
  - App.jsx
  - BrowserRouter
  - Providers (React)
-->

<!-- Global UI Providers (optional, future-ready) -->
<!--
  Example later:
  <ToastContainer />
-->

<!-- App content -->
<slot />
