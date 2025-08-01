# n8n Automation: Weather Agent with LLM Integration

This project showcases a simple automation workflow built using [n8n]([https://n8n.io/](https://ebadr761.app.n8n.cloud/workflow/bJh3s9fS5NlDydwP)), designed to act like an AI-powered assistant.

The workflow takes a natural language question from the user—such as _“Do I need an umbrella in downtown Calgary?”_—and performs the following:

1. Fetches live weather data from a public API (`wttr.in`)
2. Sends the weather data and original question to an LLM (e.g., OpenAI or a simulated Function node)
3. Returns a smart, human-readable answer with reasoning

The focus of this automation is to demonstrate how **API integration** and **AI-powered responses** can be combined in low-code workflows using n8n.

---

**Tech Stack**:  
- n8n (automation platform)  
- HTTP Request node  
- Function node or OpenAI integration  
- wttr.in (public weather API)

---

This is a minimal agent-style workflow intended for experimentation and learning around **AI automation pipelines**.
