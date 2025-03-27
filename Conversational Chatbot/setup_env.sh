#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

echo "----------- Updating system packages -----------"
sudo apt update
sudo apt install -y software-properties-common

echo "----------- Adding deadsnakes PPA -----------"
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update

echo "----------- Installing Python 3.10 and dependencies -----------"
if ! command -v python3.10 &> /dev/null; then
    sudo apt install -y python3.10 python3.10-venv python3.10-distutils
else
    echo "✅ Python 3.10 is already installed."
fi

echo "----------- Checking Python version -----------"
python3.10 --version

echo "----------- Creating Python virtual environment -----------"
if [ ! -d "Langgraph_chatbot" ]; then
    python3.10 -m venv Langgraph_chatbot
    echo "✅ Virtual environment 'Langgraph_chatbot' created."
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo ""
    echo "❌ Virtual environment is NOT activated."
    echo "👉 Please run the following command and then re-run this script:"
    echo "   source Langgraph_chatbot/bin/activate"
    echo ""
    exit 1
else
    echo "✅ Virtual environment is activated."
fi

echo "----------- Upgrading pip -----------"
pip install --upgrade pip

echo "----------- Installing system dependencies -----------"
sudo apt install -y ffmpeg

echo "----------- Installing Azure Cognitive Services Speech SDK -----------"
pip install azure-cognitiveservices-speech

echo "----------- Installing Langchain and Langgraph -----------"
pip install requests langchain-core langchain-openai langgraph

echo "----------- Installing Audio Handling Libraries -----------"
pip install sounddevice numpy elevenlabs pydub

echo "----------- Installing FastAPI and supporting tools -----------"
pip install fastapi uvicorn pandas
pip install python-dotenv

echo ""
echo "----------- ✅ Setup Complete! -----------"
echo "🟢 To activate your environment in the future, run:"
echo "    source Langgraph_chatbot/bin/activate"
