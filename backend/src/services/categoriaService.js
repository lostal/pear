const Categoria = require('../models/Categoria');
const Producto = require('../models/Producto');
const client = require('../config/redis');

const CACHE_KEY = 'categorias:lista';
const CACHE_TTL = 300;

class CategoriaService {
  async getAll() {
    const cached = await client.get(CACHE_KEY);
    if (cached) return JSON.parse(cached);

    const categorias = await Categoria.find().sort({ orden: 1 });
    await client.set(CACHE_KEY, JSON.stringify(categorias), { EX: CACHE_TTL });
    return categorias;
  }

  async create(data) {
    const categoria = new Categoria(data);
    await categoria.save();
    await client.del(CACHE_KEY);
    return categoria;
  }

  async update(id, data) {
    const categoria = await Categoria.findByIdAndUpdate(id, data, { new: true });
    await client.del(CACHE_KEY);
    return categoria;
  }

  async delete(id) {
    const enUso = await Producto.exists({ categoria: id });
    if (enUso) throw new Error('CATEGORIA_EN_USO');
    await Categoria.findByIdAndDelete(id);
    await client.del(CACHE_KEY);
  }
}

module.exports = new CategoriaService();
