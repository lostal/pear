import type { Product, Categoria, ProductosPorCategoria } from '../types/index.js';

function createProducts() {
  let list = $state<Product[]>([]);
  let loading = $state(false);

  const byCategory = $derived.by(() => {
    const map = new Map<string, ProductosPorCategoria>();
    for (const p of list) {
      const catId = p.categoria?._id ?? '__sin_categoria__';
      if (!map.has(catId)) {
        map.set(catId, {
          categoria: p.categoria ?? ({ nombre: 'Sin categoría', slug: '', orden: 9999 } as Categoria),
          productos: []
        });
      }
      map.get(catId)!.productos.push(p);
    }
    return Array.from(map.values()).sort(
      (a, b) => (a.categoria.orden ?? 0) - (b.categoria.orden ?? 0)
    );
  });

  return {
    get list() { return list; },
    get loading() { return loading; },
    get byCategory() { return byCategory; },

    setList(l: Product[]) { list = l; },
    setLoading(l: boolean) { loading = l; },

    addProduct(p: Product) { list = [...list, p]; },
    updateProduct(updated: Product) {
      list = list.map(p => p._id === updated._id ? updated : p);
    },
    removeProduct(id: string) {
      list = list.filter(p => p._id !== id);
    },
  };
}

export const products = createProducts();
