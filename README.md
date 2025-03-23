# 🛡️ Botnet Detection Tool

## 📝 Summary
The **Botnet Detection Tool** is an AI-driven cybersecurity application designed to detect and alert users about potential botnet activity within their network. It leverages a Random Forest classifier to analyze network traffic patterns, detect abnormal behavior, and provide real-time alerts with suspicious IP tracking.

## 🎯 Mission Statement
Our mission is to provide a robust, adaptive, and user-friendly solution for detecting botnet activity in real-time, helping organizations and individuals secure their networks against evolving cyber threats.

## ⚠️ The Problem
Botnet attacks are a significant threat to cybersecurity, often used for:
- Large-scale Distributed Denial-of-Service (DDoS) attacks
- Data theft
- Other malicious activities

These attacks involve thousands or even millions of compromised devices, making detection difficult due to the vast volume and complexity of traffic.

Traditional botnet detection methods rely on signature-based or heuristic approaches, which can be ineffective against evolving botnet tactics. This tool addresses these challenges by using machine learning to analyze network traffic and distinguish between normal and malicious behavior.

## ✨ Features
| Feature | Description |
|---------|-------------|
| 🔍 Real-time Monitoring | Continuously monitor network traffic files in a specified directory |
| 📊 Queue System | Handle multiple files simultaneously with queue-based processing |
| 🚫 Suspicious IP Tracking | Track and log potentially malicious IP addresses with timestamps |
| 📁 CSV Export | Process and save analyzed network traffic data in CSV format |
| 🤖 Automated Processing | Automatically detect and process new network traffic files |
| 🛠️ Error Handling | Robust error handling with retry mechanisms |
| 📈 Progress Tracking | Real-time progress indicators and timing information |

## 🌟 How Are We Unique?
- **AI/ML-Driven Detection**: Uses a Random Forest classifier trained on real-world network traffic data
- **Real-time Processing**: Monitors directory for new files and processes them automatically
- **Comprehensive IP Tracking**: Maintains a database of suspicious IPs for threat analysis
- **Robust Error Handling**: Multiple retry attempts and graceful error recovery
- **User-friendly Output**: Clear, organized console output with visual indicators

## 🚀 Steps to Use
1. **Install Dependencies**:
   ```bash
   # Ensure Python 3.10.12 is installed
   pip install -r requirements.txt
   ```

2. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

3. **Set Up Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   .\venv\Scripts\activate   # Windows
   ```

4. **Run Application**:
   ```bash
   python monitor.py
   ```

## 🔍 Troubleshooting
| Issue | Solution |
|-------|----------|
| Performance Slowdowns | Ensure sufficient system resources |
| False Positives/Negatives | Update ML model with new data |
| Installation Issues | Verify Python and dependencies |

## 🤝 Contributing
We welcome contributions! Please follow these steps:
1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Submit a pull request with a detailed description of your changes

## 👥 Team
| Role | Member |
|------|--------|
| AI Designer | Andrew Sykes |
| Front End | Chloe Zhang |
| Backend | Owin Rojas |
| QA & Documentation | Eldwin C |

## 🙏 Credits
- **Pandas & NumPy**: Core data processing and numerical operations
- **Scikit-learn**: Machine learning implementation (Random Forest Classifier and Label Encoding)
- **Joblib**: Model and encoder serialization
- **Watchdog**: Real-time file system monitoring
- **Pathlib**: Path manipulation and directory creation
- **Threading**: Multi-threaded processing for file handling
- **Queue**: Thread-safe queue implementation for file processing
- **Logging**: Structured logging system
- **Datetime**: Timestamp handling and time-based operations
- **OS**: File system operations and path management

## 📄 License
© 2025 | 404NotFound Team - Hackathon @ Concordia University 2025
