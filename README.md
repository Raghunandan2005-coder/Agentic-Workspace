## Agentic Project Workspace
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
