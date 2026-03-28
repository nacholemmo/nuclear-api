from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

from config import settings
from models import (
    PETSimulationRequest,
    PETSimulationResponse,
    PhotonPair,
    ShieldingSimulationRequest,
    ShieldingSimulationResponse,
    DecaySimulationRequest,
    DecaySimulationResponse,
)
from physics import (
    simulate_pet_annihilations,
    simulate_shielding,
    simulate_radioactive_decay,
)
from data import ISOTOPE_DATA

app = FastAPI(
    title="Nuclear Physics Monte Carlo Simulator",
    description="API for simulating PET imaging, radiation shielding, and radioactive decay using Monte Carlo methods",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Nuclear Physics Monte Carlo Simulator API",
        "version": "1.0.0",
        "endpoints": [
            "/simular/pet",
            "/simular/blindaje",
            "/simular/decay"
        ]
    }


@app.post("/simular/pet", response_model=PETSimulationResponse)
async def simulate_pet(request: PETSimulationRequest):
    """
    Simulate PET annihilation events.
    
    Each event generates:
    - Random origin point (x, y) within tumor radius
    - Two 511 keV photons emitted at 180° (back-to-back)
    
    Returns LOR (Lines of Response) data for visualization.
    """
    try:
        origins, directions1, directions2 = simulate_pet_annihilations(
            n_events=request.n_events,
            tumor_radius=request.tumor_radius,
            tumor_center_x=request.tumor_center_x,
            tumor_center_y=request.tumor_center_y,
        )
        
        photon_pairs = [
            PhotonPair(
                origin_x=float(origins[i, 0]),
                origin_y=float(origins[i, 1]),
                direction1_x=float(directions1[i, 0]),
                direction1_y=float(directions1[i, 1]),
                direction2_x=float(directions2[i, 0]),
                direction2_y=float(directions2[i, 1]),
            )
            for i in range(request.n_events)
        ]
        
        return PETSimulationResponse(
            n_events=request.n_events,
            photon_pairs=photon_pairs,
            energy_kev=511.0,
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")


@app.post("/simular/blindaje", response_model=ShieldingSimulationResponse)
async def simulate_shielding_endpoint(request: ShieldingSimulationRequest):
    """
    Simulate photon interaction with shielding material.
    
    Uses either:
    - Stochastic random walk (Monte Carlo)
    - Deterministic Beer-Lambert law
    
    Accounts for Compton scattering and photoelectric absorption.
    """
    try:
        transmitted, absorbed, scattered, mu = simulate_shielding(
            material=request.material.value,
            thickness=request.thickness,
            energy_kev=request.energy_kev,
            n_photons=request.n_photons,
            use_random_walk=request.use_random_walk,
        )
        
        transmission_fraction = transmitted / request.n_photons
        
        return ShieldingSimulationResponse(
            material=request.material.value,
            thickness=request.thickness,
            energy_kev=request.energy_kev,
            n_photons=request.n_photons,
            transmitted=transmitted,
            absorbed=absorbed,
            scattered=scattered,
            transmission_fraction=transmission_fraction,
            attenuation_coefficient=mu,
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")


@app.post("/simular/decay", response_model=DecaySimulationResponse)
async def simulate_decay(request: DecaySimulationRequest):
    """
    Simulate radioactive decay using Monte Carlo.
    
    Compares:
    - Deterministic exponential decay law
    - Stochastic Monte Carlo simulation
    
    Useful for understanding statistical fluctuations in small samples.
    """
    try:
        if request.isotope.value not in ISOTOPE_DATA:
            raise HTTPException(
                status_code=400,
                detail=f"Isotope {request.isotope.value} not found in database"
            )
        
        (
            final_activity,
            simulated_activity,
            n_initial,
            n_remaining,
            decay_constant,
            half_life,
        ) = simulate_radioactive_decay(
            isotope=request.isotope.value,
            initial_activity_mbq=request.initial_activity_mbq,
            time_hours=request.time_hours,
            n_simulations=request.n_simulations,
        )
        
        return DecaySimulationResponse(
            isotope=request.isotope.value,
            half_life_hours=half_life,
            initial_activity_mbq=request.initial_activity_mbq,
            time_hours=request.time_hours,
            final_activity_mbq=final_activity,
            simulated_activity_mbq=simulated_activity,
            n_initial_atoms=n_initial,
            n_remaining_atoms=n_remaining,
            decay_constant=decay_constant,
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")


def run_server():
    """Entry point for running the server via uv run."""
    import uvicorn
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
    )


if __name__ == "__main__":
    run_server()
