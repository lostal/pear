<script lang="ts">
  interface Props {
    variant?: 'primary' | 'secondary' | 'destructive' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    loading?: boolean;
    disabled?: boolean;
    type?: 'button' | 'submit' | 'reset';
    class?: string;
    onclick?: (e: MouseEvent) => void;
    children?: import('svelte').Snippet;
  }

  let {
    variant = 'primary',
    size = 'md',
    loading = false,
    disabled = false,
    type = 'button',
    class: klass = '',
    onclick,
    children,
  }: Props = $props();

  const base =
    'inline-flex items-center justify-center font-medium rounded-md transition-all duration-200 focus-visible:outline-2 focus-visible:outline-offset-2 disabled:pointer-events-none disabled:opacity-50 cursor-pointer';

  const variantMap: Record<string, string> = {
    primary: 'bg-[var(--color-primary)] text-[var(--color-primary-foreground)] hover:opacity-80',
    secondary: 'bg-[var(--color-secondary)] text-[var(--color-secondary-foreground)] border border-[var(--color-border)] hover:bg-[var(--color-accent)]',
    destructive: 'bg-[var(--color-destructive)] text-[var(--color-destructive-foreground)] hover:opacity-80',
    ghost: 'bg-transparent text-[var(--color-foreground)] hover:bg-[var(--color-accent)]',
  };

  const sizeMap: Record<string, string> = {
    sm: 'text-sm px-3 py-1.5 gap-1.5',
    md: 'text-sm px-4 py-2 gap-2',
    lg: 'text-base px-5 py-2.5 gap-2',
  };

  const classes = $derived(`${base} ${variantMap[variant]} ${sizeMap[size]} ${klass}`);
</script>

<button {type} class={classes} disabled={disabled || loading} {onclick}>
  {#if loading}
    <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
    </svg>
  {/if}
  {@render children?.()}
</button>
