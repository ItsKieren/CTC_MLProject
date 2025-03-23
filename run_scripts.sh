#!/bin/bash

# Create required directories if they don't exist
mkdir -p scapy_packet_files
mkdir -p scapy_processed_files

# Function to handle cleanup on script termination
cleanup() {
    echo "Stopping all processes..."
    pkill -f "python3 dump.py"
    pkill -f "python3 monitor.py"
    exit 0
}

# Set up trap for cleanup on SIGINT (Ctrl+C)
trap cleanup SIGINT

# Start dump.py in background
echo "🚀 Starting dump.py..."
python3 dump.py &
DUMP_PID=$!

# Wait a moment for the server to start
sleep 2

# Check if dump.py is running
if ps -p $DUMP_PID > /dev/null; then
    echo "✅ dump.py is running (PID: $DUMP_PID)"
else
    echo "❌ Failed to start dump.py"
    exit 1
fi

# Start monitor.py in background
echo "🔍 Starting monitor.py..."
python3 monitor.py &
MONITOR_PID=$!

# Wait a moment for monitor to start
sleep 2

# Check if monitor.py is running
if ps -p $MONITOR_PID > /dev/null; then
    echo "✅ monitor.py is running (PID: $MONITOR_PID)"
else
    echo "❌ Failed to start monitor.py"
    cleanup
fi

echo "📝 Both scripts are running. Press Ctrl+C to stop..."

# Wait for either process to exit
wait