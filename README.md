Here are step-by-step instructions to install and run the screen recording app from the [GitHub repository](https://github.com/expertahmed/screenrecorder) on Windows, Linux, and macOS.

## Installation Steps

### Windows

#### 1. **Install Python**
   - Download and install Python 3.12 or later from the [official Python website](https://www.python.org/downloads/).
   - During installation, ensure you select the option to add Python to your PATH.

#### 2. **Install Git (optional)**
   - Download and install Git from [git-scm.com](https://git-scm.com/download/win) if you want to clone the repository directly.

#### 3. **Clone the Repository**
   - Open Command Prompt and run:
     ```bash
     git clone https://github.com/expertahmed/screenrecorder.git
     cd screenrecorder
     ```

#### 4. **Create a Virtual Environment**
   - Open Command Prompt as Administrator and navigate to the project directory.
   - Run the following commands to create and activate a virtual environment:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

#### 5. **Install Required Packages**
   - Install the necessary packages using pip:
     ```bash
     pip install -r requirements.txt
     ```

#### 6. **Run the Setup Script**
   - Run the setup script to install the application and create a desktop shortcut:
     ```bash
     python setup.py install
     ```

#### 7. **Run the Application**
   - Use the desktop shortcut created by the setup script to start the application.
   - Alternatively, you can run the application manually:
     ```bash
     python src\main.py
     ```

### Linux

#### 1. **Install Python and Pip**
   - Most Linux distributions come with Python pre-installed. If not, use the package manager to install Python:
     ```bash
     sudo apt-get update
     sudo apt-get install python3 python3-pip python3-venv
     ```

#### 2. **Install Git (optional)**
   - If you want to clone the repository directly:
     ```bash
     sudo apt-get install git
     ```

#### 3. **Clone the Repository**
   - Open a terminal and run:
     ```bash
     git clone https://github.com/expertahmed/screenrecorder.git
     cd screenrecorder
     ```

#### 4. **Create a Virtual Environment**
   - Run the following commands to create and activate a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

#### 5. **Install Required Packages**
   - Install the necessary packages using pip:
     ```bash
     pip install -r requirements.txt
     ```

#### 6. **Run the Setup Script**
   - Run the setup script to install the application and create a desktop shortcut:
     ```bash
     sudo python setup.py install
     ```

#### 7. **Run the Application**
   - Use the desktop shortcut created by the setup script to start the application.
   - Alternatively, you can run the application manually:
     ```bash
     python src/main.py
     ```

### macOS

#### 1. **Install Python and Pip**
   - Use Homebrew to install Python if it’s not already installed:
     ```bash
     brew install python
     ```

#### 2. **Install Git (optional)**
   - Install Git if you want to clone the repository directly:
     ```bash
     brew install git
     ```

#### 3. **Clone the Repository**
   - Open Terminal and run:
     ```bash
     git clone https://github.com/expertahmed/screenrecorder.git
     cd screenrecorder
     ```

#### 4. **Create a Virtual Environment**
   - Run the following commands to create and activate a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

#### 5. **Install Required Packages**
   - Install the necessary packages using pip:
     ```bash
     pip install -r requirements.txt
     ```

#### 6. **Run the Setup Script**
   - Run the setup script to install the application and create a desktop shortcut:
     ```bash
     sudo python setup.py install
     ```

#### 7. **Run the Application**
   - Use the desktop shortcut created by the setup script to start the application.
   - Alternatively, you can run the application manually:
     ```bash
     python src/main.py
     ```

## Additional Notes

- **Python Version**: Ensure that Python 3.12 or later is used as it provides support for modern features and libraries.
- **Permissions**: Administrative or sudo privileges are required for certain installation steps, especially for creating desktop shortcuts and installing system-wide dependencies.
- **Audio Input**: Ensure the microphone or audio input device is properly connected and selected in the application settings.
- **Dependencies**: The `requirements.txt` file should contain all necessary Python packages required for the application.

By following these steps, you can set up and run the screen recording application on Windows, Linux, and macOS. Each platform has its specific steps, mainly due to differences in package management and system configurations.
