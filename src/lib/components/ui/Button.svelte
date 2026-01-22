<script lang="ts">
  export let variant:
    | "default"
    | "destructive"
    | "outline"
    | "secondary"
    | "ghost"
    | "link"
    | "gradient"
    | "success" = "default";

  export let size: "default" | "sm" | "lg" | "xl" | "icon" = "default";
  export let type: "button" | "submit" | "reset" = "button";

  const base =
    "inline-flex items-center justify-center gap-2 rounded-lg text-sm font-medium transition disabled:opacity-50";

  const variants = {
    default: "bg-primary text-white hover:bg-primary/90",
    outline: "border border-gray-300 hover:border-blue-600",
    gradient: "bg-blue-600 text-white hover:bg-blue-700",
  };

  const sizes = {
    default: "h-10 px-4",
    sm: "h-9 px-3",
    lg: "h-12 px-6",
  };
</script>

<button
  {type}
  class={`${base} ${variants[variant]} ${sizes[size]}`}
  on:click
>
  <slot />
</button>
