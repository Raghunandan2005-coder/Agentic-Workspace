# Agentic-Workspace
Multi-agent software development workspace using Google ADK, Agentic RAG, MCP, and persistent project memory.

Agentic Project Workspace is a multi-agent software development workspace designed to take a project requirement through a structured development workflow:
Requirement → Planning → Knowledge Retrieval → Implementation → Testing → Repair → Review → Persistent Project State

The system is built using Google ADK, Agentic RAG, MCP-based filesystem tools, automated testing, and persistent project memory.

**Current Status:** Active development and validation project. The Workspace has been validated end-to-end with two different project types: a TaskFlow CLI application and an Appointment Booking System end to end backend.

## What Problem Does It Solve?
When developing software with an AI agent, generating code is only one part of the development process.

A useful development system should be able to:
 - Understand project requirements
- Retrieve relevant project knowledge
- Break requirements into implementation tasks
- Delegate work to specialized agents
- Inspect and modify real project files
- Run automated tests
- Respond to test failures
- Request corrective implementation
- Retest the modified project
- Review the completed implementation
- Maintain project state across sessions

Agentic Project Workspace explores how these capabilities can be combined into a **Manager-orchestrated multi-agent development workflow**

## Architecture


                          User
                           │
                           ▼
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
                     Coder   Reviewer
                        │       │
                        └───┬───┘
                            ▼
                         Manager
                            │
                            ▼
     
             Persistent Project State


## Design Principle

Specialist agents perform and report. The Manager orchestrates and decides.
The Manager coordinates the development workflow while specialist agents remain responsible for their assigned capabilities

 ## Agents
Manager Agent :

The central orchestrator of the Workspace.
Responsibilities
•	Receive the project goal 

•	Coordinate specialist agents

•	Delegate implementation tasks 

•	Observe agent results 

•	Control correction loops

•	Manage workflow progression

•	Maintain project execution state

The Manager is responsible for orchestration rather than directly implementing project files

Planner Agent :

Responsible for understanding requirements and creating an implementation plan.
Responsibilities
•	Understand project requirements 

•	Retrieve relevant project knowledge through RAG 

•	Identify required implementation work 

•	Create an implementation plan 

•	Provide context to the Coder Agent 

The Planner does not directly modify project files

Coder Agent :

Responsible for project implementation.
Responsibilities

•	Inspect the assigned project

•	Create project files 

•	Modify existing files

•	Implement the Planner's plan

•	Use filesystem operations through MCP 

•	Report implementation changes

The Coder Agent does not directly manage persistent project memory

Testing Agent :

Responsible for automated validation.
Responsibilities

•	Execute the project's automated tests 

•	Report test results

•	Provide failure evidence

•	Validate fixes after implementation changes 

The Testing Agent uses a restricted test execution tool rather than unrestricted shell access.

Reviewer Agent:

Responsible for final technical review.
Responsibilities

•	Check implementation against requirements 

•	Inspect project structure

•	Review implementation quality

•	Consider test results

•	Identify remaining issues

•	Approve or reject the implementation

The Reviewer is designed as a read-only validation agent and does not modify project files.

## Project Knowledge RAG

Project Knowledge and Project Memory serve different purposes.
The Project Knowledge RAG represents what the project is supposed to do.
The RAG layer allows agents to retrieve relevant project requirements and documentation instead of passing the entire project documentation through every agent interaction.

## RAG Pipeline

 Project Requirements  -> Document Ingestion ->
    
Current Implementation
•	Python 
•	LangChain 
•	ChromaDB 
•	Ollama 
•	nomic-embed-text 
The RAG system is used to provide project-specific knowledge to the development workflow.

## Persistent Project Memory
Project Knowledge and Project Memory are intentionally separated.
Project Knowledge
Answers:
What should the project do?
Examples:
•	Requirements 
•	Specifications 
•	Project documentation 
Project Memory
Answers:
What has happened in the project?
The persistent project state tracks information such as:
•	Current task 
•	Workflow status 
•	Last completed task 
•	Next task 
•	Agent responsible for the latest update 
•	Validation state 
This separation allows the Workspace to distinguish between:

Project Knowledge

What should be built?

Project Memory

What has happened so far?

##  MCP Filesystem Integration

The Coder Agent interacts with real project files through a filesystem MCP layer.

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

The filesystem tool layer provides controlled operations such as:
•	Reading files 
•	Writing files 
•	Editing files 
•	Creating directories 
•	Listing directories 
•	Searching project files 
•	Moving files 
•	Inspecting file information 
MCP is used as the filesystem interaction layer instead of giving development agents unrestricted filesystem or shell access.


## Development Correction Loop

A key capability of the Workspace is responding to implementation and test failures

             Coder
               │
               ▼
         Testing Agent
               │	
        ┌──────┴──────┐
        │             │
       PASS          FAIL
        │             │
        ▼             ▼
    Reviewer       Manager
                      │
                      ▼
                    Coder
                      │
                      ▼
                 Testing Agent

The Workspace does not simply stop when a test fails.
Testing results can trigger another implementation cycle:
Test → Failure → Repair → Retest
This allows the system to validate whether corrections actually resolve the detected problem.


Project Isolation
The Workspace is designed to support multiple projects inside a shared project workspace.

projectworkspace/
│

│

    ├── TaskFlow_CLI/

    ├── taskflow_cli/
    |   └── tests

    ├── appointment-booking-system/
    ├── app/
    └── tests/

Agents are instructed to:
•	Identify the correct project directory 
•	Work only inside the assigned project 
•	Avoid modifying unrelated projects 
•	Reuse an existing project directory when continuing work 
•	Avoid placing project source files directly in the shared workspace root 
Project isolation is important when validating the Workspace across multiple software projects.

## End-to-End Validation

	
The Workspace has currently been validated using two different project types.

Test 1 — TaskFlow CLI
The first end-to-end validation project was a TaskFlow CLI application.

The Workspace was required to:

•	Understand the requirements

•	Plan the project 

•	Implement the application

•	Create and execute tests

•	Respond to test failures

•	Correct the implementation

•	Retest the project

•	Perform a final review 

Initial Result	

38 tests

34 passed

4 failed

The failures triggered a correction cycle.

Final Result

38 tests

38 passed

0 failed

The Reviewer subsequently inspected the implementation and test results and approved the completed workflow.

This demonstrated the basic:

          Plan
           ↓
          Build
            ↓
          Test
            ↓
           Fix
            ↓
          Retest
            ↓
          Review 




       
development loop.

Test 2 — Appointment Booking System Backend

The second end-to-end validation project was an Appointment Booking System.

The project was selected to test backend reasoning, validation, database constraints, automated testing, and correction loops.

Core Requirement

Prevent users from booking an already occupied appointment slot.

The Workspace was required to:

•	Understand the project requirements

•	Plan the implementation

•	Generate the project structure

•	Implement the backend

•	Create automated tests

•	Run the test suite

•	Respond to implementation/test failures

•	Repair the implementation

•	Rerun the tests

•	Perform a final technical review

Generated Project Capabilities

The resulting project included:

•	Patient registration

•	Doctor profiles

•	Appointment slots 

•	Appointment booking 

•	Duplicate-booking prevention

•	Appointment cancellation 

•	Appointment history

• Input validation 

•	Error handling 

•	SQLite persistence 

•	Automated tests 

Final Automated Test Result

13 tests	

13 passed

0 failed

## Runtime Verification

The critical duplicate-booking behavior was also verified against the running FastAPI application.

First appointment booking

        │
        ▼
     200 OK
        │
        ▼
Appointment created

The same appointment slot was then submitted again:

     Same slot booked again
           │
           ▼ 
        
       409 Conflict
           │
           ▼
    Slot is already booked.

Please choose another slot.

This provided runtime evidence that the generated application enforced the core booking constraint.

The Reviewer subsequently inspected the implementation and final test results.

## Current Validation Status

The Workspace has currently been validated against two project types:

Validation	Project Type	Final Result

Test 1	TaskFlow CLI	38/38 tests passed

Test 2	Appointment Booking System	13/13 tests passed

The two projects provide validation across different development scenarios:

TaskFlow CLI
    │
    └── CLI application + correction loop

Appointment Booking System
    │
    └── Backend application + database constraints + validation + correction loop

Additional project validations may be added as the Workspace evolves

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
        ├── appointment-booking-system/




## Technologies :

Technology            	Purpose

Python	               Core implementation

Google ADK	           Agent orchestration

Gemini                 LLM reasoning

Openrouter Models       LLM reasoning

LangChain	              RAG pipeline

ChromaDB                Vector storage

Ollama	                Local embeddings

nomic-embed-text	      Embedding model

MCP	Tool                integration

Filesystem MCP	         Project file operations

Pytest	                 Automated testing

Git / GitHub	           Source control



## Running the Workspace

From the agenticworkspace directory:

cd "E:\RAG\RAG Hands On\Agentic Workspace\agenticworkspace"
Start the ADK application:

adk run Manageragent

The exact workflow depends on the project requirement provided to the Workspace.

Current Limitations

This project is currently a learning and validation system, not a production autonomous software-development platform.

Current areas being explored include:

•	More diverse project validation

•	Agent communication and delegation quality 

•	Agent evaluation 

•	Cost and token monitoring 

•	Observability 

•	More robust failure recovery

•	Production deployment 

•	Larger project complexity

## Status: 
Completed learning and validation project. The workspace has been validated end-to-end on two different software projects, including automated testing, failure-driven correction, retesting, and final review.

The current validation demonstrates the development workflow on two project types, but does not establish that the system can reliably handle arbitrary software projects.










