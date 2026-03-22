const express = require('express');
const router = express.Router();
const CategoriaController = require('../controllers/categoriaController');
const authJWT = require('../middleware/authMiddleware');

router.get('/', CategoriaController.getAll.bind(CategoriaController));
router.post('/', authJWT, CategoriaController.create.bind(CategoriaController));
router.put('/reorder', authJWT, CategoriaController.reorder.bind(CategoriaController));
router.put('/:id', authJWT, CategoriaController.update.bind(CategoriaController));
router.delete('/:id', authJWT, CategoriaController.delete.bind(CategoriaController));

module.exports = router;
