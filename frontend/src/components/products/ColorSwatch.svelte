<script lang="ts">
  import type { OpcionColor } from '../../types/index.js';

  interface Props {
    opciones: OpcionColor[];
    selected?: string;
    onselect: (opcion: OpcionColor) => void;
  }

  let { opciones, selected, onselect }: Props = $props();
</script>

<div class="flex flex-wrap gap-2">
  {#each opciones as opcion}
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <button
      title={opcion.valor}
      onclick={() => onselect(opcion)}
      class="relative w-8 h-8 rounded-full border-2 transition-all cursor-pointer focus:outline-none"
      style={selected === opcion.valor
        ? `border-color: var(--color-foreground); background: ${opcion.codigoHex};`
        : `border-color: transparent; outline: 2px solid transparent; background: ${opcion.codigoHex};`}
    >
      {#if selected === opcion.valor}
        <span
          class="absolute inset-0 rounded-full ring-2 ring-offset-1 pointer-events-none"
          style="ring-color: var(--color-foreground);"
        ></span>
      {/if}
    </button>
  {/each}
</div>
