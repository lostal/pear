<script lang="ts">
  import { theme } from '../../stores/theme.svelte.js';
  import { slide } from 'svelte/transition';
  import { onMount } from 'svelte';

  let isOpen = $state(false);
  let dropdownRef: HTMLDivElement | undefined = $state();

  function toggleDropdown() {
    isOpen = !isOpen;
  }

  function closeDropdown() {
    isOpen = false;
  }

  function setTheme(newTheme: 'light' | 'dark' | 'system') {
    theme.set(newTheme);
    closeDropdown();
  }

  function handleClickOutside(event: MouseEvent) {
    if (dropdownRef && !dropdownRef.contains(event.target as Node)) {
      closeDropdown();
    }
  }

  onMount(() => {
    document.addEventListener('click', handleClickOutside);
    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  });
</script>

<div class="relative" bind:this={dropdownRef}>
  <button
    onclick={toggleDropdown}
    class="p-2 rounded-md hover:bg-accent transition-all opacity-70 hover:opacity-100 cursor-pointer"
    style="color: var(--color-muted-foreground);"
    aria-label="Menú de tema"
    aria-expanded={isOpen}
    aria-haspopup="true"
  >
    {#if theme.current === 'system'}
      <!-- Monitor -->
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect width="20" height="14" x="2" y="3" rx="2" />
        <line x1="8" x2="16" y1="21" y2="21" />
        <line x1="12" x2="12" y1="17" y2="21" />
      </svg>
    {:else if theme.current === 'light'}
      <!-- Sol -->
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="5" />
        <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
      </svg>
    {:else}
      <!-- Luna -->
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
      </svg>
    {/if}
  </button>

  {#if isOpen}
    <div
      transition:slide={{ duration: 200 }}
      class="absolute right-0 mt-2 w-36 rounded-md border bg-popover shadow-lg z-50 overflow-hidden"
      style="color: var(--color-popover-foreground);"
    >
      <div class="p-1">
        <button
          onclick={() => setTheme('light')}
          class="flex w-full items-center rounded-sm px-2 py-1.5 text-sm hover:bg-accent cursor-pointer transition-colors
            {theme.current === 'light' ? 'bg-accent' : ''}"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="mr-2">
            <circle cx="12" cy="12" r="5" />
            <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
          </svg>
          Claro
        </button>
        <button
          onclick={() => setTheme('dark')}
          class="flex w-full items-center rounded-sm px-2 py-1.5 text-sm hover:bg-accent cursor-pointer transition-colors
            {theme.current === 'dark' ? 'bg-accent' : ''}"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="mr-2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
          </svg>
          Oscuro
        </button>
        <button
          onclick={() => setTheme('system')}
          class="flex w-full items-center rounded-sm px-2 py-1.5 text-sm hover:bg-accent cursor-pointer transition-colors
            {theme.current === 'system' ? 'bg-accent' : ''}"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="mr-2">
            <rect width="20" height="14" x="2" y="3" rx="2" />
            <line x1="8" x2="16" y1="21" y2="21" />
            <line x1="12" x2="12" y1="17" y2="21" />
          </svg>
          Sistema
        </button>
      </div>
    </div>
  {/if}
</div>
