import requests
import json

BASE_URL = "http://localhost:8000"


def test_pet_simulation():
    """Test PET simulation endpoint."""
    print("\n=== Testing PET Simulation ===")
    
    payload = {
        "n_events": 100,
        "tumor_radius": 2.5,
        "tumor_center_x": 0.0,
        "tumor_center_y": 0.0
    }
    
    response = requests.post(f"{BASE_URL}/simular/pet", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Events simulated: {data['n_events']}")
        print(f"✓ Energy: {data['energy_kev']} keV")
        print(f"✓ First photon pair:")
        print(f"  Origin: ({data['photon_pairs'][0]['origin_x']:.3f}, {data['photon_pairs'][0]['origin_y']:.3f})")
        print(f"  Dir1: ({data['photon_pairs'][0]['direction1_x']:.3f}, {data['photon_pairs'][0]['direction1_y']:.3f})")
        print(f"  Dir2: ({data['photon_pairs'][0]['direction2_x']:.3f}, {data['photon_pairs'][0]['direction2_y']:.3f})")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)


def test_shielding_simulation():
    """Test shielding simulation endpoint."""
    print("\n=== Testing Shielding Simulation ===")
    
    payload = {
        "material": "Plomo",
        "thickness": 5.0,
        "energy_kev": 511.0,
        "n_photons": 10000,
        "use_random_walk": True
    }
    
    response = requests.post(f"{BASE_URL}/simular/blindaje", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Material: {data['material']}")
        print(f"✓ Thickness: {data['thickness']} cm")
        print(f"✓ Transmitted: {data['transmitted']} ({data['transmission_fraction']*100:.2f}%)")
        print(f"✓ Absorbed: {data['absorbed']}")
        print(f"✓ Scattered: {data['scattered']}")
        print(f"✓ μ: {data['attenuation_coefficient']:.4f} cm⁻¹")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)


def test_decay_simulation():
    """Test radioactive decay simulation endpoint."""
    print("\n=== Testing Decay Simulation ===")
    
    payload = {
        "isotope": "Tc-99m",
        "initial_activity_mbq": 100.0,
        "time_hours": 12.0,
        "n_simulations": 10000
    }
    
    response = requests.post(f"{BASE_URL}/simular/decay", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Isotope: {data['isotope']}")
        print(f"✓ Half-life: {data['half_life_hours']} h")
        print(f"✓ Initial activity: {data['initial_activity_mbq']} MBq")
        print(f"✓ Final activity (deterministic): {data['final_activity_mbq']:.2f} MBq")
        print(f"✓ Final activity (Monte Carlo): {data['simulated_activity_mbq']:.2f} MBq")
        print(f"✓ Atoms remaining: {data['n_remaining_atoms']}/{data['n_initial_atoms']}")
        print(f"✓ λ: {data['decay_constant']:.4f} h⁻¹")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)


def test_root():
    """Test root endpoint."""
    print("\n=== Testing Root Endpoint ===")
    
    response = requests.get(f"{BASE_URL}/")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Message: {data['message']}")
        print(f"✓ Version: {data['version']}")
        print(f"✓ Endpoints: {', '.join(data['endpoints'])}")
    else:
        print(f"✗ Error: {response.status_code}")


if __name__ == "__main__":
    print("=" * 60)
    print("Nuclear Physics Monte Carlo API - Test Suite")
    print("=" * 60)
    
    try:
        test_root()
        test_pet_simulation()
        test_shielding_simulation()
        test_decay_simulation()
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to API")
        print("Make sure the server is running: uvicorn main:app --reload")
