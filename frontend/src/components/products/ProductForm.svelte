<script lang="ts">
  import type { Product } from '../../types/index.js';
  import Input from '../ui/Input.svelte';
  import Button from '../ui/Button.svelte';

  interface Props {
    product?: Product | null;
    onSave: (data: { nombre: string; precio: number }) => Promise<void>;
    onCancel: () => void;
  }

  let { product = null, onSave, onCancel }: Props = $props();

  // svelte-ignore state_referenced_locally
  let nombre = $state(product?.nombre ?? '');
  // svelte-ignore state_referenced_locally
  let precio = $state<number | string>(product?.precio ?? '');
  let saving = $state(false);
  let errors = $state<Record<string, string>>({});

  function validate() {
    const errs: Record<string, string> = {};
    if (!nombre.trim()) errs.nombre = 'El nombre es obligatorio.';
    const p = Number(precio);
    if (isNaN(p) || p < 0) errs.precio = 'El precio debe ser un número positivo.';
    return errs;
  }

  async function handleSubmit(e: SubmitEvent) {
    e.preventDefault();
    errors = validate();
    if (Object.keys(errors).length > 0) return;

    saving = true;
    try {
      await onSave({ nombre: nombre.trim(), precio: Number(precio) });
    } finally {
      saving = false;
    }
  }
</script>

<form onsubmit={handleSubmit} class="flex flex-col gap-4">
  <Input
    bind:value={nombre}
    label="Nombre"
    placeholder="Nombre del producto"
    required
    error={errors.nombre}
  />
  <Input
    bind:value={precio}
    type="number"
    label="Precio (€)"
    placeholder="0.00"
    required
    error={errors.precio}
  />

  <div class="flex justify-end gap-3 pt-2">
    <Button variant="secondary" type="button" onclick={onCancel} disabled={saving}>
      Cancelar
    </Button>
    <Button type="submit" loading={saving} disabled={saving}>
      {product ? 'Guardar cambios' : 'Crear producto'}
    </Button>
  </div>
</form>
