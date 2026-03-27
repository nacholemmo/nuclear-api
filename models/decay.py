from enum import Enum
from pydantic import BaseModel, Field, field_validator


class IsotopeType(str, Enum):
    TC99M = "Tc-99m"
    F18 = "F-18"
    I131 = "I-131"
    GA67 = "Ga-67"
    TL201 = "Tl-201"


class DecaySimulationRequest(BaseModel):
    isotope: IsotopeType = Field(
        ...,
        description="Radioactive isotope"
    )
    initial_activity_mbq: float = Field(
        ...,
        gt=0,
        le=10_000,
        description="Initial activity in MBq"
    )
    time_hours: float = Field(
        ...,
        gt=0,
        le=1000,
        description="Time elapsed in hours"
    )
    n_simulations: int = Field(
        default=10_000,
        gt=0,
        le=1_000_000,
        description="Number of Monte Carlo simulations"
    )


class DecaySimulationResponse(BaseModel):
    isotope: str = Field(..., description="Isotope simulated")
    half_life_hours: float = Field(..., description="Half-life in hours")
    initial_activity_mbq: float = Field(..., description="Initial activity in MBq")
    time_hours: float = Field(..., description="Time elapsed in hours")
    final_activity_mbq: float = Field(..., description="Final activity in MBq (deterministic)")
    simulated_activity_mbq: float = Field(..., description="Simulated activity in MBq (stochastic)")
    n_initial_atoms: int = Field(..., description="Initial number of atoms simulated")
    n_remaining_atoms: int = Field(..., description="Remaining atoms after simulation")
    decay_constant: float = Field(..., description="Decay constant λ (h⁻¹)")
