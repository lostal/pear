<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { auth } from '../stores/auth.svelte.js';
  import { toast } from '../stores/toast.svelte.js';
  import { fetchUsers, updateUserRole, deleteUser } from '../services/users.service.js';
  import type { User } from '../types/index.js';
  import UserRow from '../components/users/UserRow.svelte';
  import ConfirmDialog from '../components/ui/ConfirmDialog.svelte';
  import Spinner from '../components/ui/Spinner.svelte';
  import PageLayout from '../components/layout/PageLayout.svelte';

  $effect(() => {
    if (!auth.isAuthenticated) push('/');
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

<PageLayout>
  <div class="mb-10">
    <h1 class="text-4xl sm:text-5xl font-semibold tracking-tight" style="letter-spacing: -0.04em;">Usuarios</h1>
    <p class="text-sm mt-1.5" style="color: var(--color-muted-foreground);">Gestión de cuentas</p>
  </div>

  {#if loading}
    <div class="flex justify-center py-20"><Spinner size="lg" /></div>
  {:else}
    <div class="bg-white rounded-2xl overflow-hidden" style="box-shadow: 0 2px 12px rgba(0,0,0,0.06);">
      <table class="w-full text-sm">
        <thead>
          <tr style="border-bottom: 1px solid var(--color-border);">
            <th class="text-left py-3 px-5 text-xs font-medium uppercase tracking-widest" style="color: var(--color-muted-foreground);">Usuario</th>
            <th class="text-left py-3 px-5 text-xs font-medium uppercase tracking-widest" style="color: var(--color-muted-foreground);">Rol</th>
            <th class="text-left py-3 px-5 text-xs font-medium uppercase tracking-widest" style="color: var(--color-muted-foreground);">Acciones</th>
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
        <div class="text-center py-10" style="color: var(--color-muted-foreground);">No hay usuarios.</div>
      {/if}
    </div>
  {/if}
</PageLayout>

<ConfirmDialog
  open={!!deleteTarget}
  title="¿Eliminar usuario?"
  message="Se eliminará la cuenta de «{deleteTarget?.username}» permanentemente."
  confirmLabel="Eliminar"
  loading={deleting}
  onconfirm={handleDelete}
  oncancel={() => (deleteTarget = null)}
/>
