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
    'inline-flex items-center justify-center font-medium transition-all duration-200 focus-visible:outline-2 focus-visible:outline-offset-2 disabled:pointer-events-none disabled:opacity-50 cursor-pointer';

  const variantMap: Record<string, string> = {
    primary: 'text-white',
    secondary: 'border hover:opacity-80',
    destructive: 'text-white',
    ghost: 'hover:opacity-80',
  };

  const sizeMap: Record<string, string> = {
    sm: 'text-xs px-3 py-1.5 gap-1.5 rounded-full',
    md: 'text-sm px-5 py-2 gap-2 rounded-full',
    lg: 'text-base px-6 py-2.5 gap-2 rounded-full',
  };

  const styleMap: Record<string, string> = {
    primary: 'background-color: var(--color-apple-blue); color: white;',
    secondary: 'background-color: white; color: var(--color-foreground); border-color: var(--color-border);',
    destructive: 'background-color: var(--color-destructive); color: white;',
    ghost: 'background-color: transparent; color: var(--color-foreground);',
  };

  const classes = $derived(`${base} ${variantMap[variant]} ${sizeMap[size]} ${klass}`);
</script>

<button
  {type}
  class={classes}
  style={styleMap[variant]}
  disabled={disabled || loading}
  {onclick}
  onmouseenter={(e) => { if (variant === 'primary') (e.currentTarget as HTMLElement).style.backgroundColor = 'var(--color-apple-blue-hover)'; }}
  onmouseleave={(e) => { if (variant === 'primary') (e.currentTarget as HTMLElement).style.backgroundColor = 'var(--color-apple-blue)'; }}
>
  {#if loading}
    <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
    </svg>
  {/if}
  {@render children?.()}
</button>
