<script lang="ts">
  interface Props {
    open: boolean;
    title?: string;
    onclose?: () => void;
    children?: import('svelte').Snippet;
  }

  let { open, title = '', onclose, children }: Props = $props();

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Escape') onclose?.();
  }
</script>

{#if open}
  <div
    class="fixed inset-0 z-50 flex items-center justify-center p-4"
    role="dialog"
    aria-modal="true"
    tabindex="-1"
    onkeydown={handleKeydown}
  >
    <!-- Backdrop -->
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div
      class="absolute inset-0 backdrop-blur-sm"
      style="background: rgba(0,0,0,0.35);"
      onclick={onclose}
    ></div>

    <!-- Panel -->
    <div
      class="relative z-10 w-full max-w-lg bg-white rounded-3xl border overflow-hidden"
      style="border-color: var(--color-border); box-shadow: 0 24px 60px rgba(0,0,0,0.15);"
    >
      {#if title}
        <div class="flex items-center justify-between px-6 py-5 border-b" style="border-color: var(--color-border);">
          <h2 class="text-lg font-semibold" style="letter-spacing: -0.02em;">{title}</h2>
          <button
            onclick={onclose}
            class="transition-colors cursor-pointer rounded-full p-1 hover:bg-gray-100"
            style="color: var(--color-muted-foreground);"
            aria-label="Cerrar"
          >
            <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      {/if}
      <div class="px-6 py-5">
        {@render children?.()}
      </div>
    </div>
  </div>
{/if}
