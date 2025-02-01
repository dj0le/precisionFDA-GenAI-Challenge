


# precisionFDA  GenAI Challenge
Entry for the Precision FDA Democratizing and Demystifying AI - GenAI Community Challenge.

The Challenge overview can be reviewed here:
[`precisionFDA Challenge Details`](https://precision.fda.gov/challenges/34/intro)

This is the command line version of the app that directly accesses the llm and vectordb

Python app using Langchain, Ollama, Chroma, and PyMuPDF. The default llm model is llama3.2, which is the small format version of Llama 3. With a model size of only 2.0 GB, it is capable of running on many platforms. Users can also choose from any other models they have in Ollama if they prefer.

## USAGE

1. In the cli/main.py file, you can change the variables for the documents or test-questions if needed (defaults are the actual challenge set so should be fine)
2. More likely, you will want to change the MODEL variable. It can be any chat trained model that you download from Ollama.
3. To see your available models, in the terminal, run "Ollama list".
4. Change the model variable to the entire model name, but strip the ":latest" or any other tag at the end. So "llama3.2:latest" would just be 'llama3.2'
4. Save and run

## TEST RESULTS

1. Running the test will produce a file 'llm_output.txt' in the base cli folder
2. It will overwrite everytime you run the program if you don't rename or move it
3. It's currently outputting to text files
4. In the cli/test-results folder, there are a number of model runs that I recorded. The results are very interesting in a number of ways.


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
7. Navigate into the 'cli' directory, then:
```bash
python3 main.py
```
