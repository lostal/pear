<script lang="ts">
  import Modal from './Modal.svelte';
  import Button from './Button.svelte';

  interface Props {
    open: boolean;
    title?: string;
    message?: string;
    confirmLabel?: string;
    loading?: boolean;
    onconfirm?: () => void;
    oncancel?: () => void;
  }

  let {
    open,
    title = '¿Confirmar acción?',
    message = 'Esta acción no se puede deshacer.',
    confirmLabel = 'Confirmar',
    loading = false,
    onconfirm,
    oncancel,
  }: Props = $props();
</script>

<Modal {open} {title} onclose={oncancel}>
  <p class="text-[var(--color-muted-foreground)] mb-6">{message}</p>
  <div class="flex justify-end gap-3">
    <Button variant="secondary" onclick={oncancel} disabled={loading}>Cancelar</Button>
    <Button variant="destructive" onclick={onconfirm} {loading}>{confirmLabel}</Button>
  </div>
</Modal>
