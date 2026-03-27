# Notas Técnicas - Nuclear Physics API

## 🔬 Fundamentos Físicos

### PET (Positron Emission Tomography)

**Proceso de Aniquilación:**
- Positrón (e⁺) + Electrón (e⁻) → 2γ (511 keV cada uno)
- Emisión back-to-back (180°) por conservación de momento
- Energía: E = m₀c² = 0.511 MeV por fotón

**Implementación:**
```python
# Distribución uniforme en círculo (tumor)
r = √U(0,1) × R_tumor
θ = U(0, 2π)

# Posición de aniquilación
x = x_center + r·cos(θ)
y = y_center + r·sin(θ)

# Direcciones opuestas
φ = U(0, 2π)
d₁ = (cos(φ), sin(φ))
d₂ = -d₁
```

### Blindaje de Radiación

**Ley de Beer-Lambert (Determinístico):**
```
I(x) = I₀ · e^(-μx)
```
- I₀: Intensidad inicial
- μ: Coeficiente de atenuación lineal (cm⁻¹)
- x: Espesor del material (cm)

**Random Walk (Estocástico):**
```python
for cada fotón:
    while posición < espesor:
        P_interacción = 1 - e^(-μ·Δx)
        
        if random() < P_interacción:
            if random() < P_fotoeléctrico:
                # Absorción total
                fotón absorbido
            else:
                # Dispersión Compton
                E_nueva = 0.8 · E_actual
                if E_nueva < 50 keV:
                    fotón absorbido
                else:
                    continuar con E_nueva
```

**Coeficientes de Atenuación:**
- Interpolación lineal entre valores tabulados
- Fuente: NIST XCOM Database
- Rango: 100 keV - 10 MeV

### Decaimiento Radiactivo

**Ley Exponencial:**
```
N(t) = N₀ · e^(-λt)
A(t) = A₀ · e^(-λt)
```
- λ = ln(2) / T½ (constante de decaimiento)
- T½: Vida media
- A: Actividad (MBq)

**Monte Carlo:**
```python
for cada átomo:
    P_decaimiento = 1 - e^(-λt)
    if random() < P_decaimiento:
        átomo decae
    else:
        átomo sobrevive
```

## 📊 Datos Físicos

### Isótopos Médicos

| Isótopo | T½ (h) | E_γ (keV) | Aplicación |
|---------|--------|-----------|------------|
| Tc-99m  | 6.01   | 140.5     | SPECT (diagnóstico general) |
| F-18    | 1.83   | 511.0     | PET (oncología, neurología) |
| I-131   | 192.5  | 364.0     | Terapia (tiroides) |
| Ga-67   | 78.3   | 93.3      | Infecciones, tumores |
| Tl-201  | 73.1   | 167.0     | Cardiología |

### Coeficientes de Atenuación (μ) a 511 keV

| Material | μ (cm⁻¹) | HVL (cm) |
|----------|----------|----------|
| Plomo    | 0.4103   | 1.69     |
| Agua     | 0.0966   | 7.17     |
| Hormigón | 0.1877   | 3.69     |

HVL (Half-Value Layer) = ln(2) / μ

## 🧮 Algoritmos Numéricos

### Generación de Puntos Aleatorios en Círculo

**Método Correcto (Implementado):**
```python
r = sqrt(random()) * R  # ✓ Distribución uniforme en área
θ = random() * 2π
```

**Método Incorrecto:**
```python
r = random() * R  # ✗ Concentra puntos en el centro
θ = random() * 2π
```

### Interpolación de Coeficientes

```python
# Interpolación lineal en escala log-log para mayor precisión
energies = [100, 200, 300, ..., 10000] keV
mu_values = [5.549, 1.525, 0.7854, ..., 0.0685] cm⁻¹

mu(E) = np.interp(E, energies, mu_values)
```

### Eficiencia Computacional

**Vectorización con NumPy:**
- ✓ `np.random.uniform(0, 1, n)` - Genera n valores a la vez
- ✗ `[random() for _ in range(n)]` - Loop Python (100x más lento)

**Complejidad:**
- PET: O(n) - n eventos
- Shielding (Beer-Lambert): O(1) - cálculo directo
- Shielding (Random Walk): O(n·m) - n fotones, m pasos promedio
- Decay: O(n) - n átomos

## 🔧 Consideraciones de Implementación

### Type Hints (Python 3.12)

```python
from numpy.typing import NDArray
import numpy as np

def simulate_pet(
    n_events: int,
    radius: float
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    ...
```

### Validación con Pydantic

```python
class PETSimulationRequest(BaseModel):
    n_events: int = Field(..., gt=0, le=1_000_000)
    tumor_radius: float = Field(..., gt=0, le=50)
```

### Separación de Responsabilidades

```
main.py          → Endpoints HTTP (FastAPI)
models/          → Validación de datos (Pydantic)
physics/         → Lógica pura (NumPy)
data/            → Constantes físicas
```

## 🎯 Casos de Uso

### 1. Optimización de Detectores PET
- Simular diferentes geometrías de tumor
- Analizar distribución de LORs
- Optimizar posicionamiento de detectores

### 2. Diseño de Blindaje
- Calcular espesor necesario para atenuación deseada
- Comparar materiales (costo vs eficacia)
- Validar normativas de protección radiológica

### 3. Planificación de Dosis
- Calcular actividad residual en pacientes
- Planificar tiempos de espera post-inyección
- Optimizar logística de radiofármacos

## 📈 Validación de Resultados

### PET
- Verificar que |d₁| = |d₂| = 1 (vectores unitarios)
- Verificar que d₁ · d₂ = -1 (opuestos)
- Distribución uniforme en el área del tumor

### Blindaje
- Comparar Random Walk vs Beer-Lambert
- Verificar conservación: transmitted + absorbed + scattered = n_photons
- HVL experimental ≈ ln(2)/μ

### Decay
- Actividad simulada ≈ actividad teórica (para n grande)
- Fluctuaciones estadísticas ~ √n
- λ = ln(2) / T½

## 🔍 Referencias

1. **NIST XCOM**: Photon Cross Sections Database
   - https://physics.nist.gov/PhysRefData/Xcom/html/xcom1.html

2. **Cherry & Sorenson**: Physics in Nuclear Medicine (4th Ed.)
   - Capítulo 6: Interaction of Radiation with Matter
   - Capítulo 18: Positron Emission Tomography

3. **IAEA**: Radiation Protection and Safety of Radiation Sources
   - Safety Standards Series No. GSR Part 3

4. **Knoll**: Radiation Detection and Measurement (4th Ed.)
   - Capítulo 2: Radiation Interactions
