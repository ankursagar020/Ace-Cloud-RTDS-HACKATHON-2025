# Ace-Cloud-RTDS-HACKATHON-2025

Developed for the Ace Cloud x RTDS Hackathon, this project explores Agentic AI—autonomous agents that can plan, reason, and act independently in dynamic environments. It focuses on intelligent decision-making with minimal human input, solving real-world problems through adaptive and goal-oriented behavior.
LINK(for frontend): https://cloud-scribe-ai-pilot.lovable.app/

Agentic AI for Cloud Operations
🧠 Overview
Agentic AI for Cloud Operations is an intelligent assistant built for managing OpenStack infrastructure using natural language instructions. Designed for cloud operators, it reduces the need to manually execute CLI commands or API calls by using a conversational interface powered by a language model. The system interprets user intent, validates it, seeks explicit confirmation, and securely executes the corresponding OpenStack API operations.

🎯 Project Goals
The application enables:
1. Parsing natural-language requests like "Create an S.4 VM named dev‑box."
2. Mapping intents to OpenStack APIs (Nova, Neutron, Cinder)
3. Asking for confirmation before resource modification (create, delete, resize)
4. Executing operations securely with TLS-encrypted API calls
5. Querying project usage or quota status
6. Logging user actions into a local cursor.db (SQLite), with future scalability toward PostgreSQL.

📂 Project Structure
agentic_openstack_app/
│
├── main.py                         # Entry point for the application
│
├── config/
│   └── settings.py                # Stores credentials, endpoint URLs, and constants
│
├── auth/
│   ├── auth_handler.py           # OpenStack Keystone authentication
│   └── access_control.py         # RBAC / access checks (role-based access)
│
├── llm/
│   ├── parser.py                 # Intent detection and entity extraction using LLM
│   └── validator.py              # Validates if the request is a supported CRUD action
│
├── services/
│   ├── compute_service.py        # Interacts with Nova for VM operations
│   ├── network_service.py        # Interacts with Neutron for network provisioning
│   ├── volume_service.py         # Interacts with Cinder for volume creation/deletion
│   └── usage_service.py          # Provides project usage metrics
│
├── agents/
│   └── dispatcher.py             # Decision-making layer that routes validated intent
│
└── utils/
    └── logger.py                 # Logging of all user intents and actions

✅ Functional Coverage
The application supports the following confirmed operations:

#	Scenario		Example Query					Result Behavior
FR‑1	VM Provisioning		“Create an S.4 VM named dev‑box.”		Confirms → Creates VM → Returns VM ID and IP
FR‑2	VM Resizing		“Resize dev‑box to flavor M.8.”			Confirms → Resizes → Returns status
FR‑3	VM Deletion		“Delete the VM dev‑box.”				Confirms → Deletes → Confirms deletion
FR‑4	Network Creation	“Create a private network called blue‑net.”	Confirms → Creates network and subnet → Returns info
FR‑5	Volume Operations	“Create a 100 GB volume named data‑disk.”	Confirms → Creates volume → Returns volume ID "Delete volume data‑disk" Confirms → Deletes volume
FR‑6	Usage Query		“What’s my project usage?”			Fetches and returns vCPU, RAM, GPU, volume usage summary

🔐 Security Considerations
1. All API communications occur over TLS-secured endpoints
2. Role-based access control is enforced through access_control.py
3. Confirmation prompts safeguard resource-modifying operations

🗄️ Logging and Database
Database Engine: Currently uses SQLite (cursor.db) for quick prototyping and local logging
Logged Information:
1. Timestamped user requests
2. Operation type and outcome
3. Resource identifiers involved
4. Future Plan: Transition to PostgreSQL for production scalability and multi-user support

⚙️ Authentication & API Access
Uses OpenStack Keystone for identity and token-based authentication
Credentials and endpoint URLs are stored securely in config/settings.py
Supported services:
1. Compute (Nova)
2. Network (Neutron)
3. Volume (Cinder)
4. Usage Metrics




