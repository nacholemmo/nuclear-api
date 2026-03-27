# Nuclear Physics Simulator API (Monte Carlo)

## Project Context
- **Owner:** Ignacio Lemmo (Software Engineer & Bioengineer)
- **Tech Stack:** Python 3.12, FastAPI, NumPy, Uvicorn, uv (package manager).
- **Domain:** Medical Physics (PET/SPECT), Radiation Shielding, and Nuclear Decay.

## Engineering Standards
- **Environment:** Always use `uv` for dependency management.
- **Style:** Clean Code, PEP 8, Type Hinting mandatory (Python 3.12 syntax).
- **Validation:** Use Pydantic v2 for all Request/Response schemas.
- **Concurrency:** Use `async/await` for API endpoints, but offload heavy Monte Carlo loops to `NumPy` or `ProcessPoolExecutor` if necessary.

## Core Physics Logic (Monte Carlo)
- **PET Simulation:** Origin inside a specific radius (tumor), emission of 2 photons at 180° (511 keV).
- **Shielding:** Implementation of Beer-Lambert law vs. stochastic Random Walk using linear attenuation coefficients (μ).
- **Units:** Use MeV for energy, cm for distance, and MBq for activity.

## Common Commands
- **Install Deps:** `uv pip install -e .`
- **Run Dev Server:** `./start.sh` or `uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000`
- **Run Tests:** `python test_api.py` or `./examples.sh`
- **Validate Setup:** `python validate_setup.py`

## API Architecture
- `main.py`: FastAPI routes and CORS configuration.
- `models/`: Pydantic schemas for inputs/outputs.
- `physics/`: Pure logic for Monte Carlo and nuclear math.
- `data/`: Constants for attenuation coefficients (Lead, Water, Concrete).