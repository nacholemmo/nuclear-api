# Quick Start Guide

## 🚀 Inicio Rápido

### 1. Instalar dependencias

```bash
uv pip install -e .
```

### 2. Iniciar el servidor

```bash
# Opción 1: Script bash
./start.sh

# Opción 2: Con uv run
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en `http://localhost:8000`

### 3. Verificar que funciona

Abre tu navegador en: `http://localhost:8000/docs`

Verás la documentación interactiva de Swagger UI.

## 📝 Ejemplos de Uso

### Desde Python

```bash
python test_api.py
```

### Desde Bash/cURL

```bash
./examples.sh
```

### Desde tu aplicación Angular

```typescript
// En tu servicio Angular
import { HttpClient } from '@angular/common/http';

export class NuclearPhysicsService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  simulatePET(params: any) {
    return this.http.post(`${this.apiUrl}/simular/pet`, params);
  }

  simulateShielding(params: any) {
    return this.http.post(`${this.apiUrl}/simular/blindaje`, params);
  }

  simulateDecay(params: any) {
    return this.http.post(`${this.apiUrl}/simular/decay`, params);
  }
}
```

## 🧪 Prueba Manual con cURL

### PET Simulation

```bash
curl -X POST "http://localhost:8000/simular/pet" \
  -H "Content-Type: application/json" \
  -d '{
    "n_events": 1000,
    "tumor_radius": 2.5
  }'
```

### Shielding Simulation

```bash
curl -X POST "http://localhost:8000/simular/blindaje" \
  -H "Content-Type: application/json" \
  -d '{
    "material": "Plomo",
    "thickness": 5.0,
    "energy_kev": 511.0,
    "n_photons": 10000
  }'
```

### Decay Simulation

```bash
curl -X POST "http://localhost:8000/simular/decay" \
  -H "Content-Type: application/json" \
  -d '{
    "isotope": "Tc-99m",
    "initial_activity_mbq": 100.0,
    "time_hours": 12.0
  }'
```

## 🔍 Validación de Datos

Todos los endpoints validan automáticamente:

- **Valores positivos**: espesores, energías, actividades
- **Rangos válidos**: n_events ≤ 1,000,000
- **Materiales válidos**: Plomo, Agua, Hormigón
- **Isótopos válidos**: Tc-99m, F-18, I-131, Ga-67, Tl-201

Si envías datos inválidos, recibirás un error 422 con detalles específicos.

## 📊 Visualización de Resultados

### PET - Dibujar LORs

```javascript
// En tu frontend Angular
photonPairs.forEach(pair => {
  // Línea desde el origen en dirección 1
  const line1 = {
    x1: pair.origin_x,
    y1: pair.origin_y,
    x2: pair.origin_x + pair.direction1_x * 50, // 50 cm de longitud
    y2: pair.origin_y + pair.direction1_y * 50
  };
  
  // Línea desde el origen en dirección 2 (opuesta)
  const line2 = {
    x1: pair.origin_x,
    y1: pair.origin_y,
    x2: pair.origin_x + pair.direction2_x * 50,
    y2: pair.origin_y + pair.direction2_y * 50
  };
  
  // Dibujar ambas líneas
  drawLine(line1);
  drawLine(line2);
});
```

## 🐛 Troubleshooting

### Error: "Port 8000 already in use"

```bash
# Encuentra el proceso usando el puerto
lsof -i :8000

# Mata el proceso
kill -9 <PID>
```

### Error: "Module not found"

```bash
# Reinstala las dependencias
uv pip install -e .
```

### CORS Error desde Angular

Verifica que tu app Angular esté corriendo en `http://localhost:4200`. Si usas otro puerto, actualiza `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:TU_PUERTO"],
    ...
)
```
