<script lang="ts">
  import Skeleton from '../ui/Skeleton.svelte';
</script>

<div class="px-4 py-5 sm:py-6 rounded-2xl">
  <div class="flex items-start justify-between gap-6">
    <div class="flex-1">
      <Skeleton class="h-7 w-2/3 mb-2" />
    </div>
    <Skeleton class="h-9 w-24 flex-shrink-0" />
  </div>
</div>
