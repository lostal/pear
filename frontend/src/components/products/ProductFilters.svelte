<script lang="ts">
  import { products } from '../../stores/products.svelte.js';

  function handleSearch(e: Event) {
    products.setSearch((e.target as HTMLInputElement).value);
  }
</script>

<div class="flex flex-col sm:flex-row gap-3 items-start sm:items-center">
  <div class="relative">
    <svg
      class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--color-muted-foreground)] pointer-events-none"
      viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
    >
      <circle cx="11" cy="11" r="8" /><path stroke-linecap="round" stroke-linejoin="round" d="m21 21-4.35-4.35" />
    </svg>
    <input
      value={products.search}
      placeholder="Buscar productos..."
      oninput={handleSearch}
      class="w-full sm:max-w-xs pl-9 pr-4 py-2 rounded-md bg-[var(--color-secondary)]/50 border border-transparent hover:border-[var(--color-border)]/50 focus:bg-[var(--color-secondary)] focus:border-[var(--color-border)] focus:outline-none text-sm transition-all"
    />
  </div>

  <span class="text-xs font-bold uppercase tracking-widest text-[var(--color-muted-foreground)]">
    {products.count} producto{products.count !== 1 ? 's' : ''}
  </span>
</div>
