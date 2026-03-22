<script lang="ts">
  import { untrack } from 'svelte';
  import { getImageUrl } from '../../types/index.js';
  import { ChevronLeft, ChevronRight } from 'lucide-svelte';

  interface Props {
    imagenes: string[];
    alt?: string;
  }

  let { imagenes, alt = 'Producto' }: Props = $props();
  let selectedIndex = $state(0);
  let viewportW = $state(0);

  // Al cambiar color: mantener índice, solo clampear si hay menos fotos
  $effect(() => {
    const max = Math.max(0, imagenes.length - 1);
    untrack(() => {
      if (selectedIndex > max) selectedIndex = max;
    });
  });

  function navigate(dir: number) {
    const next = selectedIndex + dir;
    if (next >= 0 && next < imagenes.length) selectedIndex = next;
  }

  // ── Drag / Swipe ──────────────────────────────────────────────
  let isDragging = $state(false);
  let dragX = $state(0);
  let startX = 0;
  let startY = 0;
  let movedEnough = false;

  function onPointerDown(e: PointerEvent) {
    if ((e.target as HTMLElement).closest('.nav-btn')) return;
    (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
    isDragging = true;
    startX = e.clientX;
    startY = e.clientY;
    dragX = 0;
    movedEnough = false;
    e.preventDefault();
  }

  function onPointerMove(e: PointerEvent) {
    if (!isDragging) return;
    const dx = e.clientX - startX;
    const dy = e.clientY - startY;
    if (!movedEnough && Math.abs(dy) > Math.abs(dx) && Math.abs(dy) > 6) {
      isDragging = false;
      dragX = 0;
      return;
    }
    if (Math.abs(dx) > 6) movedEnough = true;
    // Rubber band en los extremos: resiste el arrastre imposible
    const atStart = selectedIndex === 0;
    const atEnd = selectedIndex === imagenes.length - 1;
    if ((atStart && dx > 0) || (atEnd && dx < 0)) {
      dragX = dx * 0.22;
    } else {
      dragX = dx;
    }
  }

  function onPointerUp() {
    if (!isDragging) return;
    isDragging = false;
    if (Math.abs(dragX) > viewportW * 0.18 && movedEnough) {
      navigate(dragX < 0 ? 1 : -1);
    }
    dragX = 0;
    movedEnough = false;
  }

  const stripX = $derived(-(selectedIndex * viewportW) + dragX);
  const stripTransition = $derived(isDragging ? 'none' : 'transform 0.32s ease-in-out');
</script>

<div class="flex flex-col gap-3">
  <div
    class="viewport {isDragging ? 'is-dragging' : ''}"
    bind:clientWidth={viewportW}
    onpointerdown={onPointerDown}
    onpointermove={onPointerMove}
    onpointerup={onPointerUp}
    onpointercancel={onPointerUp}
    role="img"
    aria-label={alt}
  >
    {#if imagenes.length > 0 && viewportW > 0}
      <div class="strip" style="transform: translateX({stripX}px); transition: {stripTransition};">
        {#each imagenes as img (img)}
          <div class="slide" style="width: {viewportW}px;">
            <img src={getImageUrl(img)} {alt} draggable="false" />
          </div>
        {/each}
      </div>
    {:else if imagenes.length === 0}
      <span class="text-7xl font-black select-none" style="color: #bbb;">
        {alt.charAt(0)}
      </span>
    {/if}

    {#if imagenes.length > 1}
      {#if selectedIndex > 0}
        <button class="nav-btn nav-prev" onclick={() => navigate(-1)} aria-label="Foto anterior">
          <ChevronLeft size={16} strokeWidth={2.5} />
        </button>
      {/if}
      {#if selectedIndex < imagenes.length - 1}
        <button class="nav-btn nav-next" onclick={() => navigate(1)} aria-label="Foto siguiente">
          <ChevronRight size={16} strokeWidth={2.5} />
        </button>
      {/if}
    {/if}
  </div>

  {#if imagenes.length > 1}
    <div class="thumbs">
      {#each imagenes as img, i (img)}
        <button
          class="thumb {i === selectedIndex ? 'active' : ''}"
          onclick={() => (selectedIndex = i)}
          aria-label="{alt} foto {i + 1}"
        >
          <img src={getImageUrl(img)} alt="" draggable="false" />
        </button>
      {/each}
    </div>
  {/if}
</div>

<style>
  .viewport {
    position: relative;
    aspect-ratio: 1;
    border-radius: 1.25rem;
    overflow: hidden;
    background: #d9d9d9;
    cursor: grab;
    user-select: none;
    -webkit-user-select: none;
    touch-action: pan-y;
  }
  .viewport.is-dragging {
    cursor: grabbing;
  }

  .strip {
    display: flex;
    height: 100%;
    will-change: transform;
  }
  .slide {
    flex-shrink: 0;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #d9d9d9;
  }
  .slide img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    pointer-events: none;
    -webkit-user-drag: none;
    display: block;
  }

  /* Flechas */
  .nav-btn {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    z-index: 2;
    width: 2.25rem;
    height: 2.25rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--color-border);
    background: var(--color-background);
    color: var(--color-foreground);
    cursor: pointer;
    opacity: 0;
    transition:
      opacity 0.2s,
      scale 0.15s;
    padding: 0;
  }
  .nav-btn:hover {
    scale: 1.1;
  }
  .viewport:hover .nav-btn {
    opacity: 1;
  }
  .nav-prev {
    left: 0.625rem;
  }
  .nav-next {
    right: 0.625rem;
  }

  /* Miniaturas */
  .thumbs {
    display: flex;
    gap: 0.5rem;
    overflow-x: auto;
    padding-bottom: 0.125rem;
    scrollbar-width: none;
  }
  .thumbs::-webkit-scrollbar {
    display: none;
  }
  .thumb {
    flex-shrink: 0;
    width: 3.25rem;
    height: 3.25rem;
    border-radius: 0.5rem;
    overflow: hidden;
    border: 2px solid transparent;
    cursor: pointer;
    opacity: 0.45;
    transition:
      border-color 0.15s,
      opacity 0.15s;
    background: #d9d9d9;
    padding: 0;
  }
  .thumb.active {
    border-color: var(--color-foreground);
    opacity: 1;
  }
  .thumb:not(.active):hover {
    opacity: 0.75;
  }
  .thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    pointer-events: none;
    display: block;
  }
</style>
