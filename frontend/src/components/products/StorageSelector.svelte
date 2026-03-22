<script lang="ts">
  import type { GrupoOpciones, Opcion } from '../../types/index.js';
  import { formatPrice } from '../../lib/utils.js';

  interface Props {
    grupo: GrupoOpciones;
    selected?: string;
    precioBase: number;
    onselect: (opcion: Opcion) => void;
  }

  let { grupo, selected, precioBase, onselect }: Props = $props();
</script>

<div class="flex flex-wrap gap-2">
  {#each grupo.opciones as opcion}
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <button
      onclick={() => onselect(opcion)}
      class="px-4 py-2 rounded-xl border text-sm font-medium transition-all cursor-pointer"
      style={selected === opcion.valor
        ? 'border-color: var(--color-foreground); background: var(--color-foreground); color: var(--color-background);'
        : 'border-color: var(--color-border); color: var(--color-foreground);'}
    >
      <span>{opcion.valor}</span>
      {#if opcion.modificadorPrecio !== 0}
        <span class="ml-1 opacity-60 text-xs">
          {formatPrice(precioBase + opcion.modificadorPrecio)}
        </span>
      {/if}
    </button>
  {/each}
</div>
