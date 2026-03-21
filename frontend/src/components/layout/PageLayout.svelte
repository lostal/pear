<script lang="ts">
  interface Props {
    children?: import('svelte').Snippet;
    narrow?: boolean;
  }
  let { children, narrow = false }: Props = $props();
</script>

<div class="{narrow ? 'max-w-3xl' : 'max-w-6xl'} mx-auto px-4 sm:px-6 lg:px-8 pt-10 pb-20">
  {@render children?.()}
</div>
