const ProductService = require('../services/productService');
const path = require('path');

function isAdmin(req, res) {
  if (req.user.role !== 'admin') {
    res.status(403).json({ error: 'Solo admin' });
    return false;
  }
  return true;
}

class ProductController {
  // ── List & Single ──────────────────────────────────────────────

  async getProducts(req, res) {
    try {
      const products = await ProductService.getAllProducts(req.query.categoria);
      res.json(products);
    } catch (err) {
      res.status(500).json({ error: 'Error al obtener productos' });
    }
  }

  async getProduct(req, res) {
    try {
      const product = await ProductService.getProductById(req.params.id);
      if (!product) return res.status(404).json({ error: 'Producto no encontrado' });
      res.json(product);
    } catch (err) {
      res.status(500).json({ error: 'Error al obtener producto' });
    }
  }

  // ── CRUD básico ────────────────────────────────────────────────

  async createProduct(req, res) {
    try {
      if (!isAdmin(req, res)) return;
      const { nombre, descripcion, categoria, precioBase, orden } = req.body;
      const product = await ProductService.createProduct({
        nombre, descripcion, categoria, precioBase: Number(precioBase), orden: Number(orden) || 0
      });
      res.status(201).json(product);
    } catch (err) {
      res.status(500).json({ error: 'Error al crear producto' });
    }
  }

  async updateProduct(req, res) {
    try {
      if (!isAdmin(req, res)) return;
      const allowed = ['nombre', 'descripcion', 'categoria', 'precioBase', 'activo', 'orden'];
      const data = {};
      allowed.forEach(k => { if (req.body[k] !== undefined) data[k] = req.body[k]; });
      const product = await ProductService.updateProduct(req.params.id, data);
      if (!product) return res.status(404).json({ error: 'Producto no encontrado' });
      res.json(product);
    } catch (err) {
      res.status(500).json({ error: 'Error al actualizar producto' });
    }
  }

  async deleteProduct(req, res) {
    try {
      if (!isAdmin(req, res)) return;
      await ProductService.deleteProduct(req.params.id);
      res.json({ message: 'Producto desactivado' });
    } catch (err) {
      res.status(500).json({ error: 'Error al eliminar producto' });
    }
  }

  // ── Grupos de opciones ─────────────────────────────────────────

  async addGrupo(req, res) {
    try {
      if (!isAdmin(req, res)) return;
      const product = await ProductService.addGrupo(req.params.id, req.body);
      res.status(201).json(product);
    } catch (err) {
      res.status(500).json({ error: 'Error al añadir grupo' });
    }
  }

  async updateGrupo(req, res) {
    try {
      if (!isAdmin(req, res)) return;
      const product = await ProductService.updateGrupo(req.params.id, req.params.gId, req.body);
      res.json(product);
    } catch (err) {
      res.status(500).json({ error: 'Error al actualizar grupo' });
    }
  }

  async deleteGrupo(req, res) {
    try {
      if (!isAdmin(req, res)) return;
      await ProductService.deleteGrupo(req.params.id, req.params.gId);
      res.json({ message: 'Grupo eliminado' });
    } catch (err) {
      res.status(500).json({ error: 'Error al eliminar grupo' });
    }
  }

  // ── Opciones ───────────────────────────────────────────────────

  async addOpcion(req, res) {
    try {
      if (!isAdmin(req, res)) return;
      // For color options, images are uploaded separately
      const opcionData = { ...req.body };
      if (req.files && req.files.length > 0) {
        opcionData.imagenes = req.files.map(f => path.relative('/uploads', f.path));
      }
      const product = await ProductService.addOpcion(req.params.id, req.params.gId, opcionData);
      res.status(201).json(product);
    } catch (err) {
      res.status(500).json({ error: 'Error al añadir opción' });
    }
  }

  async updateOpcion(req, res) {
    try {
      if (!isAdmin(req, res)) return;
      const product = await ProductService.updateOpcion(
        req.params.id, req.params.gId, req.params.oId, req.body
      );
      if (!product) return res.status(404).json({ error: 'Opción no encontrada' });
      res.json(product);
    } catch (err) {
      res.status(500).json({ error: 'Error al actualizar opción' });
    }
  }

  async deleteOpcion(req, res) {
    try {
      if (!isAdmin(req, res)) return;
      await ProductService.deleteOpcion(req.params.id, req.params.gId, req.params.oId);
      res.json({ message: 'Opción eliminada' });
    } catch (err) {
      res.status(500).json({ error: 'Error al eliminar opción' });
    }
  }

  // ── Imágenes de opciones de color ──────────────────────────────

  async addImagenesOpcion(req, res) {
    try {
      if (!isAdmin(req, res)) return;
      if (!req.files || req.files.length === 0) return res.status(400).json({ error: 'Sin archivos' });
      const filenames = req.files.map(f => path.relative('/uploads', f.path));
      const product = await ProductService.addImagenesToOpcion(
        req.params.id, req.params.gId, req.params.oId, filenames
      );
      res.json(product);
    } catch (err) {
      res.status(500).json({ error: 'Error al subir imágenes' });
    }
  }

  async deleteImagenOpcion(req, res) {
    try {
      if (!isAdmin(req, res)) return;
      const filename = req.query.f;
      if (!filename) return res.status(400).json({ error: 'Falta el parámetro f' });
      const product = await ProductService.deleteImagenFromOpcion(
        req.params.id, req.params.gId, req.params.oId, filename
      );
      res.json(product);
    } catch (err) {
      res.status(500).json({ error: 'Error al eliminar imagen' });
    }
  }

  // ── Imágenes default ───────────────────────────────────────────

  async addImagenesDefault(req, res) {
    try {
      if (!isAdmin(req, res)) return;
      if (!req.files || req.files.length === 0) return res.status(400).json({ error: 'Sin archivos' });
      const filenames = req.files.map(f => path.relative('/uploads', f.path));
      const product = await ProductService.addImagenesDefault(req.params.id, filenames);
      res.json(product);
    } catch (err) {
      res.status(500).json({ error: 'Error al subir imágenes' });
    }
  }

  async deleteImagenDefault(req, res) {
    try {
      if (!isAdmin(req, res)) return;
      const filename = req.query.f;
      if (!filename) return res.status(400).json({ error: 'Falta el parámetro f' });
      const product = await ProductService.deleteImagenDefault(req.params.id, filename);
      res.json(product);
    } catch (err) {
      res.status(500).json({ error: 'Error al eliminar imagen' });
    }
  }
}

module.exports = new ProductController();
