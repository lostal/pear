<script lang="ts">
  import { products } from '../../stores/products.svelte.js';
  import Input from '../ui/Input.svelte';

  function handleSearch(e: Event) {
    products.setSearch((e.target as HTMLInputElement).value);
  }
</script>

<div class="flex flex-col sm:flex-row gap-3 items-start sm:items-center">
  <div class="flex-1">
    <Input
      value={products.search}
      placeholder="Buscar productos..."
      oninput={handleSearch}
      class="max-w-sm"
    />
  </div>

  <span class="text-sm text-[var(--color-muted-foreground)]">
    {products.count} producto{products.count !== 1 ? 's' : ''}
  </span>
</div>
