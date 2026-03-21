<script lang="ts">
  import Skeleton from '../ui/Skeleton.svelte';
</script>

<div class="bg-white rounded-2xl overflow-hidden" style="box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
  <!-- Aspect-square placeholder -->
  <div class="aspect-square">
    <Skeleton class="w-full h-full rounded-none" />
  </div>
  <div class="p-4">
    <Skeleton class="h-4 w-3/4 mb-2" />
    <Skeleton class="h-3 w-1/3" />
  </div>
</div>
