<script lang="ts">
  import { goto } from "$app/navigation";
  import { Eye, EyeOff, Mail, Lock, ArrowRight } from "lucide-svelte";
  import { authStore } from "$lib/stores/auth.store";

  import Card from "$lib/components/ui/Card.svelte";
  import CardHeader from "$lib/components/ui/CardHeader.svelte";
  import CardTitle from "$lib/components/ui/CardTitle.svelte";
  import CardDescription from "$lib/components/ui/CardDescription.svelte";
  import CardContent from "$lib/components/ui/CardContent.svelte";
  import AuthButton from "$lib/components/ui/AuthButton.svelte";
  import Input from "$lib/components/ui/Input.svelte";

  let showPassword = false;
  let email = "";
  let password = "";
  let error = "";
  let loading = false;

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  async function submit() {
    error = "";

    if (!email || !password) {
      error = "Email and password are required.";
      return;
    }

    if (!emailRegex.test(email)) {
      error = "Enter a valid email address.";
      return;
    }

    loading = true;

    try {
      // ✅ REAL AUTHENTICATION
      await authStore.signin({ email, password });

      // ✅ ONLY AFTER SUCCESS
      goto("/dashboard");
    } catch (e: any) {
      // ❌ WRONG EMAIL OR PASSWORD
      error = e.message || "Invalid email or password";
    } finally {
      loading = false;
    }
  }
</script>


<div class="min-h-screen flex">
  <!-- LEFT BRAND PANEL -->
  <div class="hidden lg:flex lg:w-1/2 gradient-hero items-center justify-center p-12 text-white">
    <div class="max-w-md text-center animate-fade-in">
      <h1 class="text-5xl font-bold mb-6">Order</h1>

      <p class="text-lg text-white/80">
        Streamline your order management with our powerful and intuitive platform.
      </p>

      <div class="mt-12 grid grid-cols-3 gap-8">
        <div>
          <div class="text-3xl font-bold">500+</div>
          <div class="text-sm opacity-80">Active Users</div>
        </div>
        <div>
          <div class="text-3xl font-bold">10K+</div>
          <div class="text-sm opacity-80">Orders</div>
        </div>
        <div>
          <div class="text-3xl font-bold">99%</div>
          <div class="text-sm opacity-80">Uptime</div>
        </div>
      </div>
    </div>
  </div>

  <!-- RIGHT FORM PANEL -->
  <div class="flex-1 flex items-center justify-center p-8 bg-background">
    <Card className="w-full max-w-md shadow-xl border-0 animate-slide-up">
      <CardHeader className="text-center pb-2">
        <div class="lg:hidden mb-4">
          <h1 class="text-3xl font-bold text-primary">Order</h1>
        </div>

        <CardTitle className="text-2xl font-bold">Welcome back</CardTitle>
        <CardDescription>
          Sign in to your account to continue
        </CardDescription>
      </CardHeader>

      <CardContent className="pt-6">
        <form class="space-y-5" on:submit|preventDefault={submit}>
          <!-- EMAIL -->
          <div class="relative">
            <Mail
              class="absolute left-4 top-1/2 -translate-y-1/2
                     h-5 w-5 text-muted-foreground pointer-events-none"
            />
          </div>

          <!-- PASSWORD -->
          <div class="relative">
            <Lock
              class="absolute left-4 top-1/2 -translate-y-1/2
                     h-5 w-5 text-muted-foreground pointer-events-none"
            />

            <Input
              type={showPassword ? "text" : "password"}
              bind:value={password}
              placeholder="••••••••"
              className="pl-12 pr-12"
            />

            <button
              type="button"
              class="absolute right-4 top-1/2 -translate-y-1/2
                     text-muted-foreground hover:text-primary transition"
              on:click={() => (showPassword = !showPassword)}
            >
              {#if showPassword}
                <EyeOff class="h-5 w-5" />
              {:else}
                <Eye class="h-5 w-5" />
              {/if}
            </button>
          </div>

          {#if error}
            <p class="text-red-500 text-sm">{error}</p>
          {/if}

          <!-- BUTTON -->
          <AuthButton
            type="submit"
            variant="gradient"
            size="xl"
            class="w-full h-11"
          >
            Sign In
            <ArrowRight class="h-5 w-5" />
          </AuthButton>
        </form>

        <!-- FOOTER -->
        <div class="mt-8 text-center">
          <p class="text-sm text-muted-foreground">
            Don&apos;t have an account?
            <a
              href="/signup"
              class="text-primary font-medium hover:underline ml-1"
            >
              Sign up
            </a>
          </p>
        </div>
      </CardContent>
    </Card>
  </div>
</div>
