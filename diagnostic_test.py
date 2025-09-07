#!/usr/bin/env python3
"""
Diagnostic test script to identify SPCI package issues
"""

import sys
import os

def test_python_path():
    """Check if spci is in Python path"""
    print("Testing Python path...")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Python path:")
    for path in sys.path:
        print(f"  {path}")
    
    # Try to find spci in installed packages
    try:
        import site
        site_packages = site.getsitepackages()
        print(f"\nSite packages directories:")
        for sp in site_packages:
            print(f"  {sp}")
            if os.path.exists(sp):
                spci_dirs = [d for d in os.listdir(sp) if 'spci' in d.lower()]
                if spci_dirs:
                    print(f"    SPCI-related directories: {spci_dirs}")
    except Exception as e:
        print(f"Could not check site packages: {e}")

def test_direct_import():
    """Try different import methods"""
    print("\n" + "="*50)
    print("TESTING DIRECT IMPORT METHODS")
    print("="*50)
    
    # Method 1: Direct import
    print("\n1. Testing 'import spci'...")
    try:
        import spci
        print(f"✅ SUCCESS: import spci")
        print(f"   Package location: {spci.__file__ if hasattr(spci, '__file__') else 'Unknown'}")
        print(f"   Package version: {getattr(spci, '__version__', 'Unknown')}")
        return True
    except Exception as e:
        print(f"❌ FAILED: import spci - {e}")
    
    # Method 2: Try importing individual modules
    print("\n2. Testing individual module imports...")
    modules_to_test = [
        'spci.PI_class_EnbPI',
        'spci.SPCI_class', 
        'spci.data',
        'spci.utils_SPCI',
        'spci.utils_EnbPI',
        'spci.visualize'
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ SUCCESS: {module}")
        except Exception as e:
            print(f"❌ FAILED: {module} - {e}")
    
    # Method 3: Check if package directory exists
    print("\n3. Checking package installation...")
    try:
        import spci
        import os
        if hasattr(spci, '__path__'):
            package_path = spci.__path__[0]
            print(f"✅ Package path found: {package_path}")
            if os.path.exists(package_path):
                files = os.listdir(package_path)
                print(f"   Files in package: {files}")
            else:
                print(f"❌ Package path does not exist!")
        else:
            print("❌ Package has no __path__ attribute")
    except Exception as e:
        print(f"❌ Could not check package path: {e}")
    
    return False

def test_import_with_path():
    """Try adding package to path manually"""
    print("\n" + "="*50)
    print("TESTING MANUAL PATH ADDITION")
    print("="*50)
    
    # Try to find the package installation
    import site
    import os
    
    for site_dir in site.getsitepackages():
        potential_path = os.path.join(site_dir, 'spci')
        if os.path.exists(potential_path):
            print(f"Found spci at: {potential_path}")
            sys.path.insert(0, site_dir)
            try:
                import spci
                print("✅ SUCCESS with manual path addition")
                return True
            except Exception as e:
                print(f"❌ Still failed with manual path: {e}")
    
    return False

def test_numpy_compatibility():
    """Test for numpy compatibility issues"""
    print("\n" + "="*50)
    print("TESTING NUMPY COMPATIBILITY")
    print("="*50)
    
    try:
        import numpy as np
        print(f"✅ NumPy version: {np.__version__}")
        
        # Test problematic packages individually
        problematic_packages = [
            'skranger',
            'sklearn_quantile', 
            'statsmodels'
        ]
        
        for pkg in problematic_packages:
            try:
                __import__(pkg)
                print(f"✅ {pkg}: OK")
            except Exception as e:
                if "numpy.dtype size changed" in str(e):
                    print(f"❌ {pkg}: NUMPY COMPATIBILITY ISSUE")
                    print(f"   Error: {e}")
                else:
                    print(f"⚠️  {pkg}: {e}")
                    
    except Exception as e:
        print(f"❌ NumPy import failed: {e}")
    
    return False

def main():
    """Run all diagnostic tests"""
    print("="*60)
    print("SPCI PACKAGE DIAGNOSTIC TEST")
    print("="*60)
    
    test_python_path()
    test_numpy_compatibility()
    success = test_direct_import()
    
    if not success:
        test_import_with_path()
    
    print("\n" + "="*60)
    print("DIAGNOSTIC COMPLETE")
    print("="*60)
    
    if not success:
        print("\n🔧 SUGGESTED FIXES:")
        print("1. For numpy compatibility issues:")
        print("   pip uninstall skranger sklearn_quantile -y")
        print("   pip install --no-cache-dir --force-reinstall skranger sklearn_quantile")
        print("\n2. Alternative - downgrade numpy:")
        print("   pip install 'numpy<2.0'")
        print("\n3. Reinstall the package:")
        print("   pip uninstall spci -y")
        print("   pip install git+https://github.com/michaelbiafore/SPCI-code_xXuXie.git")
        print("\n4. Or install from local directory:")
        print("   pip uninstall spci -y") 
        print('   pip install "A:\\Packages\\SPCI\\SPCI-code_xXuXie"')
        print("\n5. Check for dependency issues in the package modules")

if __name__ == "__main__":
    main()
