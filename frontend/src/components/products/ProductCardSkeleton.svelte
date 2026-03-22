<script lang="ts">
  import Skeleton from '../ui/Skeleton.svelte';
</script>

<div
  class="rounded-lg border overflow-hidden"
  style="background: var(--color-card); border-color: var(--color-border);"
>
  <!-- Aspect-square placeholder -->
  <div class="aspect-square">
    <Skeleton class="w-full h-full rounded-none" />
  </div>
  <div class="p-4">
    <Skeleton class="h-4 w-3/4 mb-2" />
    <Skeleton class="h-3 w-1/3" />
  </div>
</div>
