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
  };
}

export const categories = createCategories();
