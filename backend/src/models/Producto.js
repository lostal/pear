const mongoose = require('mongoose');

const opcionSchema = new mongoose.Schema({
  valor: { type: String, required: true },
  codigoHex: { type: String },         // solo tipo 'color'
  imagenes: { type: [String], default: [] }, // solo tipo 'color'
  modificadorPrecio: { type: Number, default: 0 } // solo tipo 'storage'/'button'
});

const grupoOpcionesSchema = new mongoose.Schema({
  tipo: { type: String, enum: ['color', 'storage', 'button'], required: true },
  nombre: { type: String, required: true },
  opciones: [opcionSchema]
});

const productoSchema = new mongoose.Schema({
  nombre: { type: String, required: true },
  descripcion: { type: String, default: '' },
  categoria: { type: mongoose.Schema.Types.ObjectId, ref: 'Categoria' },
  precioBase: { type: Number, required: true },
  imagenesDefault: { type: [String], default: [] },
  gruposOpciones: [grupoOpcionesSchema],
  activo: { type: Boolean, default: true },
  orden: { type: Number, default: 0 }
}, { timestamps: true });

module.exports = mongoose.model('Producto', productoSchema);
