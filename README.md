# 📚 Research Assistant Multi-Agent System

A multi-agent AI research system that transforms a user query into a structured, validated research report using:

- OpenAI Agents (manager + specialized roles)
- Olostep API (external knowledge / research grounding)
- Multi-agent reasoning pipeline (Research → Analysis → Judge)
- Instruction-driven agent behavior design

---

# 🚀 What this project does

This system takes a user query and produces a **well-structured research report** by coordinating multiple AI agents.

### Workflow

User Query  
→ Manager Agent (Orchestrator)  
→ Olostep API (external knowledge retrieval)  
→ Research Agent (fact collection & summarization)  
→ Analysis Agent (reasoning & insights)  
→ Judge Agent (validation & quality check)  
→ Final Report

---

# 🧠 Architecture

User Query
    ↓
Manager Agent (Orchestrator)
    ↓
Olostep API (Knowledge Retrieval)
    ↓
Research Agent (Fact Gathering)
    ↓
Analysis Agent (Reasoning & Insights)
    ↓
Judge Agent (Validation & Quality Check)
    ↓
Final Report

---

# 🏗️ System Design

┌──────────────────────────────┐
│        assistant.py          │  ← Entry Point
└──────────────┬───────────────┘
               │
               ↓
┌──────────────────────────────┐
│      Manager Agent           │
│   (Orchestration Layer)      │
└──────────────┬───────────────┘
               │
     ┌─────────┼──────────┐
     ↓         ↓          ↓
┌────────┐ ┌────────┐ ┌────────┐
│Research│ │Analysis│ │ Judge  │
│ Agent  │ │ Agent  │ │ Agent  │
└────┬───┘ └────┬───┘ └────┬───┘
     │          │           │
     └────┬─────┴────┬─────┘
          ↓           ↓
     ┌────────────────────┐
     │   Olostep API      │
     │ (External RAG Layer)│
     └────────────────────┘
               │
               ↓
     ┌────────────────────┐
     │ Final Report       │
     └────────────────────┘

---

# 🤖 Agent Roles

## 🧭 Manager Agent
- Entry point of reasoning
- Breaks down user query into steps
- Decides when to use tools (Olostep API)
- Delegates tasks to sub-agents

---

## 🔍 Research Agent
- Collects factual information
- Summarizes external knowledge
- Ensures grounded responses

---

## 🧠 Analysis Agent
- Performs reasoning over collected data
- Extracts insights and patterns
- Converts raw data into structured understanding

---

## ⚖️ Judge Agent
- Evaluates response quality
- Detects hallucinations or inconsistencies
- Ensures final output reliability

---

# 🌐 External Dependency: Olostep API

This system uses Olostep API as its external knowledge layer.

Instead of vector DB-based RAG, it:
- Sends query to Olostep
- Receives contextual information
- Feeds results into agent pipeline

---

# 📁 Project Structure

src/
 └── app/
     ├── research/
     │    └── assistant.py        # 🚀 Entry point / orchestration
     │
     ├── agent/
     │    └── instruction/
     │         └── instructions.py # 🧠 Agent prompts & behaviors
     │
     ├── tools/
     │    └── olostep_client.py    # 🌐 API wrapper (assumed)
     │
     └── ...
     
---

# ⚙️ Setup

## 1. Clone repository

git clone https://github.com/Anks533/research_assistant_multi_agent.git
cd research_assistant_multi_agent

---

## 2. Create virtual environment

python -m venv venv

Mac/Linux:
source venv/bin/activate

Windows:
venv\Scripts\activate

---

## 3. Install dependencies

If using pyproject.toml:

pip install .

OR:

pip install -r requirements.txt

---

## 4. Environment variables

Create a `.env` file:

OPENAI_API_KEY=your_openai_key
OLOSTEP_API_KEY=your_olostep_key

---

# ▶️ Run the project

python src/app/research/assistant.py

OR:

python -m src.app.research.assistant

---

# 📤 Example Output

Input:
"What are the risks and benefits of AI in healthcare?"

Output:
- Executive summary
- Key findings
- Structured analysis
- Verified insights (Judge Agent validated)

---

# 🔥 Key Strengths

- Modular multi-agent architecture
- Clear separation of responsibilities
- External knowledge grounding via API
- Built-in validation layer (Judge Agent)
- Highly extensible design

---

# ⚠️ Limitations

- No persistent memory system
- Depends on external Olostep API
- Orchestration is LLM-driven (non-deterministic)
- Limited observability per agent step

---

# 🚀 Future Improvements

- Add DAG-based orchestration (LangGraph style)
- Add memory layer (short + long term)
- Add tracing per agent execution
- Add retry loop based on Judge feedback
- Add fallback RAG system

---

# 🧠 Summary

A multi-agent AI research system that uses OpenAI + Olostep API to generate validated, structured research reports through specialized agents.
