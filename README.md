# Hotelier Chatbot Assistant

Script to use ChatGPT on hotel internal data.

## Installation

```
pip install langchain openai chromadb tiktoken unstructured streamlit
```
constants.py contains your OpenAI Key

The hotel data is placed to the following file: `data.txt`.

## Example usage
First you need to run the app, and it will open in your browser:
```
streamlit run app.py
```
Test it using e.g. the following prompts:
```
We have a booking request for an apartment with mountain view from 2nd July for 6 nights. How much would it cost?

or

What do our guests want today?
```

