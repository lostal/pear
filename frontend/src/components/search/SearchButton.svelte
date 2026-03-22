<script lang="ts">
  import { onMount } from 'svelte';
  import { uiState } from '../../lib/ui.svelte.js';
  import { Search } from 'lucide-svelte';

  function handleKeydown(e: KeyboardEvent) {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      uiState.openSearch();
    }
  }

  onMount(() => {
    window.addEventListener('keydown', handleKeydown);
    return () => window.removeEventListener('keydown', handleKeydown);
  });
</script>

<button
  onclick={() => uiState.openSearch()}
  class="group flex items-center gap-2 px-3 py-2 rounded-md transition-all duration-200 cursor-pointer"
  style="background: var(--color-secondary); color: var(--color-muted-foreground); border: 1px solid transparent;"
  aria-label="Buscar productos"
>
  <Search size={16} class="opacity-70" />
  <span class="hidden sm:inline-block text-xs font-semibold opacity-80">Buscar</span>
  <kbd
    class="hidden lg:inline-flex h-5 items-center gap-1 rounded px-1.5 font-mono text-xs font-medium ml-1"
    style="border: 1px solid var(--color-border); background: var(--color-muted); color: var(--color-muted-foreground);"
  >
    <span class="text-xs">⌘</span>K
  </kbd>
</button>
