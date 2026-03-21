<script lang="ts">
  import type { User } from '../../types/index.js';
  import { auth } from '../../stores/auth.svelte.js';
  import Badge from '../ui/Badge.svelte';
  import Button from '../ui/Button.svelte';

  interface Props {
    user: User;
    onRoleChange: (user: User, role: 'user' | 'admin') => void;
    onDelete: (user: User) => void;
  }

  let { user, onRoleChange, onDelete }: Props = $props();

  const isSelf = $derived(auth.user?._id === user._id);
</script>

<tr class="border-b border-[var(--color-border)] hover:bg-[var(--color-accent)]/30 transition-colors">
  <td class="py-3 px-4">
    <p class="font-medium text-sm">{user.username}</p>
  </td>
  <td class="py-3 px-4">
    <Badge variant={user.role === 'admin' ? 'success' : 'muted'}>
      {user.role}
    </Badge>
  </td>
  <td class="py-3 px-4">
    <div class="flex gap-2">
      {#if !isSelf}
        <Button
          size="sm"
          variant="secondary"
          onclick={() => onRoleChange(user, user.role === 'admin' ? 'user' : 'admin')}
        >
          {user.role === 'admin' ? '→ User' : '→ Admin'}
        </Button>
        <Button size="sm" variant="destructive" onclick={() => onDelete(user)}>
          Borrar
        </Button>
      {:else}
        <span class="text-xs text-[var(--color-muted-foreground)] italic">Tú</span>
      {/if}
    </div>
  </td>
</tr>
