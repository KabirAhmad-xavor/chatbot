<h2 align="left" id="setup">Project Setup Guide ⚙️</h2>

## ℹ️Installation Instructions

Follow these steps to install and set up the project on your system.

### 1. Install Dependencies

```sh
sudo apt update
sudo apt install -y software-properties-common
```

### 2. Add the deadsnakes PPA (For Ubuntu Users)

```sh
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
```

### 3. Install Python 3.10

```sh
sudo apt install python3.10 python3.10-venv python3.10-distutils
```

### 4. Verify Python Installation

```sh
python3.10 --version
```

### 5. Create a Virtual Environment (Recommended)

```sh
python3.10 -m venv chatbot
source chatbot/bin/activate
```

### 6. Install Required Packages

#### Azure Speech SDK

```sh
pip install azure-cognitiveservices-speech
```

#### Langchain / Langgraph

```sh
pip install requests langchain-core langchain-openai langgraph
```

#### Audio Handling

```sh
pip install sounddevice numpy elevenlabs pydub
sudo apt install ffmpeg  # Debian/Ubuntu
```

#### FastAPI

```sh
pip install fastapi uvicorn pandas
```





## 🚀Running the Setup Script

Run the following command before running the script.

```sh
sudo apt update
sudo apt install dos2unix
dos2unix setup_env.sh
```

Run the following commands to execute the setup script:

```sh
chmod +x setup_env.sh
./setup_env.sh
```

## Running the Project

### 1. Start the API Server

```sh
uvicorn APIs:app --port 8002 --reload
```

### 2. Run the Main File

```sh
python main.py
```

## 📝Notes

- Ensure that you **only use the setup script (`setup_env.sh`)** for installation.
- Always activate the virtual environment `Langgraph_chatbot` before running commands.

```sh
source Langgraph_chatbot/bin/activate
```
