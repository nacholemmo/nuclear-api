from pydantic import BaseModel, Field, field_validator


class PETSimulationRequest(BaseModel):
    n_events: int = Field(
        ...,
        gt=0,
        le=1_000_000,
        description="Number of annihilation events to simulate"
    )
    tumor_radius: float = Field(
        ...,
        gt=0,
        le=50,
        description="Radius of the tumor in cm"
    )
    tumor_center_x: float = Field(
        default=0.0,
        description="X coordinate of tumor center in cm"
    )
    tumor_center_y: float = Field(
        default=0.0,
        description="Y coordinate of tumor center in cm"
    )


class PhotonPair(BaseModel):
    origin_x: float = Field(..., description="X coordinate of annihilation point (cm)")
    origin_y: float = Field(..., description="Y coordinate of annihilation point (cm)")
    direction1_x: float = Field(..., description="X component of first photon unit vector")
    direction1_y: float = Field(..., description="Y component of first photon unit vector")
    direction2_x: float = Field(..., description="X component of second photon unit vector")
    direction2_y: float = Field(..., description="Y component of second photon unit vector")


class PETSimulationResponse(BaseModel):
    n_events: int = Field(..., description="Number of events simulated")
    photon_pairs: list[PhotonPair] = Field(..., description="List of photon pairs from annihilations")
    energy_kev: float = Field(default=511.0, description="Photon energy in keV")
