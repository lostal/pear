<script lang="ts">
  import { getImageUrl } from '../../types/index.js';

  interface Props {
    imagenes: string[];
    alt?: string;
  }

  let { imagenes, alt = 'Producto' }: Props = $props();
  let selectedIndex = $state(0);

  // Reset cuando cambian las imágenes (al seleccionar otro color)
  $effect(() => {
    imagenes;
    selectedIndex = 0;
  });

  const mainImage = $derived(imagenes[selectedIndex] ?? null);
</script>

<div class="flex flex-col gap-4">
  <!-- Imagen principal -->
  <div
    class="aspect-square rounded-2xl overflow-hidden flex items-center justify-center"
    style="background: var(--color-secondary);"
  >
    {#if mainImage}
      <img
        src={getImageUrl(mainImage)}
        {alt}
        class="w-full h-full object-contain transition-opacity duration-200"
      />
    {:else}
      <span class="text-7xl font-black select-none" style="color: var(--color-border);">
        {alt.charAt(0)}
      </span>
    {/if}
  </div>

  <!-- Miniaturas -->
  {#if imagenes.length > 1}
    <div class="flex gap-2 justify-center flex-wrap">
      {#each imagenes as img, i}
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <button
          onclick={() => selectedIndex = i}
          class="w-14 h-14 rounded-lg overflow-hidden border-2 transition-all cursor-pointer"
          style={i === selectedIndex
            ? 'border-color: var(--color-foreground);'
            : 'border-color: transparent; opacity: 0.5;'}
        >
          <img
            src={getImageUrl(img)}
            alt="{alt} {i + 1}"
            class="w-full h-full object-cover"
          />
        </button>
      {/each}
    </div>
  {/if}
</div>
