import type { Categoria } from '../types/index.js';

function createCategories() {
  let list = $state<Categoria[]>([]);
  let loading = $state(false);

  return {
    get list() {
      return list;
    },
    get loading() {
      return loading;
    },
    setList(l: Categoria[]) {
      list = l;
    },
    setLoading(l: boolean) {
      loading = l;
    },
    addCategory(c: Categoria) {
      list = [...list, c];
    },
    updateCategory(updated: Categoria) {
      list = list.map((c) => (c._id === updated._id ? updated : c));
    },
    removeCategory(id: string) {
      list = list.filter((c) => c._id !== id);
    },
  };
}

export const categories = createCategories();
