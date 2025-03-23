## ⚙️ **Installation**

### **Two-step setup: First install the prerequisites, then set up the project.**

### **Prerequisites**

#### **Install Dependencies**

Before setting up the project, ensure you have the necessary dependencies installed:

1. **Install Python (Recommended version v3.10.12)**:
   Install Python on your system from the official [Python website](https://www.python.org/downloads/release/python-31012).
   - **Windows users**: Ensure Python is added to your system PATH. If required, follow this guide to [add Python to PATH](https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-so-it-finds-my-modules-packages).

   After installation, verify Python is installed correctly by checking the version:

   ```bash
   python --version
   ```

   You should see an output like:
   ```
   Python 3.10.12
   ```

2. **Install Pip (Python Package Installer)**:
   Pip is typically included with Python. To ensure it's installed correctly, run:

   ```bash
   pip --version
   ```

   If it’s not installed, follow the instructions on the [Pip installation page](https://pip.pypa.io/en/stable/installation/).

#### **Install Required Libraries**:

Ensure the required libraries for the project are installed by running the following command:

```bash
pip install -r requirements.txt
```

This will install the necessary dependencies listed in the `requirements.txt` file.

### **Setup**

1. **Clone the Project**:

   Clone the project repository to your local machine:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Setup Virtual Environment** (Optional but recommended):

   Create and activate a virtual environment to manage dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # For Linux/macOS
   .\venv\Scripts\activate    # For Windows
   ```


#### **🚀 Run the Project**

To start the application, run the following command:

```bash
python main.py
```

You should see three services running:

- **Server**: Runs on `http://localhost:<port>` (replace `<port>` with your actual port number).
- **Botnet detection**: Monitors network traffic for potential botnet activity.
- **Web Interface**: A Flask server that handles requests and visualizations.

### **📖 API Documentation**

If your project exposes any APIs, provide a section for the API documentation here. For example:

- **POST /start**: Starts the packet capture and botnet detection.
  - **Request**: Starts the capture process.
  - **Response**: Returns a status message (e.g., `"Capture Started"`).
  
- **POST /stop**: Stops the packet capture.
  - **Request**: Stops monitoring traffic.
  - **Response**: Returns a status message (e.g., `"Capture Stopped"`).

- **GET /download_csv**: Allows the user to download captured network data as a CSV file.
  - **Response**: Provides a downloadable CSV file containing packet information.

**Example:**

```bash
curl -X POST http://localhost:5000/start
```

You can add more details based on your specific routes and API functionality.

### **Known Issues**

There are some known issues that can be ignored for now:


---

### Conclusion

This structure organizes the setup and installation instructions, providing users with clear steps to get started with your project. Additionally, it includes instructions for running the project and handling any potential issues (e.g., GCP quota-related problems).
