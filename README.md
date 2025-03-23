# 🛡️ Botnet Detection Tool

## 📝 Summary
The **Botnet Detection Tool** is an AI-driven cybersecurity application designed to detect and alert users about potential botnet activity within their network. It leverages a Random Forest classifier to analyze network traffic patterns, detect abnormal behavior, and provide real-time alerts with suspicious IP tracking. Our tool processes network traffic data in real-time, utilizing advanced machine learning algorithms to identify potential threats and malicious activities. The system maintains a comprehensive database of suspicious IPs and provides detailed analytics through an intuitive console interface. With features like queue-based processing, automated file handling, and robust error recovery, this tool offers a complete solution for network security professionals and organizations looking to protect their infrastructure from botnet threats.

## 🎯 Mission Statement
Our mission is to provide a robust, adaptive, and user-friendly solution for detecting botnet activity in real-time, helping organizations and individuals secure their networks against evolving cyber threats. We strive to:
- Empower security professionals with advanced AI-driven detection capabilities
- Reduce false positives through sophisticated machine learning algorithms
- Provide comprehensive threat intelligence through detailed IP tracking and analysis
- Ensure seamless integration into existing security workflows
- Maintain high performance and reliability through robust error handling
- Adapt to emerging threats through continuous model updates
- Make advanced security tools accessible to organizations of all sizes

By combining cutting-edge technology with user-friendly design, we aim to create a more secure digital environment where organizations can confidently manage and protect their network infrastructure against increasingly sophisticated botnet attacks.

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
   git clone git@github.com:ItsKieren/CTC_MLProject.git
   cd CTC_MLProject
   ```

3. **Set Up Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   .\venv\Scripts\activate   # Windows
   ```

4. **Run Application**:
   ```bash
   python dump.py
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
**DReLAB Dataset** (Deep REinforcement Learning Adversarial Botnet dataset)  
DOI: 10.17632/nf22d786tj.1  
Published: December 9, 2020  
Contributors: Andrea Venturi, Michele Colajanni

## 📄 License
© 2025 | 404NotFound Team - Hackathon @ Concordia University 2025
