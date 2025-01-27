# precisionFDA  GenAI Challenge
Entry for the Precision FDA Democratizing and Demystifying AI - GenAI Community Challenge.

The Challenge overview can be reviewed here:
[`precisionFDA Challenge Details`](https://precision.fda.gov/challenges/34/intro)

## Entry Details
A local first RAG implementation using open source solutions. The tool is a rag based local llm setup capable of accurately answering questions using the FDA provided data in the Cosmetic Guidance PDF.

## Technologies
Cosmeticky is a python based app and uses Langchain, Ollama, Chroma, and PyMuPDF. The llm model is llama3.2, which is the small format version of Llama 3. With a model size of only 2.0 GB, it is capable of running on many platforms.


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
python -m venv .pvenv
source .pvenv/bin/activate
```
6. Install requirements
```bash
pip install -r requirements.txt
```

Now you should be able to run the various py scripts individually until I finish the api / ui / full implementation of the project.

If in doubt, choose 'cosmeticky.py'
```bash
python3 cosmeticky.py
```

## Remaining Steps:

1. Finish rag implementation
2. FastAPI implementation
3. UI implementation
4. Local first refactoring
