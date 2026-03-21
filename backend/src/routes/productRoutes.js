const express = require('express');
const router = express.Router();
const path = require('path');
const fs = require('fs');
const multer = require('multer');
const ProductController = require('../controllers/productController');
const authJWT = require('../middleware/authMiddleware');

// ── Multer: almacenamiento con subdirectorios por producto/variante ────────────

function makeStorage(destFn) {
  return multer.diskStorage({
    destination(req, file, cb) {
      const dir = destFn(req);
      fs.mkdirSync(dir, { recursive: true });
      cb(null, dir);
    },
    filename(req, file, cb) {
      cb(null, `${Date.now()}${path.extname(file.originalname)}`);
    }
  });
}

// Para crear una opción con imágenes: usamos gId como directorio temporal (oId aún no existe)
const uploadOpcionNewImages = multer({
  storage: makeStorage(req =>
    path.join('/uploads', 'productos', req.params.id, req.params.gId)
  )
});

// Para añadir imágenes a una opción existente: usamos oId como directorio
const uploadOpcionImages = multer({
  storage: makeStorage(req =>
    path.join('/uploads', 'productos', req.params.id, req.params.oId)
  )
});

const uploadDefaultImages = multer({
  storage: makeStorage(req =>
    path.join('/uploads', 'productos', req.params.id, 'default')
  )
});

// ── Rutas ─────────────────────────────────────────────────────────────────────

// Lista y detalle
router.get('/', ProductController.getProducts.bind(ProductController));
router.get('/:id', ProductController.getProduct.bind(ProductController));

// CRUD básico (admin)
router.post('/', authJWT, ProductController.createProduct.bind(ProductController));
router.put('/:id', authJWT, ProductController.updateProduct.bind(ProductController));
router.delete('/:id', authJWT, ProductController.deleteProduct.bind(ProductController));

// Grupos de opciones
router.post('/:id/grupos', authJWT, ProductController.addGrupo.bind(ProductController));
router.put('/:id/grupos/:gId', authJWT, ProductController.updateGrupo.bind(ProductController));
router.delete('/:id/grupos/:gId', authJWT, ProductController.deleteGrupo.bind(ProductController));

// Opciones dentro de grupos
router.post(
  '/:id/grupos/:gId/opciones',
  authJWT,
  uploadOpcionNewImages.array('imagenes', 10),
  ProductController.addOpcion.bind(ProductController)
);
router.put(
  '/:id/grupos/:gId/opciones/:oId',
  authJWT,
  ProductController.updateOpcion.bind(ProductController)
);
router.delete(
  '/:id/grupos/:gId/opciones/:oId',
  authJWT,
  ProductController.deleteOpcion.bind(ProductController)
);

// Imágenes adicionales en opciones de color
router.post(
  '/:id/grupos/:gId/opciones/:oId/imagenes',
  authJWT,
  uploadOpcionImages.array('imagenes', 10),
  ProductController.addImagenesOpcion.bind(ProductController)
);
// filename viene como query param ?f=... para evitar problemas con barras en la ruta
router.delete(
  '/:id/grupos/:gId/opciones/:oId/imagenes',
  authJWT,
  ProductController.deleteImagenOpcion.bind(ProductController)
);

// Imágenes default
router.post(
  '/:id/imagenes-default',
  authJWT,
  uploadDefaultImages.array('imagenes', 10),
  ProductController.addImagenesDefault.bind(ProductController)
);
// filename viene como query param ?f=...
router.delete(
  '/:id/imagenes-default',
  authJWT,
  ProductController.deleteImagenDefault.bind(ProductController)
);

module.exports = router;
