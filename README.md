# Distribution Grid Analysis using python API

This repository contains Python scripts that leverage OpenDSSDirect to perform power system analysis on distribution networks. The main script `python2dss.py` loads a distribution system model and solves the power flow at a specified loading level.

## Prerequisites

- Python 3.10
- pip (Python package installer) or Conda

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/RabayetSadnan/py2dss.git
cd py2dss
```

### 2. Create a Virtual Environment

#### Option 1: Using venv

##### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

##### On macOS and Linux:
```bash
python -m venv venv
source venv/bin/activate
```

#### Option 2: Using Conda

```bash
# Create a new conda environment with Python 3.10
conda create --name py2dss_api python=3.10

# Activate the environment
conda activate py2dss_api
```

### 3. Install Dependencies

#### Using pip:
```bash
pip install -r requirements.txt
```

#### Using conda (if available through conda):
```bash
conda install --file requirements.txt
```
If some packages are not available in conda, you can use pip within the conda environment:
```bash
conda install pip
pip install -r requirements.txt
```

The `requirements.txt` file should include:
```
opendssdirect.py
matplotlib
numpy
pandas
```

## File Structure

The repository should have the following structure:
```
py2dss/
├── python2dss.py            # The main Python script
├── requirements.txt         # Dependencies
├── README.md                # This file
└── OpenDSS_files/           # Directory containing OpenDSS models
    └── master_new_secondary_loads.dss
                             # Main DSS file
    └── master_new.dss       # Another Main DSS file
```

## Usage

To run the script, make sure your virtual environment is activated and execute:

```bash
python python2dss.py
```

Note: Ensure that the `OpenDSS_files` directory contains the necessary OpenDSS model files before running the script.

## Extending the Code

This script provides a base for power flow analysis. You can extend it to:
- Visualize voltage profiles
- Analyze power losses
- Perform contingency analysis
- Integrate distributed energy sources
- Conduct time-series simulations

## License

MIT License

Copyright (c) 2025 Rabayet Sadnan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.