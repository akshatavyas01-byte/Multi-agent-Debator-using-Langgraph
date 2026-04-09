# Multi-Agent AI Debate System (LangGraph)

An AI-powered multi-agent system where specialized agents (Pro, Con, Fact-Checker, and Judge) collaborate to simulate structured debates, verify arguments, and generate a reasoned final verdict.

## Live Demo
**Try it here:**[![Live Demo](https://img.shields.io/badge/Live-Demo-green)](https://multi-agent-debator-using-langgraph-1.onrender.com/)
**Watch demo:** [![Watch Demo](images\streaming.png)](https://youtu.be/HLJKZpAW1xg)


## Why this project
In an information-rich environment, evaluating topics objectively is challenging due to conflicting viewpoints and potential misinformation.

This project addresses that by:
- introducing multiple AI agents with opposing perspectives  
- validating arguments using fact-checking  
- producing a balanced and reasoned final verdict
  
## Architecture
![Architecture diagram](images\Multi-agent architecture.drawio.png)

The system is built using multi-agent graph where each agent has s specific role:

        - Pro Agent-> Generates supporting arguments
        - Con Agent-> Generates opposing arguments
        - Fact-Checker Agent->  Verifies arguments using retrieved knowledge
        - Judge Agent-> Evaluates and decides the winner
        
**Note**: Due to token constraints, fact-checking is performed on limited context, which may impact verification accuracy.

## Key Highlights 
    - Multi-agent architecture with role-based reasoning  
    - Fact-checking using external knowledge retrieval  
    - Structured debate simulation with multiple rounds  
    - Final verdict based on factual validation  

## Tech Stack

- **Language:** Python  
- **Frontend:** Streamlit  
- **LLM Orchestration:** LangGraph, LangChain  
- **Model Providers:** Hugging Face, Groq  
- **State Management:** Session-based memory  

## Example Demo 
### 1.Video Demo
[![Watch Demo](images\streaming.png)](https://youtu.be/HLJKZpAW1xg)

### 2. Streamlit UI:
![Streamlit UI](images\user_interface.png)

### 3. Topic Input:
![Debate topic submitted](images\user_requuest.png)

### 3. Debate Output
![Streamed Result image 1](images\result1.png)
![Streamed Result image 2](images\result2.png)
![Streamed Result image 3](images\result3.png)

## Installation & Setup 
### 1. Clone the Repository:
```python
git clone https://github.com/your-username/risk-analyser.git
cd risk-analyser
```
### 2. Create Virtual Environment
```python
python -m venv .venv
```
### Activate it:
Windows vscode terminal:
```python
.venv\Scripts\Activate.ps1
```
### 3. Install Dependencies
```python
pip install -r requirements.txt
```
### 4. Add Environment Variables
Create a .env file and add:
```python
hf_api=your_api_key_here
groq_api=your_api_key_here
```

## Usage 
### 1. Run the streamlit frontend:
```python
streamlit run main/init.py
```
### 3. Open the browser and:
    - Enter a topic
    - Click Submit
    - View streamed PRO vs CON arguments along with the Verdict.

## Project Structure

     project/
            |── main/
            |   |── state.py
            |   |── init.py
            |   |── nodes.py
            |   |── graph.py
            |
            |── images/
            |
            |
            |── .env
            |
            |── requirements.txt
            |
            └── ReadMe.md

## Limitations
- Limited accuracy of the fact-checker agent due to token constraints.
- The final verdict may be less reliable as it is based on limited fact-checking context.
- No user authentication system is implemented.
- No per-user session data storage.
- No caching mechanism for repeated topics.

## Future Improvements
- Optimize or increase effective context usage for the fact-checker agent.
- Improve the accuracy and robustness of fact verification.
- Integrate multiple data sources for more reliable fact-checking.
- Implement a user authentication system.
- Add per-user session data storage.
- Introduce caching for repeated queries to improve performance.

## License
This project is licensed under the MIT License.

## Author
**Akshata Vyas**  
GitHub: [akshatavyas01-byte](https://github.com/akshatavyas01-byte)

        
