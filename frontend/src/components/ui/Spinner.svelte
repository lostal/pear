<script lang="ts">
  interface Props {
    size?: 'sm' | 'md' | 'lg';
    class?: string;
  }

  let { size = 'md', class: klass = '' }: Props = $props();

  const sizes = { sm: 'h-4 w-4', md: 'h-6 w-6', lg: 'h-10 w-10' };
</script>

<svg
  class="animate-spin {sizes[size]} {klass}"
  style="color: var(--color-foreground); opacity: 0.5;"
  viewBox="0 0 24 24"
  fill="none"
  aria-label="Cargando"
>
  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
</svg>
