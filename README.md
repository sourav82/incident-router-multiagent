# AI-Powered Incident Routing & Troubleshooting (ServiceNow + Azure Functions)

This project implements an AI-driven incident triaging and troubleshooting system integrated with ServiceNow and Azure Functions.

The system automatically:

- Receives incident events from ServiceNow
- Classifies incidents using AI
- Searches historical Knowledge Base (KB) articles using semantic search
- Updates incidents with recommended solutions
- Assigns incidents to the appropriate team
- Notifies stakeholders if no KB match is found

# Architecture Overview

<img width="155" height="201" alt="image" src="https://github.com/user-attachments/assets/a6028938-38e7-4f7f-a452-03849aed5c60" />


# ServiceNow Configuration

The following configurations must be completed in ServiceNow before deploying the application.
# Assignment Groups

Create the following assignment groups in ServiceNow:

| Assignment Group |
| ---------------- |
| Level-1          |
| Network-L2       |
| MBS-L2           |
| IBS-L2           |
| Algo             |

Each assignment group should contain **multiple members** so the system can randomly assign incidents to an available engineer.

# Level-1 Assignment Rule

A **ServiceNow Business Rule** automatically assigns all newly created incidents to the Level-1 queue.

Example Logic:

When Incident Created
→ Assign to "Level-1" Assignment Group

# Webhook Configuration

Once an incident is assigned to **Level-1**, ServiceNow triggers a **Webhook** to the Azure Function App.

# Webhook Payload
The webhook sends the following incident information:

{
  "number": "INC0012345",
  "sys_id": "abc123xyz",
  "description": "Customer unable to connect to VPN"
}

# Azure Function Application

The webhook is received by an Azure Function which triggers the AI triaging pipeline.

Responsibilities:

- Receive ServiceNow webhook payload
- Start LangGraph workflow
- Run AI agents
- Update incident in ServiceNow

# AI Agent Workflow
The application uses LangGraph to orchestrate multiple AI agents.

Workflow:

Router → Classifier → KB Search → Troubleshoot → Notification

# Router Agent

The router agent determines whether the incident qualifies for Level-1 AI triaging.

If the incident is not relevant, the workflow exits.

# Classifier Agent

The classifier agent analyzes the incident description and determines the most appropriate assignment group.

Example classifications:

| Description                 | Assignment Group |
| --------------------------- | ---------------- |
| Network connectivity issues | Network-L2       |
| Major Business Services     | MBS-L2           |
| Important Business Services | IBS-L2           |
| Trading system problems     | Algo             |

The identified assignment group will later be used to update the incident.

# Knowledge Base (KB) Semantic Search

The KB agent performs semantic similarity search using a vector database.

Process:

1. Incident description converted into embeddings
2. Vector similarity search performed
3. Top matching KB articles retrieved

Technology used:

Azure OpenAI Embeddings
Chroma Vector Database

Example result:

KB Article: VPN Connection Failure
Resolution: Restart VPN client and re-authenticate
Similarity Score: 0.89

# Vector Database

The system uses Chroma Vector Database.

**Vector Store Location**
/tmp/vectordb

The vector store is built from a SQLite KB database containing historical incidents and their resolutions.

Process:

SQLite KB
   ↓
Generate embeddings
   ↓
Store in Chroma Vector DB
   ↓
Semantic search during incidents

# Troubleshooting Engine

The troubleshooting agent updates the incident in ServiceNow with:

- Correct assignment group
- Recommended KB solutions
- Random assignment to group member

Example update:

Assignment Group: Network-L2
Assigned To: John Doe

Work Notes:
Found matching KB articles:

1. VPN Connection Failure
2. Network Authentication Timeout


# Notification Engine

If no KB article is found, the system assumes this incident may represent a new or unknown problem.

In such cases:

- Email notifications are sent to stakeholders
- A War Room meeting invite is triggered

Purpose:

Identify new issue patterns
Coordinate cross-team troubleshooting
Capture knowledge for future incidents

# Repository Structure

<img width="197" height="241" alt="image" src="https://github.com/user-attachments/assets/3645b9de-b81b-4bd1-9dd2-3b9e3b22d830" />

Deployment

The application is deployed as an Azure Function App.

Trigger type:

> HTTP Trigger (Webhook)

# Deployment

The application is deployed as an Azure Function App.

Trigger type:

> HTTP Trigger (Webhook)

When ServiceNow sends the webhook, the function processes the incident automatically.

# Security Considerations

Sensitive information such as:

- Azure OpenAI API Keys
- ServiceNow credentials
- Storage keys

must be stored in:

> Azure Function App → Application Settings

# Future Enhancements

Potential improvements:

- Incident priority prediction
- Auto-resolution for known issues
- Automatic KB creation for new incidents
- Dashboard for incident analytics
- Teams / Slack war room automation

# Summary

This system automates Level-1 incident triaging using AI.

Capabilities include:

- AI-based incident classification
- Semantic KB search
- Automatic ServiceNow updates
- Intelligent routing to Level-2 teams
- War-room escalation for unknown issues

This significantly reduces manual triage effort and accelerates incident resolution.
