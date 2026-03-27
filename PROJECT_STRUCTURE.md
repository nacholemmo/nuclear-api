# Estructura del Proyecto

```
nuclear-api/
├── .env.example              # Variables de entorno de ejemplo
├── .gitignore                # Archivos ignorados por Git
├── .python-version           # Versión de Python (3.12)
├── CLAUDE.md                 # Contexto del proyecto para IA
├── README.md                 # Documentación principal
├── QUICKSTART.md             # Guía de inicio rápido
├── PROJECT_STRUCTURE.md      # Este archivo
├── pyproject.toml            # Configuración del proyecto y dependencias
├── uv.lock                   # Lock file de dependencias
│
├── main.py                   # ⭐ FastAPI app principal con endpoints
│
├── models/                   # 📦 Pydantic schemas (validación)
│   ├── __init__.py
│   ├── pet.py               # Request/Response para PET
│   ├── shielding.py         # Request/Response para Blindaje
│   └── decay.py             # Request/Response para Decaimiento
│
├── physics/                  # 🔬 Lógica de Monte Carlo
│   ├── __init__.py
│   └── monte_carlo.py       # Simulaciones físicas
│
├── data/                     # 📊 Constantes físicas
│   ├── __init__.py
│   └── constants.py         # Coeficientes de atenuación e isótopos
│
├── examples.sh              # 🧪 Ejemplos con cURL
└── test_api.py              # 🧪 Suite de tests con requests
```

## 📁 Descripción de Módulos

### `main.py`
- **FastAPI app** con 3 endpoints principales
- **CORS** configurado para Angular (localhost:4200)
- **Validación automática** con Pydantic
- **Documentación interactiva** en `/docs`

### `models/`
Schemas de validación con Pydantic v2:
- **pet.py**: `PETSimulationRequest`, `PETSimulationResponse`, `PhotonPair`
- **shielding.py**: `ShieldingSimulationRequest`, `ShieldingSimulationResponse`
- **decay.py**: `DecaySimulationRequest`, `DecaySimulationResponse`

### `physics/monte_carlo.py`
Funciones puras de simulación:
- `simulate_pet_annihilations()`: Genera eventos de aniquilación
- `simulate_shielding()`: Random walk o Beer-Lambert
- `simulate_radioactive_decay()`: Decaimiento estocástico

### `data/constants.py`
Datos físicos:
- `ISOTOPE_DATA`: Half-life y energías de 5 isótopos médicos
- `ATTENUATION_COEFFICIENTS`: μ(E) para Plomo, Agua, Hormigón

## 🔄 Flujo de Datos

```
Request (JSON)
    ↓
FastAPI Endpoint (main.py)
    ↓
Pydantic Validation (models/)
    ↓
Monte Carlo Simulation (physics/)
    ↓
NumPy Calculations
    ↓
Response (JSON)
```

## 🎯 Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Info de la API |
| `/simular/pet` | POST | Simulación PET |
| `/simular/blindaje` | POST | Simulación de blindaje |
| `/simular/decay` | POST | Decaimiento radiactivo |

## 🧮 Algoritmos Implementados

### PET
1. Generar punto aleatorio en círculo (tumor)
2. Generar ángulo aleatorio de emisión
3. Crear vectores unitarios opuestos (180°)

### Blindaje
**Método Estocástico (Random Walk):**
1. Fotón avanza en pasos de 0.1 cm
2. En cada paso: probabilidad de interacción = 1 - e^(-μΔx)
3. Si interactúa: 60% Compton, 40% Fotoeléctrico
4. Compton: reduce energía 20%, puede dispersarse
5. Fotoeléctrico: absorción total

**Método Determinístico:**
- Ley de Beer-Lambert: I/I₀ = e^(-μx)

### Decaimiento
1. Calcular λ = ln(2) / T½
2. Para cada átomo: random() > (1 - e^(-λt)) → sobrevive
3. Comparar con modelo determinístico: A(t) = A₀ e^(-λt)

## 🔧 Tecnologías

- **FastAPI**: Framework web async
- **Pydantic v2**: Validación de datos
- **NumPy**: Cálculos vectorizados
- **Uvicorn**: Servidor ASGI
- **uv**: Gestor de paquetes

## 📝 Notas de Desarrollo

- Todos los módulos usan **type hints** (Python 3.12)
- Separación clara: **endpoints** ≠ **lógica física**
- Funciones puras en `physics/` (fácil de testear)
- Constantes físicas en archivos separados
- CORS configurado para desarrollo local
