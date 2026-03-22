import { toast as sonner } from 'svelte-sonner';

export type ToastType = 'success' | 'error' | 'info' | 'warning';

export const toast = {
  success: (msg: string) => sonner.success(msg),
  error: (msg: string) => sonner.error(msg),
  info: (msg: string) => sonner.info(msg),
  warning: (msg: string) => sonner.warning(msg),
};
