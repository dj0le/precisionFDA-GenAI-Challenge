# precisionFDA  GenAI Challenge
Entry for the Precision FDA Democratizing and Demystifying AI - GenAI Community Challenge.

The Challenge overview can be reviewed here:
[`precisionFDA Challenge Details`](https://precision.fda.gov/challenges/34/intro)

### Entry Details
A local first RAG implementation using open source solutions. The tool is a rag based local llm setup capable of accurately answering questions using the FDA provided data in the Cosmetic Guidance PDF.

### Technologies
Python based app using Langchain, Ollama, Chroma, and PyMuPDF. The default llm model is llama3.2, which is the small format version of Llama 3. With a model size of only 2.0 GB, it is capable of running on many platforms. Users can also choose from any other models they have in Ollama if they prefer.


## Getting Started

### Prerequisites
- Python 3.8 or higher ([`Python`](https://www.python.org/downloads/))
- Node.js and npm
- Bash shell (comes with macOS and Linux, use Git Bash on Windows)
- Ollama ([`Ollama Download Page`](https://ollama.com/download))
- At least these 2 models installed in Ollama:
-- llama3.2
-- mxbai-embed-large
```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
```

### Installation
1. Clone the repository
```bash
git clone https://github.com/dj0le/precisionFDA-GenAI-Challenge
cd precisionFDA-GenAI-Challenge
```

2. Install backend dependencies
```bash
cd api
pip install -r requirements.txt
cd ..
```

3. Install frontend dependencies
```bash
cd frontend
npm install
cd ..
```

## Running the Application
You can start both the frontend and backend servers using start.sh or start.bat

### Linux and Mac
```bash
./start.sh
```
### Windows
You can start both the frontend and backend servers with:
```bash
start.bat
```

This will start:
- Backend API at http://localhost:8000
- Frontend development server at http://localhost:5173

You can also run each part separately:
- Backend: `cd api && uvicorn main:app --reload`
- Frontend: `cd frontend && npm run dev`


## Command line only version

There is an additional version included, which does not use the FastAPI backend, and instead runs in the terminal. If you prefer this command line approach, inside the CLi folder is the complete local rag implementation without fastapi etc. This has it's own README which will explain it further.
