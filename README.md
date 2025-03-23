# Botnet Detection Tool
Botnet Detection Tool is an AI-driven cybersecurity application designed to detect and alert users about potential botnet activity within their network. It uses machine learning algorithms to analyze network traffic, detect abnormal behavior, and provide real-time alerts.

### User Stories

#### REQUIRED (10pts)

- [ x ] User can start network traffic capture to analyze incoming and outgoing network data.
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

## Open-source libraries used
Scapy: For packet sniffing and network traffic analysis.

Matplotlib: For visualizing network activity.

Flask: For building the web interface.

Collections: For efficiently managing network connection data.

CSV: For saving and analyzing captured network traffic data.

Sklearn (for AI/ML): For implementing machine learning algorithms that help detect botnet behavior in network traffic.

###License
Copyright [2025] [404NotFound Team - Hackathon @ Concordia University 2025]


Describe any challenges encountered while building the app.

### Open-source libraries used

- [Android Async HTTP](https://github.com/codepath/CPAsyncHttpClient) - Simple asynchronous HTTP requests with JSON parsing
- [Glide](https://github.com/bumptech/glide) - Image loading and caching library for Androids
