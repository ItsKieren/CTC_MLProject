# CrackShark

## Summary
**CrackShark** is an AI-driven cybersecurity tool designed to detect potential botnet activity and alert sysadmins to enact change. Additionally, CrackSharp is able to save IP addresses to a database of known botnets which can be used to block incoming traffic temporarily or permanently. The AI model behind this uses a Random Forest classification algorithm in order to determine if a subset of internet traffic packet data follows similar patterns to the labeled training data. Overall CrackSharp offers a complete solution for network security professionals or organizations looking to protect their infrastructure from DDOS or DOS attacks popular in the modern age. 

## Mission Statement
Our mission is to provide a lightweight, open-source, and user-friendly solution for detecting botnet activity in real-time, helping organizations and individuals secure their networks against persistent cyber threats.

## Features
- Real-time automated network monitoring 
- Suspicious IP Tracking
- Process and save analyzed network traffic data in house
- Queue based log analysis
- GUI based concurrent visualization

## Setup
1. **Clone Repository**:
   ```bash
   git clone git@github.com:ItsKieren/CTC_MLProject.git
   cd CTC_MLProject
   ```

2. **Set Up Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   .\venv\Scripts\activate   # Windows
   ```
   
3. **Install Dependencies**:
   ```bash
   # Ensure Python 3.10.12 is installed
   pip install -r requirements.txt
   ```
   
4. **Unzip Model**:
   ```bash
   7z x CTC_MLProeject/models/random_forest_model.7z
   ```

5. **Run Application**:
   ```bash
   python dump.py
   python monitor.py
   ```



## Troubleshooting
| Issue | Solution |
|-------|----------|
| Performance Slowdowns | Ensure sufficient allocated system resources as CrackShark is lightweight and should run efficiently on systems with as little as  2GB RAM and an Intel I3 CPU |
| Installation Issues | Verify dependencies and ensure program is running as administrator|
| False Positives/Negatives | Update ML model with new data with included training script |


## Contributing
We welcome contributions! Please follow these steps:
1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Submit a pull request with a detailed description of your changes

## Team | 404NotFound 
| Role | Member |
|------|--------|
| AI Designer | Andrew Sykes |
| Front End | Chloe Zhang |
| Backend | Owin Rojas |
| QA & Documentation | Eldwin C |
| Data Processing | Kieren A |

## Credits
  
This project uses the following technologies, libraries, and datasets:

**Languages -** Python, Bash\
**Frameworks -** Flask, Bootstrap\
**Libraries -** Scapy, Scikit-learn, Pandas, NumPy, Chart.js\
**Training Dataset -** DReLAB (Deep REinforcement Learning Adversarial Botnet dataset)

## License
[MIT](LICENSE.md)
