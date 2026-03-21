<script lang="ts">
  import Skeleton from '../ui/Skeleton.svelte';
</script>

<div class="flex flex-col bg-[var(--color-card)] border border-[var(--color-border)] rounded-lg p-4 gap-3">
  <div class="flex items-start justify-between gap-2">
    <Skeleton class="h-5 w-3/4" />
    <Skeleton class="h-5 w-14" />
  </div>
  <Skeleton class="h-4 w-1/3" />
  <Skeleton class="h-4 w-full" />
  <Skeleton class="h-4 w-4/5" />
  <div class="flex items-center justify-between pt-2 border-t border-[var(--color-border)]">
    <Skeleton class="h-6 w-16" />
    <div class="flex gap-2">
      <Skeleton class="h-7 w-14" />
      <Skeleton class="h-7 w-14" />
    </div>
  </div>
</div>
