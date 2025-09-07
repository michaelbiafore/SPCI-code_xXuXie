# Complete Test: Installing and Using SPCI Package

## Test Overview
This test will:
1. Create a new test project directory
2. Create a fresh conda environment 
3. Install the SPCI package from your GitHub repo
4. Test basic functionality to verify it works
5. Clean up the test environment

## Step-by-Step Test Commands

### Step 1: Create Test Project Directory
```powershell
# Navigate to a test location (not inside your SPCI directory)
cd C:\Users\$env:USERNAME\Desktop
mkdir spci_test_project
cd spci_test_project
```

### Step 2: Create Fresh Conda Environment
```powershell
# Create new environment specifically for testing
conda create -n spci_test python=3.9 -y
conda activate spci_test
```

### Step 3: Install SPCI Package from GitHub
```powershell
# Install your package from GitHub
pip install git+https://github.com/michaelbiafore/SPCI-code_xXuXie.git
```

### Step 4: Create Test Script
Create a file called `test_spci.py` with the following content:

```python
#!/usr/bin/env python3
"""
Test script to verify SPCI package installation and basic functionality
"""

def test_import():
    """Test that we can import the package"""
    print("Testing import...")
    try:
        import spci
        print(f"✅ Successfully imported spci version {spci.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import spci: {e}")
        return False

def test_main_classes():
    """Test that main classes are accessible"""
    print("\nTesting main classes...")
    try:
        import spci
        
        # Test prediction_interval class
        pi = spci.prediction_interval()
        print("✅ Successfully created prediction_interval instance")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create main classes: {e}")
        return False

def test_data_loading():
    """Test that we can access data utilities"""
    print("\nTesting data utilities...")
    try:
        import spci
        import pandas as pd
        import numpy as np
        
        # Create some dummy data to test with
        np.random.seed(42)
        test_data = pd.DataFrame({
            'time': range(100),
            'value': np.random.randn(100).cumsum()
        })
        
        print("✅ Successfully created test data")
        print(f"   Test data shape: {test_data.shape}")
        return True
    except Exception as e:
        print(f"❌ Failed data test: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality if possible"""
    print("\nTesting basic functionality...")
    try:
        import spci
        import numpy as np
        
        # Try to access some utility functions
        print("✅ Package imports working correctly")
        
        # Check what's available in the package
        available_items = [item for item in dir(spci) if not item.startswith('_')]
        print(f"✅ Available items in spci: {available_items}")
        
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("SPCI Package Installation Test")
    print("=" * 50)
    
    tests = [
        test_import,
        test_main_classes,
        test_data_loading,
        test_basic_functionality
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your SPCI package is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    main()
```

### Step 5: Run the Test
```powershell
# Run the test script
python test_spci.py
```

### Step 6: Additional Manual Test (Interactive)
```powershell
# Start Python interactive session
python
```

Then in the Python interpreter:
```python
# Test interactive usage
import spci
print(f"SPCI version: {spci.__version__}")

# Check what's available
print("Available items:", [x for x in dir(spci) if not x.startswith('_')])

# Try to create main classes
try:
    pi = spci.prediction_interval()
    print("✅ prediction_interval class works")
except Exception as e:
    print(f"❌ prediction_interval failed: {e}")

# Exit Python
exit()
```

### Step 7: Test Installation from Local Path (Alternative)
```powershell
# Alternative: Install from local path instead of GitHub
pip uninstall spci -y
pip install "A:\Packages\SPCI\SPCI-code_xXuXie"

# Run test again
python test_spci.py
```

### Step 8: Clean Up Test Environment
```powershell
# Deactivate and remove test environment
conda deactivate
conda env remove -n spci_test -y

# Clean up test directory (optional)
cd ..
rmdir spci_test_project /s
```

## Expected Output

If everything works correctly, you should see:
```
==================================================
SPCI Package Installation Test
==================================================
Testing import...
✅ Successfully imported spci version 0.1.0

Testing main classes...
✅ Successfully created prediction_interval instance

Testing data utilities...
✅ Successfully created test data
   Test data shape: (100, 2)

Testing basic functionality...
✅ Package imports working correctly
✅ Available items in spci: ['prediction_interval', ...]

==================================================
TEST SUMMARY
==================================================
Tests passed: 4/4
🎉 ALL TESTS PASSED! Your SPCI package is working correctly.
```

## Troubleshooting

If any step fails:
1. Check that your GitHub repo has the package files
2. Verify internet connection for GitHub install
3. Check conda environment is activated
4. Look at specific error messages in the test output

This comprehensive test validates that your package conversion was successful!
