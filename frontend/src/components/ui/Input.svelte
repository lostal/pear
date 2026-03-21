<script lang="ts">
  interface Props {
    value?: string | number;
    type?: string;
    placeholder?: string;
    label?: string;
    labelClass?: string;
    error?: string;
    disabled?: boolean;
    required?: boolean;
    id?: string;
    class?: string;
    oninput?: (e: Event) => void;
    onchange?: (e: Event) => void;
  }

  let {
    value = $bindable(''),
    type = 'text',
    placeholder = '',
    label = '',
    labelClass = 'text-sm font-medium',
    error = '',
    disabled = false,
    required = false,
    id = crypto.randomUUID(),
    class: klass = '',
    oninput,
    onchange,
  }: Props = $props();
</script>

<div class="flex flex-col gap-1 {klass}">
  {#if label}
    <label for={id} class="{labelClass} text-[var(--color-foreground)]">
      {label}{#if required}<span class="text-[var(--color-destructive)] ml-0.5">*</span>{/if}
    </label>
  {/if}
  <input
    {id}
    {type}
    bind:value
    {placeholder}
    {disabled}
    {required}
    {oninput}
    {onchange}
    class="w-full rounded-md border border-[var(--color-border)] bg-[var(--color-input)] px-3 py-2 text-sm text-[var(--color-foreground)] placeholder:text-[var(--color-muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--color-pear)] focus:border-transparent disabled:opacity-50 transition-shadow"
    class:border-[var(--color-destructive)]={!!error}
  />
  {#if error}
    <p class="text-xs text-[var(--color-destructive)]">{error}</p>
  {/if}
</div>
