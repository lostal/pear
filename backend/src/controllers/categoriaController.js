const CategoriaService = require('../services/categoriaService');

class CategoriaController {
  async getAll(req, res) {
    try {
      const categorias = await CategoriaService.getAll();
      res.json(categorias);
    } catch (err) {
      res.status(500).json({ error: 'Error al obtener categorías' });
    }
  }

  async create(req, res) {
    try {
      if (req.user.role !== 'admin') return res.status(403).json({ error: 'Solo admin' });
      const categoria = await CategoriaService.create(req.body);
      res.status(201).json(categoria);
    } catch (err) {
      if (err.code === 11000) return res.status(409).json({ error: 'Slug ya existe' });
      res.status(500).json({ error: 'Error al crear categoría' });
    }
  }

  async update(req, res) {
    try {
      if (req.user.role !== 'admin') return res.status(403).json({ error: 'Solo admin' });
      const categoria = await CategoriaService.update(req.params.id, req.body);
      if (!categoria) return res.status(404).json({ error: 'Categoría no encontrada' });
      res.json(categoria);
    } catch (err) {
      res.status(500).json({ error: 'Error al actualizar categoría' });
    }
  }

  async delete(req, res) {
    try {
      if (req.user.role !== 'admin') return res.status(403).json({ error: 'Solo admin' });
      await CategoriaService.delete(req.params.id);
      res.json({ message: 'Categoría eliminada' });
    } catch (err) {
      if (err.message === 'CATEGORIA_EN_USO') {
        return res.status(409).json({ error: 'No se puede eliminar: hay productos en esta categoría' });
      }
      res.status(500).json({ error: 'Error al eliminar categoría' });
    }
  }
}

module.exports = new CategoriaController();
