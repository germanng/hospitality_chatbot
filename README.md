# Hotelier Chatbot Assistant

Script to use ChatGPT on hotel internal data.

app.py - contains the code which runs the app in your browser

main.py - contains the code with the chatbot creation

constants.py - contains your OpenAI Key

data.txt - where the hotel internal data is placed

## Installation

```
pip install langchain openai chromadb tiktoken unstructured streamlit
```
Make sure that you create a virtual environment before working with the code.
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

