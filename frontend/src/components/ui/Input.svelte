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
    <label for={id} class="{labelClass}" style="color: var(--color-foreground);">
      {label}{#if required}<span style="color: var(--color-destructive);" class="ml-0.5">*</span>{/if}
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
    class="w-full rounded-md border px-3 py-2 text-sm disabled:opacity-50 transition-all"
    style="border-color: {error ? 'var(--color-destructive)' : 'var(--color-border)'}; background: var(--color-input); color: var(--color-foreground); outline: none;"
    onfocus={(e) => {
      if (!error) {
        (e.target as HTMLElement).style.borderColor = 'var(--color-ring)';
        (e.target as HTMLElement).style.boxShadow = '0 0 0 2px color-mix(in srgb, var(--color-ring) 20%, transparent)';
      }
    }}
    onblur={(e) => {
      if (!error) {
        (e.target as HTMLElement).style.borderColor = 'var(--color-border)';
        (e.target as HTMLElement).style.boxShadow = 'none';
      }
    }}
  />
  {#if error}
    <p class="text-xs" style="color: var(--color-destructive);">{error}</p>
  {/if}
</div>
