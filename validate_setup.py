#!/usr/bin/env python3
"""
Validation script to check if the Nuclear Physics API is properly set up.
Run this before starting the server to ensure all components are working.
"""

import sys
from pathlib import Path


def check_imports():
    """Check if all required packages are installed."""
    print("Checking imports...")
    
    try:
        import fastapi
        print(f"  ✓ FastAPI {fastapi.__version__}")
    except ImportError:
        print("  ✗ FastAPI not found")
        return False
    
    try:
        import numpy as np
        print(f"  ✓ NumPy {np.__version__}")
    except ImportError:
        print("  ✗ NumPy not found")
        return False
    
    try:
        import uvicorn
        print(f"  ✓ Uvicorn {uvicorn.__version__}")
    except ImportError:
        print("  ✗ Uvicorn not found")
        return False
    
    try:
        import pydantic
        print(f"  ✓ Pydantic {pydantic.__version__}")
    except ImportError:
        print("  ✗ Pydantic not found")
        return False
    
    return True


def check_project_structure():
    """Check if all required files and directories exist."""
    print("\nChecking project structure...")
    
    required_files = [
        "main.py",
        "models/__init__.py",
        "models/pet.py",
        "models/shielding.py",
        "models/decay.py",
        "physics/__init__.py",
        "physics/monte_carlo.py",
        "data/__init__.py",
        "data/constants.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} not found")
            all_exist = False
    
    return all_exist


def check_models():
    """Check if Pydantic models can be imported."""
    print("\nChecking Pydantic models...")
    
    try:
        from models import (
            PETSimulationRequest,
            PETSimulationResponse,
            PhotonPair,
            ShieldingSimulationRequest,
            ShieldingSimulationResponse,
            DecaySimulationRequest,
            DecaySimulationResponse,
        )
        print("  ✓ All models imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Error importing models: {e}")
        return False


def check_physics():
    """Check if physics functions can be imported."""
    print("\nChecking physics engine...")
    
    try:
        from physics import (
            simulate_pet_annihilations,
            simulate_shielding,
            simulate_radioactive_decay,
        )
        print("  ✓ All physics functions imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Error importing physics: {e}")
        return False


def check_data():
    """Check if data constants can be imported."""
    print("\nChecking data constants...")
    
    try:
        from data import ISOTOPE_DATA, ATTENUATION_COEFFICIENTS
        
        print(f"  ✓ Isotopes available: {len(ISOTOPE_DATA)}")
        print(f"  ✓ Materials available: {len(ATTENUATION_COEFFICIENTS)}")
        
        for isotope in ISOTOPE_DATA:
            print(f"    - {isotope}")
        
        return True
    except Exception as e:
        print(f"  ✗ Error importing data: {e}")
        return False


def test_physics_functions():
    """Run basic tests on physics functions."""
    print("\nTesting physics functions...")
    
    try:
        import numpy as np
        from physics import (
            simulate_pet_annihilations,
            simulate_shielding,
            simulate_radioactive_decay,
        )
        
        origins, dir1, dir2 = simulate_pet_annihilations(10, 2.5)
        assert origins.shape == (10, 2), "PET simulation shape mismatch"
        assert np.allclose(np.linalg.norm(dir1, axis=1), 1.0), "Direction vectors not normalized"
        assert np.allclose(dir1 + dir2, 0.0), "Photons not back-to-back"
        print("  ✓ PET simulation works")
        
        trans, abs_, scat, mu = simulate_shielding("Plomo", 5.0, 511.0, 1000, True)
        assert trans + abs_ + scat == 1000, "Photon count mismatch"
        assert mu > 0, "Invalid attenuation coefficient"
        print("  ✓ Shielding simulation works")
        
        final, sim, n_init, n_rem, lam, t_half = simulate_radioactive_decay(
            "Tc-99m", 100.0, 12.0, 1000
        )
        assert 0 <= final <= 100, "Invalid final activity"
        assert 0 <= sim <= 100, "Invalid simulated activity"
        assert n_rem <= n_init, "More atoms remaining than initial"
        print("  ✓ Decay simulation works")
        
        return True
    except Exception as e:
        print(f"  ✗ Error testing physics: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all validation checks."""
    print("=" * 60)
    print("Nuclear Physics API - Setup Validation")
    print("=" * 60)
    
    checks = [
        ("Imports", check_imports),
        ("Project Structure", check_project_structure),
        ("Pydantic Models", check_models),
        ("Physics Engine", check_physics),
        ("Data Constants", check_data),
        ("Physics Functions", test_physics_functions),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Unexpected error in {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to start the server.")
        print("\nRun: uv run start")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
