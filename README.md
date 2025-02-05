# precisionFDA  GenAI Challenge
Entry for the Precision FDA Democratizing and Demystifying AI - GenAI Community Challenge.

The Challenge overview can be reviewed here:
[`precisionFDA Challenge Details`](https://precision.fda.gov/challenges/34/intro)

## Entry Details
A local first RAG implementation using open source solutions. The tool is a rag based local llm setup capable of accurately answering questions using the FDA provided data in the Cosmetic Guidance PDF.

## Technologies
Python based app using Langchain, Ollama, Chroma, and PyMuPDF. The default llm model is llama3.2, which is the small format version of Llama 3. With a model size of only 2.0 GB, it is capable of running on many platforms. Users can also choose from any other models they have in Ollama if they prefer.


## Install & run the current project

1. Install Python. See the official site for download and instructions:
[`Python`](https://www.python.org/downloads/)

2. Install Ollama on your local machine. Download from the official site for your platform:
[`Ollama Download Page`](https://ollama.com/download)

3. Pull the latest version of Llama3.2 and mxbai-embed
```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
```

4. Clone the repo
```bash
git clone https://github.com/dj0le/precisionFDA-GenAI-Challenge
```
5. Setup the Virtual Env
```bash
cd precisiionFDA-GenAI-Challenge
python -m venv .venv
source .venv/bin/activate
```
6. Install requirements
```bash
pip install -r requirements.txt
```
7. Start the api
```bash
python3 main.py
```

Now, your backend api should be running (http://localhost:8000/) and you can see all the endpoints available in swagger at (http://localhost:8000/docs)

If you prefer a command line approach, inside the CLi folder is the complete local rag implementation without fastapi etc. This has it's own README which will explain it further.

The deprecated version folder contains an initial implementation FastAPI implementation that did not perform robustly, and is only listed still as reference, it is otherwise unnecessary.


## Remaining Steps:

1. Improve rag implementation
2. Add user features and maybe multimodal model capability for images and graphs
3. UI implementation
4. PWA
