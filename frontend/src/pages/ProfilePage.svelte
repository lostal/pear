<script lang="ts">
  import { push } from '../lib/router.svelte.js';
  import { auth } from '../stores/auth.svelte.js';
  import PageLayout from '../components/layout/PageLayout.svelte';
  import { LogOut, User, ShieldCheck, Mail } from 'lucide-svelte';

  $effect(() => {
    if (!auth.isAuthenticated) push('/');
  });

  function handleLogout() {
    auth.logout();
    push('/');
  }
</script>

<PageLayout narrow>
  {#if auth.user}
    <div class="flex flex-col gap-6">

      <!-- Card principal -->
      <div class="rounded-2xl border overflow-hidden" style="border-color: var(--color-border); background: var(--color-card);">

        <!-- Header con avatar -->
        <div class="px-8 pt-8 pb-6 flex flex-col items-center text-center border-b" style="border-color: var(--color-border); background: var(--color-secondary);">
          <div
            class="h-20 w-20 rounded-full flex items-center justify-center text-3xl font-black mb-4 border-2"
            style="background: var(--color-background); color: var(--color-foreground); border-color: var(--color-border);"
          >
            {auth.user.username[0].toUpperCase()}
          </div>
          <h1 class="text-2xl font-black tracking-tight">{auth.user.username}</h1>
          <span
            class="mt-2 inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1 rounded-full"
            style="background: var(--color-background); color: var(--color-foreground); border: 1px solid var(--color-border);"
          >
            {#if auth.user.role === 'admin'}
              <ShieldCheck size={12} />
              Administrador
            {:else}
              <User size={12} />
              Usuario
            {/if}
          </span>
        </div>

        <!-- Info de la cuenta -->
        <div class="px-8 py-5">
          <p class="text-xs font-semibold uppercase tracking-widest mb-4" style="color: var(--color-muted-foreground);">
            Información de la cuenta
          </p>
          <div class="flex flex-col gap-4">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0" style="background: var(--color-secondary);">
                <User size={14} style="color: var(--color-muted-foreground);" />
              </div>
              <div>
                <p class="text-xs" style="color: var(--color-muted-foreground);">Nombre de usuario</p>
                <p class="text-sm font-semibold">{auth.user.username}</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0" style="background: var(--color-secondary);">
                <ShieldCheck size={14} style="color: var(--color-muted-foreground);" />
              </div>
              <div>
                <p class="text-xs" style="color: var(--color-muted-foreground);">Rol</p>
                <p class="text-sm font-semibold capitalize">{auth.user.role}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Acciones -->
      <div class="rounded-2xl border overflow-hidden" style="border-color: var(--color-border); background: var(--color-card);">
        <div class="px-8 py-5">
          <p class="text-xs font-semibold uppercase tracking-widest mb-4" style="color: var(--color-muted-foreground);">
            Sesión
          </p>
          <button
            onclick={handleLogout}
            class="flex items-center gap-2.5 text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors cursor-pointer"
            style="color: var(--color-destructive); background: color-mix(in srgb, var(--color-destructive) 8%, transparent); border: 1px solid color-mix(in srgb, var(--color-destructive) 20%, transparent);"
          >
            <LogOut size={15} />
            Cerrar sesión
          </button>
        </div>
      </div>

    </div>
  {/if}
</PageLayout>
