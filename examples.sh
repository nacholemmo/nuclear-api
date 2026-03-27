#!/bin/bash

# Nuclear Physics Monte Carlo API - Example Requests
# Make sure the server is running: uv run start

BASE_URL="http://localhost:8000"

echo "========================================="
echo "Nuclear Physics Monte Carlo API Examples"
echo "========================================="

# Test root endpoint
echo -e "\n1. Testing Root Endpoint..."
curl -X GET "${BASE_URL}/" | jq '.'

# Test PET simulation
echo -e "\n2. Testing PET Simulation..."
curl -X POST "${BASE_URL}/simular/pet" \
  -H "Content-Type: application/json" \
  -d '{
    "n_events": 100,
    "tumor_radius": 2.5,
    "tumor_center_x": 0.0,
    "tumor_center_y": 0.0
  }' | jq '.n_events, .energy_kev, .photon_pairs[0]'

# Test Shielding simulation (Lead)
echo -e "\n3. Testing Shielding Simulation (Plomo)..."
curl -X POST "${BASE_URL}/simular/blindaje" \
  -H "Content-Type: application/json" \
  -d '{
    "material": "Plomo",
    "thickness": 5.0,
    "energy_kev": 511.0,
    "n_photons": 10000,
    "use_random_walk": true
  }' | jq '{material, thickness, transmitted, absorbed, scattered, transmission_fraction, attenuation_coefficient}'

# Test Shielding simulation (Water)
echo -e "\n4. Testing Shielding Simulation (Agua)..."
curl -X POST "${BASE_URL}/simular/blindaje" \
  -H "Content-Type: application/json" \
  -d '{
    "material": "Agua",
    "thickness": 10.0,
    "energy_kev": 511.0,
    "n_photons": 10000,
    "use_random_walk": false
  }' | jq '{material, thickness, transmitted, transmission_fraction}'

# Test Decay simulation (Tc-99m)
echo -e "\n5. Testing Decay Simulation (Tc-99m)..."
curl -X POST "${BASE_URL}/simular/decay" \
  -H "Content-Type: application/json" \
  -d '{
    "isotope": "Tc-99m",
    "initial_activity_mbq": 100.0,
    "time_hours": 12.0,
    "n_simulations": 10000
  }' | jq '{isotope, half_life_hours, initial_activity_mbq, final_activity_mbq, simulated_activity_mbq}'

# Test Decay simulation (F-18)
echo -e "\n6. Testing Decay Simulation (F-18)..."
curl -X POST "${BASE_URL}/simular/decay" \
  -H "Content-Type: application/json" \
  -d '{
    "isotope": "F-18",
    "initial_activity_mbq": 50.0,
    "time_hours": 3.66,
    "n_simulations": 10000
  }' | jq '{isotope, half_life_hours, final_activity_mbq, simulated_activity_mbq}'

echo -e "\n========================================="
echo "All examples completed!"
echo "========================================="
