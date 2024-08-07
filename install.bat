@echo off

:: Install Python dependencies
pip install -r requirements.txt

:: Install the Python package
python setup.py install
