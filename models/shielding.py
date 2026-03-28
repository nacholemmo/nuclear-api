from enum import Enum
from pydantic import BaseModel, Field, field_validator

from config import settings


class MaterialType(str, Enum):
    LEAD = "Plomo"
    WATER = "Agua"
    CONCRETE = "Hormigón"


class InteractionType(str, Enum):
    TRANSMITTED = "transmitted"
    ABSORBED = "absorbed"
    SCATTERED = "scattered"


class ShieldingSimulationRequest(BaseModel):
    material: MaterialType = Field(
        ...,
        description="Shielding material type"
    )
    thickness: float = Field(
        ...,
        gt=0,
        le=100,
        description="Material thickness in cm"
    )
    energy_kev: float = Field(
        ...,
        gt=0,
        le=10_000,
        description="Initial photon energy in keV"
    )
    n_photons: int = Field(
        ...,
        gt=0,
        description="Number of photons to simulate"
    )
    use_random_walk: bool = Field(
        default=True,
        description="Use stochastic random walk (True) or Beer-Lambert law (False)"
    )

    @field_validator("n_photons")
    @classmethod
    def validate_n_photons(cls, v: int) -> int:
        if v > settings.MAX_PHOTONS:
            raise ValueError(f"n_photons must be <= {settings.MAX_PHOTONS}")
        return v


class ShieldingSimulationResponse(BaseModel):
    material: str = Field(..., description="Material used")
    thickness: float = Field(..., description="Thickness in cm")
    energy_kev: float = Field(..., description="Initial energy in keV")
    n_photons: int = Field(..., description="Total photons simulated")
    transmitted: int = Field(..., description="Number of photons transmitted")
    absorbed: int = Field(..., description="Number of photons absorbed")
    scattered: int = Field(..., description="Number of photons scattered")
    transmission_fraction: float = Field(..., description="Fraction of photons transmitted")
    attenuation_coefficient: float = Field(..., description="Linear attenuation coefficient (cm⁻¹)")
