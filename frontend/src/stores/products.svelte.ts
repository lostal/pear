import type { Product } from '../types/index.js';

function createProducts() {
  let list = $state<Product[]>([]);
  let search = $state('');
  let loading = $state(false);

  const filtered = $derived(
    list.filter((p) =>
      search.trim() === '' ||
      p.nombre.toLowerCase().includes(search.toLowerCase())
    ),
  );

  const count = $derived(filtered.length);

  return {
    get list() { return list; },
    get search() { return search; },
    get loading() { return loading; },
    get filtered() { return filtered; },
    get count() { return count; },

    setList(l: Product[]) { list = l; },
    setSearch(s: string) { search = s; },
    setLoading(l: boolean) { loading = l; },

    addProduct(p: Product) { list = [...list, p]; },
    updateProduct(updated: Product) {
      list = list.map((p) => (p._id === updated._id ? updated : p));
    },
    removeProduct(id: string) {
      list = list.filter((p) => p._id !== id);
    },
  };
}

export const products = createProducts();
