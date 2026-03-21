<script lang="ts">
  interface Props {
    class?: string;
  }

  let { class: klass = '' }: Props = $props();
</script>

<div class="animate-pulse rounded-md bg-[var(--color-accent)] {klass}"></div>
