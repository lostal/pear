<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { auth } from '../stores/auth.svelte.js';
  import { toast } from '../stores/toast.svelte.js';
  import { fetchUsers, updateUserRole, deleteUser } from '../services/users.service.js';
  import type { User } from '../types/index.js';
  import UserRow from '../components/users/UserRow.svelte';
  import ConfirmDialog from '../components/ui/ConfirmDialog.svelte';
  import Spinner from '../components/ui/Spinner.svelte';

  $effect(() => {
    if (!auth.isAuthenticated) push('/login');
    else if (!auth.isAdmin) push('/products');
  });

  $effect(() => {
    if (auth.isAdmin) loadUsers();
  });

  let users = $state<User[]>([]);
  let loading = $state(false);
  let deleteTarget = $state<User | null>(null);
  let deleting = $state(false);

  async function loadUsers() {
    loading = true;
    try {
      users = await fetchUsers();
    } catch {
      toast.error('Error al cargar los usuarios.');
    } finally {
      loading = false;
    }
  }

  async function handleRoleChange(user: User, role: 'user' | 'admin') {
    try {
      const updated = await updateUserRole(user._id, role);
      users = users.map((u) => (u._id === updated._id ? updated : u));
      toast.success(`Rol de ${user.username} actualizado.`);
    } catch {
      toast.error('Error al cambiar el rol.');
    }
  }

  async function handleDelete() {
    if (!deleteTarget) return;
    const target = deleteTarget;
    deleting = true;
    try {
      await deleteUser(target._id);
      users = users.filter((u) => u._id !== target._id);
      toast.success(`Usuario ${target.username} eliminado.`);
      deleteTarget = null;
    } catch {
      toast.error('Error al eliminar el usuario.');
    } finally {
      deleting = false;
    }
  }
</script>

<div class="max-w-4xl mx-auto px-4 sm:px-6 py-8">
  <div class="mb-6">
    <h1 class="text-2xl font-black tracking-tight">Usuarios</h1>
    <p class="text-sm text-[var(--color-muted-foreground)] mt-0.5">Gestión de cuentas</p>
  </div>

  {#if loading}
    <div class="flex justify-center py-20"><Spinner size="lg" /></div>
  {:else}
    <div class="bg-[var(--color-card)] border border-[var(--color-border)] rounded-lg overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-[var(--color-border)] bg-[var(--color-secondary)]">
            <th class="text-left py-3 px-4 font-semibold">Usuario</th>
            <th class="text-left py-3 px-4 font-semibold">Rol</th>
            <th class="text-left py-3 px-4 font-semibold">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {#each users as user (user._id)}
            <UserRow
              {user}
              onRoleChange={handleRoleChange}
              onDelete={(u) => (deleteTarget = u)}
            />
          {/each}
        </tbody>
      </table>

      {#if users.length === 0}
        <div class="text-center py-10 text-[var(--color-muted-foreground)]">No hay usuarios.</div>
      {/if}
    </div>
  {/if}
</div>

<ConfirmDialog
  open={!!deleteTarget}
  title="¿Eliminar usuario?"
  message="Se eliminará la cuenta de «{deleteTarget?.username}» permanentemente."
  confirmLabel="Eliminar"
  loading={deleting}
  onconfirm={handleDelete}
  oncancel={() => (deleteTarget = null)}
/>
