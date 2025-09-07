from setuptools import setup

# Read requirements from requirements.txt
with open('requirements.txt', 'r') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read README for long description
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "SPCI - Sequential Prediction Conformal Inference Package"

setup(
    name="spci",
    version="0.1.0",
    author="SPCI Contributors",
    description="Sequential Prediction Conformal Inference Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # Explicitly specify the package structure
    packages=['spci'],
    package_dir={'spci': '.'},
    
    # Include all Python modules in the root directory
    py_modules=[
        'PI_class_EnbPI',
        'SPCI_class', 
        'data',
        'utils_SPCI',
        'utils_EnbPI',
        'visualize'
    ],
    
    python_requires=">=3.7",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    include_package_data=True,
    package_data={
        'spci': ['Data/*.csv'],
    },
)
