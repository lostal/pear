const Producto = require('../models/Producto');
const client = require('../config/redis');
const fs = require('fs');
const path = require('path');

const TTL_LIST = 120;
const TTL_SINGLE = 300;

async function invalidateProductLists(categoriaSlug) {
  await client.del('productos:todos');
  if (categoriaSlug) await client.del(`productos:cat:${categoriaSlug}`);
}

async function invalidateProduct(id) {
  await client.del(`producto:${id}`);
}

function deleteFile(relPath) {
  if (!relPath) return;
  try { fs.unlinkSync(path.join('/uploads', relPath)); } catch (_) {}
}

class ProductService {
  // ── List & Single ──────────────────────────────────────────────

  async getAllProducts(categoriaSlug) {
    const cacheKey = categoriaSlug ? `productos:cat:${categoriaSlug}` : 'productos:todos';
    const cached = await client.get(cacheKey);
    if (cached) return JSON.parse(cached);

    const query = { activo: true };
    if (categoriaSlug) {
      // join through Categoria to filter by slug
      const Categoria = require('../models/Categoria');
      const cat = await Categoria.findOne({ slug: categoriaSlug });
      if (cat) query.categoria = cat._id;
      else return [];
    }

    const products = await Producto.find(query)
      .populate('categoria')
      .sort({ orden: 1 });

    await client.set(cacheKey, JSON.stringify(products), { EX: TTL_LIST });
    return products;
  }

  async getProductById(id) {
    const cacheKey = `producto:${id}`;
    const cached = await client.get(cacheKey);
    if (cached) return JSON.parse(cached);

    const product = await Producto.findById(id).populate('categoria');
    if (!product) return null;

    await client.set(cacheKey, JSON.stringify(product), { EX: TTL_SINGLE });
    return product;
  }

  // ── CRUD básico ────────────────────────────────────────────────

  async createProduct(data) {
    const producto = new Producto(data);
    await producto.save();
    await producto.populate('categoria');
    await invalidateProductLists(producto.categoria?.slug);
    return producto;
  }

  async updateProduct(id, data) {
    const producto = await Producto.findByIdAndUpdate(id, data, { new: true }).populate('categoria');
    if (!producto) return null;
    await invalidateProduct(id);
    await invalidateProductLists(producto.categoria?.slug);
    return producto;
  }

  async deleteProduct(id) {
    const producto = await Producto.findById(id);
    if (!producto) return;
    // Soft delete
    await Producto.findByIdAndUpdate(id, { activo: false });
    await invalidateProduct(id);
    await invalidateProductLists(producto.categoria?.slug);
  }

  // ── Grupos de opciones ─────────────────────────────────────────

  async addGrupo(id, grupoData) {
    const producto = await Producto.findByIdAndUpdate(
      id,
      { $push: { gruposOpciones: grupoData } },
      { new: true }
    ).populate('categoria');
    await this._invalidateAll(producto);
    return producto;
  }

  async updateGrupo(id, gId, grupoData) {
    const producto = await Producto.findOneAndUpdate(
      { _id: id, 'gruposOpciones._id': gId },
      { $set: { 'gruposOpciones.$.nombre': grupoData.nombre, 'gruposOpciones.$.tipo': grupoData.tipo } },
      { new: true }
    ).populate('categoria');
    await this._invalidateAll(producto);
    return producto;
  }

  async deleteGrupo(id, gId) {
    const producto = await Producto.findById(id).populate('categoria');
    const grupo = producto.gruposOpciones.id(gId);
    if (grupo && grupo.tipo === 'color') {
      grupo.opciones.forEach(op => op.imagenes.forEach(img => deleteFile(img)));
    }
    await Producto.findByIdAndUpdate(id, { $pull: { gruposOpciones: { _id: gId } } });
    await this._invalidateAll(producto);
  }

  // ── Opciones dentro de grupos ──────────────────────────────────

  async addOpcion(id, gId, opcionData) {
    const producto = await Producto.findOneAndUpdate(
      { _id: id, 'gruposOpciones._id': gId },
      { $push: { 'gruposOpciones.$.opciones': opcionData } },
      { new: true }
    ).populate('categoria');
    await this._invalidateAll(producto);
    return producto;
  }

  async updateOpcion(id, gId, oId, opcionData) {
    const producto = await Producto.findById(id).populate('categoria');
    const grupo = producto.gruposOpciones.id(gId);
    const opcion = grupo?.opciones.id(oId);
    if (!opcion) return null;
    Object.assign(opcion, opcionData);
    await producto.save();
    await this._invalidateAll(producto);
    return producto;
  }

  async deleteOpcion(id, gId, oId) {
    const producto = await Producto.findById(id).populate('categoria');
    const grupo = producto.gruposOpciones.id(gId);
    const opcion = grupo?.opciones.id(oId);
    if (opcion) {
      opcion.imagenes.forEach(img => deleteFile(img));
      grupo.opciones.pull(oId);
      await producto.save();
    }
    await this._invalidateAll(producto);
  }

  // ── Imágenes en opciones de color ──────────────────────────────

  async addImagenesToOpcion(id, gId, oId, filenames) {
    const producto = await Producto.findById(id).populate('categoria');
    const grupo = producto.gruposOpciones.id(gId);
    const opcion = grupo?.opciones.id(oId);
    if (!opcion) return null;
    opcion.imagenes.push(...filenames);
    await producto.save();
    await this._invalidateAll(producto);
    return producto;
  }

  async deleteImagenFromOpcion(id, gId, oId, filename) {
    const producto = await Producto.findById(id).populate('categoria');
    const grupo = producto.gruposOpciones.id(gId);
    const opcion = grupo?.opciones.id(oId);
    if (!opcion) return null;
    opcion.imagenes = opcion.imagenes.filter(img => img !== filename);
    await producto.save();
    deleteFile(filename);
    await this._invalidateAll(producto);
    return producto;
  }

  // ── Imágenes default ───────────────────────────────────────────

  async addImagenesDefault(id, filenames) {
    const producto = await Producto.findByIdAndUpdate(
      id,
      { $push: { imagenesDefault: { $each: filenames } } },
      { new: true }
    ).populate('categoria');
    await this._invalidateAll(producto);
    return producto;
  }

  async deleteImagenDefault(id, filename) {
    const producto = await Producto.findByIdAndUpdate(
      id,
      { $pull: { imagenesDefault: filename } },
      { new: true }
    ).populate('categoria');
    deleteFile(filename);
    await this._invalidateAll(producto);
    return producto;
  }

  // ── Helpers ────────────────────────────────────────────────────

  async _invalidateAll(producto) {
    await invalidateProduct(producto._id.toString());
    await invalidateProductLists(producto.categoria?.slug);
  }
}

module.exports = new ProductService();
