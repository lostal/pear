<script lang="ts">
  import { products } from '../../stores/products.svelte.js';

  function handleSearch(e: Event) {
    products.setSearch((e.target as HTMLInputElement).value);
  }
</script>

<div class="flex flex-col sm:flex-row gap-3 items-start sm:items-center">
  <div class="relative">
    <svg
      class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 pointer-events-none"
      style="color: var(--color-muted-foreground);"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.35-4.35" />
    </svg>
    <input
      value={products.search}
      placeholder="Buscar productos..."
      oninput={handleSearch}
      class="w-full sm:w-72 pl-9 pr-4 py-2 rounded-md text-sm transition-all"
      style="background: var(--color-input); border: 1px solid var(--color-border); color: var(--color-foreground); outline: none;"
      onfocus={(e) => {
        (e.target as HTMLElement).style.borderColor = 'var(--color-ring)';
        (e.target as HTMLElement).style.boxShadow =
          '0 0 0 2px color-mix(in srgb, var(--color-ring) 20%, transparent)';
      }}
      onblur={(e) => {
        (e.target as HTMLElement).style.borderColor = 'var(--color-border)';
        (e.target as HTMLElement).style.boxShadow = 'none';
      }}
    />
  </div>

  <span class="text-sm" style="color: var(--color-muted-foreground);">
    {products.count} producto{products.count !== 1 ? 's' : ''}
  </span>
</div>
