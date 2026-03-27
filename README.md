# Nuclear Physics Monte Carlo Simulator API

API REST desarrollada con FastAPI para simular procesos de física nuclear aplicados a Medicina Nuclear y Blindaje mediante el método de Monte Carlo.

## 🎯 Características

- **Simulación PET**: Aniquilaciones positrón-electrón con emisión de fotones de 511 keV
- **Simulación de Blindaje**: Interacción de fotones con materiales (Plomo, Agua, Hormigón)
- **Decaimiento Radiactivo**: Simulación estocástica de isótopos médicos (Tc-99m, F-18, I-131, etc.)

## 🚀 Instalación

```bash
# Instalar dependencias con uv
uv pip install -e .

# O manualmente
uv pip install fastapi uvicorn numpy scipy
```

## 🏃 Ejecución

```bash
# Opción 1: Usando el script start.sh
./start.sh

# Opción 2: Con uv run
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Opción 3: Directamente con uvicorn (si está instalado globalmente)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

## 📡 Endpoints

### 1. `/simular/pet` - Simulación PET

Simula eventos de aniquilación positrón-electrón.

**Request:**
```json
{
  "n_events": 1000,
  "tumor_radius": 2.5,
  "tumor_center_x": 0.0,
  "tumor_center_y": 0.0
}
```

**Response:**
```json
{
  "n_events": 1000,
  "photon_pairs": [
    {
      "origin_x": 1.2,
      "origin_y": -0.8,
      "direction1_x": 0.707,
      "direction1_y": 0.707,
      "direction2_x": -0.707,
      "direction2_y": -0.707
    }
  ],
  "energy_kev": 511.0
}
```

### 2. `/simular/blindaje` - Simulación de Blindaje

Simula la interacción de fotones con materiales de blindaje.

**Request:**
```json
{
  "material": "Plomo",
  "thickness": 5.0,
  "energy_kev": 511.0,
  "n_photons": 10000,
  "use_random_walk": true
}
```

**Response:**
```json
{
  "material": "Plomo",
  "thickness": 5.0,
  "energy_kev": 511.0,
  "n_photons": 10000,
  "transmitted": 1250,
  "absorbed": 7800,
  "scattered": 950,
  "transmission_fraction": 0.125,
  "attenuation_coefficient": 0.4103
}
```

### 3. `/simular/decay` - Decaimiento Radiactivo

Simula el decaimiento radiactivo de isótopos médicos.

**Request:**
```json
{
  "isotope": "Tc-99m",
  "initial_activity_mbq": 100.0,
  "time_hours": 12.0,
  "n_simulations": 10000
}
```

**Response:**
```json
{
  "isotope": "Tc-99m",
  "half_life_hours": 6.01,
  "initial_activity_mbq": 100.0,
  "time_hours": 12.0,
  "final_activity_mbq": 25.12,
  "simulated_activity_mbq": 24.98,
  "n_initial_atoms": 10000,
  "n_remaining_atoms": 2498,
  "decay_constant": 0.1153
}
```

## 🏗️ Estructura del Proyecto

```
nuclear-api/
├── main.py                 # FastAPI app y endpoints
├── models/                 # Pydantic schemas
│   ├── pet.py
│   ├── shielding.py
│   └── decay.py
├── physics/                # Lógica Monte Carlo
│   └── monte_carlo.py
├── data/                   # Constantes físicas
│   └── constants.py
├── pyproject.toml          # Configuración del proyecto
└── README.md
```

## 🔬 Física Implementada

### PET (Positron Emission Tomography)
- Generación aleatoria de puntos de aniquilación dentro del tumor
- Emisión de fotones back-to-back (180°) de 511 keV
- Vectores unitarios para visualización de LOR (Lines of Response)

### Blindaje
- **Método Determinístico**: Ley de Beer-Lambert (I = I₀ e^(-μx))
- **Método Estocástico**: Random Walk con probabilidades de interacción
- Efectos Compton y fotoeléctrico
- Coeficientes de atenuación interpolados por energía

### Decaimiento Radiactivo
- Ley exponencial: A(t) = A₀ e^(-λt)
- Simulación estocástica átomo por átomo
- Comparación entre modelo determinístico y Monte Carlo

## 🧪 Isótopos Soportados

- **Tc-99m**: T½ = 6.01 h (SPECT)
- **F-18**: T½ = 1.83 h (PET)
- **I-131**: T½ = 192.5 h (Terapia)
- **Ga-67**: T½ = 78.3 h (Diagnóstico)
- **Tl-201**: T½ = 73.1 h (Cardiología)

## 🛡️ Materiales de Blindaje

- **Plomo** (Pb): Alta densidad, uso estándar
- **Agua** (H₂O): Referencia, moderador
- **Hormigón**: Blindaje estructural

## 🔧 CORS

Configurado para aceptar requests desde `http://localhost:4200` (Angular).

## 📚 Referencias

- NIST XCOM: Photon Cross Sections Database
- IAEA Medical Physics Handbook
- Cherry & Sorenson: Physics in Nuclear Medicine

## 👨‍💻 Autor

**Ignacio Lemmo** - Ingeniero de Software & Bioingeniero
