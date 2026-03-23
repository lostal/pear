<script lang="ts">
  import type { Picture } from 'vite-imagetools';

  let {
    src,
    alt,
    class: cls = '',
    loading = 'lazy',
    fetchpriority,
    style,
  }: {
    src: Picture;
    alt: string;
    class?: string;
    loading?: 'lazy' | 'eager';
    fetchpriority?: 'high' | 'low' | 'auto';
    style?: string;
  } = $props();
</script>

<picture>
  {#each Object.entries(src.sources) as [format, srcset]}
    <source {srcset} type="image/{format}" />
  {/each}
  <img src={src.img.src} {alt} {loading} {fetchpriority} class={cls} {style} />
</picture>
