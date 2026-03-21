<script lang="ts">
  import { toast } from '../stores/toast.svelte.js';
  import Toast from './ui/Toast.svelte';
</script>

<div class="fixed bottom-4 right-4 z-[100] flex flex-col gap-2 items-end" aria-live="polite">
  {#each toast.toasts as item (item.id)}
    <Toast {item} />
  {/each}
</div>
