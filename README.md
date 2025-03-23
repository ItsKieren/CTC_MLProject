# Botnet Detection Tool
Botnet Detection Tool is an AI-driven cybersecurity application designed to detect and alert users about potential botnet activity within their network. It uses machine learning algorithms to analyze network traffic, detect abnormal behavior, and provide real-time alerts.

### User Stories

#### The following functionality is completed:

- [ x ] User can start network traffic capture to analyze incoming and outgoing network data in real time, allowing for proactive threat monitoring.
- [ x ] User can stop network traffic capture to halt data collection.
- [ x ] User can download network traffic data in CSV format for further analysis.
- [ x ] User can visualize traffic patterns using graphs showing traffic trends, protocol distribution, and port category distribution.
- [ x ] User can view real-time alerts on botnet activities (potential threats).
- [ x ] User can view detailed packet information, such as packet size, source/destination IPs, and protocol type.
- [ x ] Real-time status indicators show the capture status and active botnet detection.
  
### App Walkthough GIF
Here's a walkthrough of the implemented user stories:

<img src="https://github.com/ChloeZhang1/FlixsterPart2/blob/main/Fix2WalkThrough.gif" width=250><br>

GIF created with LiceCap

### Notes
Challenges Encountered:

- Processing real-time network traffic efficiently without causing performance slowdowns requires optimizing data collection and minimizing system resource usage

- Graphs and dashboards need to update dynamically while remaining responsive, as network traffic could generate thousands of packets per second.

- Detecting botnet activity involves training models to distinguish between normal and malicious network behavior. It is important that flagging normal activity as botnet-related (false positives) or failing to detect actual threats (false negatives) is reduced.

### Open-source libraries used
- Scapy: For packet sniffing and network traffic analysis.

- Matplotlib: For visualizing network activity.

- Flask: For building the web interface.

- Collections: For efficiently managing network connection data.

- CSV: For saving and analyzing captured network traffic data.

- Sklearn (for AI/ML): For implementing machine learning algorithms that help detect botnet behavior in network traffic.

### License
Copyright [2025] [404NotFound Team - Hackathon @ Concordia University 2025]
