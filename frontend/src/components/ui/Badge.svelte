<script lang="ts">
  interface Props {
    variant?: 'default' | 'success' | 'destructive' | 'muted';
    class?: string;
    children?: import('svelte').Snippet;
  }

  let { variant = 'default', class: klass = '', children }: Props = $props();

  const variants: Record<string, string> = {
    default: 'bg-[var(--color-secondary)] text-[var(--color-secondary-foreground)]',
    success: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    destructive: 'bg-red-100 text-[var(--color-destructive)]',
    muted: 'bg-[var(--color-muted)] text-[var(--color-muted-foreground)]',
  };
</script>

<span
  class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium {variants[
    variant
  ]} {klass}"
>
  {@render children?.()}
</span>
