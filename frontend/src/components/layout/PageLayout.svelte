<script lang="ts">
  interface Props {
    children?: import('svelte').Snippet;
  }
  let { children }: Props = $props();
</script>

<div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-16">
  {@render children?.()}
</div>
