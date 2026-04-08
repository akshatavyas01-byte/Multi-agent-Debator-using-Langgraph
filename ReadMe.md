# AI MULTIAGENT DEBATOR

## 1. Overview
``This project implements a multi-agent system that simulates a debate on a given topic and determines a winner.``

When a user submits a topic, the pro_agent and con_agent engage in a structured debate for multiple rounds. After the debate, a fact-checker agent evaluates the integrity of the arguments presented. The verified results are then passed to a judge agent, which decides the winner based on factual accuracy and reasoning.

## 2. Problem Statement
### In the current information-rich environment, it is difficult to objectively evaluate a topic and verify its accuracy. Conflicting yet valid viewpoints make it challenging to determine which side is ultimately correct.

This project introduces a multi-agent workflow consisting of a pro_agent, con_agent, fact-checker agent, and judge agent to simulate balanced debates, validate arguments, and provide a reasoned final decision.

## 3. Solution Approach 
#### This project uses 4 LLM-powered agents to debate, validate argument and give a reasoned final winner.
#### Given a topic, the workflow:
 **Pro_agent:**
    Generates a strong opening statement in favour of the topic.
**Con_agent:**
    Generates a counter argument opposing the pro_statement 
**Debate rounds**:
    Steps 1 and 2 are repeated for multiple rounds to stimulate multiple rounds of structured debate.
**Fact-checker agent:**
    Uses Wikipedia Retrieved content to verify the accuracy of the arguments.Returns arguments with their verified results.
**Judge agent:**
    Determines the winner by envaluating the results of fact checker agent. Returns a winner and factual reason.

**Note**: Due to token constraints, fact-checking is performed on limited context, which may impact verification accuracy.

## 4. Key Features 
    - Submit debate Topic through interface.
    - Recieve structured arguments.
    - Recieve reasoned winner of the debate.
    - Session based history of topics and winner.

## 5. System Architecture
    - Frontend - Streamit
    - LLM - Hugging Face & GROQ
    - LLM-Orchestration - Langgraph & Langchain
    - Storage - Session state 

## 6. Tech Stack

**Language:** Python  
**Frontend:** Streamlit  
**LLM Orchestration:** Langgraph & LangChain  
**Model Provider:** Hugging Face & Groq
**Environment Management:** python-dotenv  

## 7. How It Works(Execution Flow)
    1. User Submission
    - The user enters a topic in the interface and clicks Submit.

    2. Pro_agent
    - The llm powered agent generates a strong opening argument in favour of the topic.

    3. Con_agent
    - The llm powered agent generates a counter argument opposing the pro argument.

    4. Debate Round
    - The pro and con agents alternately generate arguments for a fixed number of rounds, simulating a structured debate.

    5. Fact-checker agent
    - The agent retrieves relevent informat form Wikipedia and verifies the factual accuracy of the arguments. It classsifies the arguments into `True`, `False` or `Needs Verification`.

    6. Judge Agent
    -  The judge evaluates the results of the fact-checker agent and determines the winner based on the factual accuracy and reasoning ability. 

    7. Result Display
    - The system displays full debate (Pro vs Con) argument along with the final verdict in the user interface.

## 8. Example Input & Output
## Render Deployed 

## 9. Installation & Setup 
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

## 10. Usage 
### 1. Run the streamlit frontend:
```python
streamlit run main/init.py
```
### 3. Open the browser and:
    - Enter a topic
    - Click Submit
    - View streamed PRO vs CON arguments along with the Verdict.

## 11. Project Structure

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

## 12. Limitations
- Limited accuracy of the fact-checker agent due to token constraints.
- The final verdict may be less reliable as it is based on limited fact-checking context.
- No user authentication system is implemented.
- No per-user session data storage.
- No caching mechanism for repeated topics.

## 13. Future Improvements
- Optimize or increase effective context usage for the fact-checker agent.
- Improve the accuracy and robustness of fact verification.
- Integrate multiple data sources for more reliable fact-checking.
- Implement a user authentication system.
- Add per-user session data storage.
- Introduce caching for repeated queries to improve performance.

## 14. License
This project is licensed under the MIT License.

## 15. Author
**Akshata Vyas**  
GitHub: [akshatavyas01-byte](https://github.com/akshatavyas01-byte)

        