#!/bin/bash

echo "🚀 Starting full RCA pipeline..."

# Step 1: Create virtual environment if missing
if [ ! -d "venv2" ]; then
  echo "🧪 Creating virtual environment..."
  python3 -m venv venv2
fi

# Step 2: Activate virtual environment
source venv2/bin/activate

# Step 3: Upgrade pip and install dependencies
echo "📦 Installing dependencies..."
python3 -m pip install --upgrade pip
pip install -r requirements.txt
pip install langchain-openai faiss-cpu

# Step 4: Index the repo
echo "🔍 Running index.py to build FAISS DB..."
python3 index.py

# Step 5: Launch Flask app
echo "🌐 Launching RCA dashboard..."
nohup python3 app.py > flask.log 2>&1 &
echo $! > flask.pid

# Step 6: Health check
sleep 3
curl -s http://localhost:5004/fd_eks/ | grep "Application Name" > /dev/null
if [ $? -eq 0 ]; then
  echo "✅ Dashboard is live at http://localhost:5004/fd_eks/"
else
  echo "❌ Dashboard failed to launch. Check flask.log for details."
fi
