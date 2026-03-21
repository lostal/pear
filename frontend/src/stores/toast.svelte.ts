export type ToastType = 'success' | 'error' | 'info' | 'warning';

export interface Toast {
  id: number;
  message: string;
  type: ToastType;
}

let _counter = 0;

function createToast() {
  let toasts = $state<Toast[]>([]);

  function add(message: string, type: ToastType = 'info', duration = 4000) {
    const id = ++_counter;
    toasts = [...toasts, { id, message, type }];
    setTimeout(() => remove(id), duration);
  }

  function remove(id: number) {
    toasts = toasts.filter((t) => t.id !== id);
  }

  return {
    get toasts() { return toasts; },
    success: (msg: string) => add(msg, 'success'),
    error: (msg: string) => add(msg, 'error'),
    info: (msg: string) => add(msg, 'info'),
    warning: (msg: string) => add(msg, 'warning'),
    remove,
  };
}

export const toast = createToast();
