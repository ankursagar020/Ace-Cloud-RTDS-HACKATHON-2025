# Ace-Cloud-RTDS-HACKATHON-2025
Developed for the Ace Cloud x RTDS Hackathon, this project explores Agentic AI—autonomous agents that can plan, reason, and act independently in dynamic environments. It focuses on intelligent decision-making with minimal human input, solving real-world problems through adaptive and goal-oriented behavior.

Background / Context
Cloud operators routinely perform tasks such as creating, resizing, or deleting VMs, volumes, and networks. Today this requires translating intent into a series of CLI commands or API calls. AceCloud challenges participants to build an agentic AI that accepts natural‑language instructions, plans the required OpenStack API calls, and executes them after a confirmation step—returning results conversationally.

Parse natural‑language requests (questions or instructions) using an LLM or intent–entity model.
Map each intent to the corresponding CRUD actions across OpenStack Compute (Nova), Network (Neutron), and Block‑Storage (Cinder) APIs.
Ask for explicit confirmation (Yes/No) before executing any create, resize, or delete action, then report the outcome.
Provide informational answers such as project usage or quota status on demand.
The solution should be secure through TLS encryption over APIs.
A Database must be maintained of user requests

