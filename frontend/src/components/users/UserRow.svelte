<script lang="ts">
  import type { User } from '../../types/index.js';
  import { auth } from '../../stores/auth.svelte.js';
  import Badge from '../ui/Badge.svelte';
  import Button from '../ui/Button.svelte';
  import { Shield, User as UserIcon, Trash2 } from 'lucide-svelte';

  interface Props {
    user: User;
    onRoleChange: (user: User, role: 'user' | 'admin') => void;
    onDelete: (user: User) => void;
  }

  let { user, onRoleChange, onDelete }: Props = $props();

  const isSelf = $derived(auth.user?._id === user._id);
</script>

<tr
  class="border-b border-[var(--color-border)] hover:bg-[var(--color-accent)]/30 transition-colors"
>
  <td class="py-3 px-4">
    <div class="flex items-center gap-3">
      <div
        class="h-8 w-8 rounded-full flex items-center justify-center text-xs font-black shrink-0 border"
        style="background: var(--color-secondary); color: var(--color-foreground); border-color: var(--color-border);"
      >
        {user.username[0].toUpperCase()}
      </div>
      <p class="font-medium text-sm">{user.username}</p>
    </div>
  </td>
  <td class="py-3 px-4">
    <Badge variant={user.role === 'admin' ? 'success' : 'muted'}>
      {user.role}
    </Badge>
  </td>
  <td class="py-3 px-4">
    <div class="flex gap-2 items-center">
      {#if !isSelf}
        <Button
          size="sm"
          variant="secondary"
          onclick={() => onRoleChange(user, user.role === 'admin' ? 'user' : 'admin')}
        >
          {#if user.role === 'admin'}
            <UserIcon size={13} />
            Hacer user
          {:else}
            <Shield size={13} />
            Hacer admin
          {/if}
        </Button>
        <Button size="sm" variant="destructive" onclick={() => onDelete(user)}>
          <Trash2 size={13} />
          Borrar
        </Button>
      {:else}
        <span
          class="text-xs px-2 py-1 rounded-md font-medium"
          style="background: var(--color-secondary); color: var(--color-muted-foreground); border: 1px solid var(--color-border);"
        >
          Tú
        </span>
      {/if}
    </div>
  </td>
</tr>
