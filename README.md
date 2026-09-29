## AGENTC WORKSPACE

Multi-Agent Development System using Google ADK, Agentic RAG, MCP, and Persistent Project Memory.

Agentic Project Workspace is a multi-agent development workspace designed to take a software project requirement, retrieve relevant project knowledge, plan implementation, modify project files, run tests, review the implementation, and maintain persistent project state across sessions.

The system is built using Google ADK, RAG, MCP-based filesystem tools, and persistent project memory.

Current status: Active learning and validation project. The system has been validated with a TaskFlow CLI project and Appointment Booking system backent is being tested and completed.

What Problem Does It Solve ?

When developing a software project with an AI agent, simply generating code is not enough.
A useful development system needs to:

•	Understand project requirements

•	Retrieve relevant project knowledge

•	Break the task into manageable steps

•	Delegate work to specialized agents

•	Modify real project files

•	Run automated tests

•	React to test failures

•	Request fixes and retesting

•	Review the completed implementation

•	Preserve project state across sessions


This project explores how these capabilities can be combined into a single Manager-orchestrated multi-agent workflow.

## Architecture

                     User
                      │
                      
               ┌─────────────┐
               │   Manager   │
               │    Agent    │
               └──────┬──────┘
                      │
               ┌─────────────┐
               │   Planner   │
               │    Agent    │
               └──────┬──────┘
                      │
              Project Knowledge
                    RAG	
                      │
                      ▼

               ┌─────────────┐
               │    Coder    │
               │    Agent    │
               └──────┬──────┘
                      │
                MCP Filesystem
                      │
                      ▼
             Project Workspace
                      │
                      ▼
               ┌─────────────┐
               │   Testing   │
               │    Agent    │
               └──────┬──────┘
                      │
                PASS / FAIL
                  │       │
                FAIL     PASS
                  │       │
                  ▼       ▼
               Coder    Reviewer
                  │       │
                  └───┬───┘
                      ▼	
                  Manager
                      │
                      ▼
             Persistent Memory


The Manager Agent is responsible for orchestration and decision-making.
Specialist agents perform their assigned work and report the result back to the Manager


##  Agents

Manager Agent

The central orchestrator.

Responsibilities:

• Receive the project goal

•	Decide which specialist should act

•	Delegate tasks

•	Observe specialist results

•	Decide whether another action is required

•	Control correction loops

•	Commit validated project state to persistent memory

Planner Agent

Responsible for planning the implementation.

Responsibilities:

•	Understand the project requirement

•	Retrieve relevant information from Project Knowledge RAG

•	Create an implementation plan

•	Identify project structure and required work

The Planner does not directly modify project files.


Coder Agent

Responsible for implementation.

Responsibilities:	

•	Inspect the assigned project

•	Create or modify project files

•	Follow the Planner's implementation plan

•	Use filesystem tools through MCP

•	Report completed changes

The Coder does not directly update persistent project memory.

Testing Agent:

Responsible for validation.

Responsibilities:

•	Run the project's automated tests

•	Report test results

•	Provide failure evidence when tests fail

The Testing Agent uses a restricted test execution tool rather than unrestricted shell access

Reviewer Agent:

Responsible for final technical review.

Responsibilities:

•	Check requirement alignment

•	Inspect implementation quality

•	Review project structure

•	Consider test results

•	Approve or reject the implementation

The Reviewer is read-only and does not modify project files or persistent memory


##  Project Knowledge RAG

Project requirements and supporting documentation are stored separately from the actual project source code.

The RAG layer allows agents to retrieve relevant project knowledge instead of passing the entire documentation context through
every agent interaction.


Current RAG pipeline

     Project Requirements
            │
            ▼
      Document Ingestion
            │	
            ▼
         Chunking
            │
            ▼
        Ollama Embeddings
            │
            ▼
        ChromaDB
            │
            ▼
      Similarity Retrieval
            │
            ▼	
     Planner / Agents

Current implementation uses:

•	Python

•	LangChain

•	ChromaDB

•	Ollama

•	nomic-embed-text

The Workspace's RAG represents what the project should contain or accomplish.

Persistent Project Memory :

Project Knowledge and Project Memory serve different purposes

Project Knowledge

Answers:
What should the project do ?

Examples:	

•	Requirements

•	Specifications

•	Project documentation

Project Memory

Answers:

What has happened in the project?

Current persistent state includes information such as:

•	Current task

•	Workflow status

•	Last completed task

•	Next task

•	Agent responsible for the latest update

•	Validation state

This separation allows the system to distinguish between requirements and execution history.



## MCP Filesystem Integration

The architecture is:

  Agent
    │
    ▼
Google ADK / MCP Client
    │
    ▼
Filesystem MCP Server
    │
    ▼
  Project Files



The filesystem MCP server provides operations such as:

•	Read files

•	Write files

•	Edit files

•	Create directories

•	List directories

•	Search files

•	Move files

•	Inspect file information


The MCP server is intentionally used as the filesystem interaction layer rather than giving the agents unrestricted filesystem
or shell access


## Correction Loop

One of the important capabilities of the Workspace is responding to test failures.

Example:

         Coder
          │	
          ▼
         Testing Agent
             │
             ├── PASS ──────► Reviewer
             │
             └── FAIL
                  │
                  ▼
                Manager
                  │
                  ▼
                 Coder
                  │
                  ▼
             Testing Agent

The Manager does not blindly continue after a failure.
 
It uses the testing evidence to decide whether another correction cycle is required.

## Project Isolation
The Workspace supports multiple projects inside a shared project workspace.

          projectworkspace/
          │
          ├── TaskFlow_CLI/
          │   ├── taskflow_cli/
          │   └── tests/
          ├── Future_Project/
          │   └── ...

Each project receives its own dedicated directory.

Agents are instructed to:

•	Identify the correct project directory

•	Work only inside that project

•	Avoid modifying other projects

•	Reuse an existing project directory when continuing work

•	Never place project source files directly in the shared workspace root

This isolation is important when validating the system across multiple projects

## Current Validation

Test 1 — TaskFlow CLI

The first end-to-end validation project was a TaskFlow CLI application.

The Workspace was required to:

•	Understand the requirements

•	Plan the project

•	Build the application

•	Create tests

•	Run the tests

•	Respond to failures

•	Correct the implementation

•	Retest

•	Perform a final review


Initial test result:

38 tests

34 passed

4 failed

After the correction loop:

38 tests

38 passed

The Reviewer subsequently returned an approval after checking the implementation and test results.

This demonstrated the basic:

Plan → Build → Test → Fix → Retest → Review

workflow.

## Test 2 — Expense Tracker	

The second validation project is an interactive Expense Tracker.

The requirements include:

•	Add expenses

•	Edit expenses

•	Delete expenses

•	Search expenses

•	Filter expenses

•	Calculate total spending

•	Category-wise summaries

•	Persistent storage

•	Interactive UI

•	Automated testing

The storage technology is intentionally not prescribed in the requirements.

The Planner should determine an appropriate implementation approach based on the project requirements and scope.

This test is intended to determine whether the Workspace can generalize from a CLI project to an interactive application.


Project Structure

    Agentic Workspace/

    │

    └── agenticworkspace/

    │
    ├── Manageragent/
    │   ├── __init__.py
    │   ├── agent.py
    │   ├── agents.py
    │   ├── memory_tools.py
    │   ├── mcp_filesystem.py
    │   └── test_tools.py
    │
    ├── Knowledgebase/
    │   ├── __init__.py
    │   ├── ingestion.py
    │   ├── retrieval.py
    │   └── chroma_db/
    │
    ├── projectmemory/
    │   └── task_state.json
    │
    └── projectworkspace/
        ├── TaskFlow_CLI/



Technology    	        Purpose :

Python	                Core implementation

Google ADK	            Agent orchestration

Gemini	                LLM reasoning

LangChain             	RAG pipeline

ChromaDB         	      Vector storage

Ollama	                Local embeddings

nomic-embed-text	      Embedding model

MCP	Tool                integration

Filesystem MCP     	    Project file operations

Pytest	                Automated testing

GitHub                	Source control



## Current Limitations

This project is currently a learning and validation system rather than a production autonomous software-development platform.

Current areas still being explored include:

•	More diverse end-to-end project validations

•	Agent communication and delegation quality

•	Agent evaluation

•	Cost and token monitoring

•	Observability

•	More robust failure recovery

•	Production deployment

•	Larger project complexity

The Workspace is intentionally being validated on multiple project types before making stronger claims about its generality.

## Project Status:

Status: Active Development & Validation	

The Workspace has completed its first end-to-end project validation with TaskFlow CLI and is being tested and Appointment

booking system against additional project types to validate its generality and reliability.
