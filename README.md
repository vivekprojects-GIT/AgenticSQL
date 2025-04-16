# AgenticSQL: An Agent-Based Framework for Natural Language to SQL Generation
AgenticSQL is a multi-agent framework that converts natural language to SQL using specialized agents for NER, schema mapping, prompt building, and validation. It supports any database via RAG and MCP, enabling scalable, explainable, and schema-aware query generation without fine-tuning.


⸻


AgenticSQL is a novel, modular, and explainable framework that leverages autonomous agents to convert natural language queries into SQL across dynamic, multi-tenant database systems. Unlike traditional NL2SQL approaches that rely on fine-tuned monolithic models or brittle prompt engineering, AgenticSQL adopts a multi-agent collaboration architecture — enabling high flexibility, transparency, and scalability.

The system is composed of specialized agents, each responsible for a discrete task: Named Entity Recognition (NER), Schema Mapping, Prompt Construction, SQL Generation, and SQL Validation. Powered by CrewAI and integrated with a Retrieval-Augmented Generation (RAG) pipeline, AgenticSQL dynamically retrieves schema context and historical query examples from vector databases like Qdrant or ChromaDB. This allows it to generalize across unseen schemas without retraining, making it ideal for enterprise analytics, SaaS applications, and AI-powered BI systems.

With the integration of a Model Context Protocol (MCP), AgenticSQL supports real-time routing and querying across multiple user databases, adapting intelligently based on user identity, intent, and query history. Each agent operates independently yet collaboratively, ensuring that the system remains modular, interpretable, and easily extendable.

AgenticSQL is fully open-source, deployable with local or cloud-based LLMs (e.g., Ollama, OpenAI), and built using FastAPI for seamless API integration. It represents a paradigm shift from black-box AI to cooperative, transparent systems that are both powerful and controllable — enabling anyone to “talk to their data” across any database, using plain English.

⸻
