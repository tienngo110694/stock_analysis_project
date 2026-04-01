# 🇻🇳 Vietnamese Stock Analysis Bot (Antigravity & Gemini Edition)

A high-density, professional-grade Discord bot designed to provide structural financial insights into the Vietnamese stock market (HOSE). Powered by **Google Gemini 2.0**, **n8n orchestration**, and **ClickHouse Vector Storage**.

---

### 🛡️ Development Support
Developed and maintained using the **Antigravity IDE**, powered by **Gemini** to ensure high-performance code and state-of-the-art AI integration.

---

## 🌊 System Architecture & Flow

The project follows a 5-step specialized pipeline to provide comprehensive stock advice:

1.  **Step 0: Data Ingestion** - Collects financial statements and history from VNDirect/HOSE and stores them in **ClickHouse**.
2.  **Step 1: Discord Interaction** - Natural language Vietnamese chat interface processing via Gemini.
3.  **Step 2: Analysis Nodes** - Triggered via **n8n**, utilizing specialized Gemini nodes for:
    - **2.1**: Financial statement analysis (ClickHouse data).
    - **2.2**: Macro economy and Industry trends.
    - **2.3**: Stock-specific news crawling.
4.  **Step 3: AI Advisor** - Final aggregation node that provides **Buy/Sell/Neutral** advice with target prices.
5.  **Step 4: Vector Memory** - Analysis results are embedded via **Ollama** and stored in ClickHouse for future Q&A.

## 🚀 Key Features

-   **Modular AI Pipeline**: Separate logic for finance, news, and macro to prevent information dilution.
-   **Vector Search Ready**: Uses ClickHouse as a vector database for long-term project memory.
-   **Discord Frontend**: Real-time analysis requests with shorthand support (e.g., `!FPT`).
-   **Automated Ingestion**: `!ingest` command to populate the analytical database on-demand.

## 🛠️ Tech Stack

-   **Language**: Python 3.12+ (Asynchronous)
-   **AI Engines**: Google GenAI (Gemini 2.0 Pro/Flash), Ollama (Local Embeddings)
-   **Databases**: ClickHouse (OLAP + Vector Storage)
-   **Orchestration**: n8n Webhooks
-   **Market Data**: vnstock, VNDirect API

## 📋 Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd stock_analysis_project
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables** (`.env`):
    ```env
    DISCORD_TOKEN=your_token
    GEMINI_API_KEY=your_key
    N8N_WEBHOOK_URL=your_webhook
    CLICKHOUSE_HOST=localhost
    CLICKHOUSE_PORT=8123
    CLICKHOUSE_USER=default
    CLICKHOUSE_PASSWORD=
    ```

4.  **Run with Ollama**:
    Ensure Ollama is running `nomic-embed-text` for vector storage.

5.  **Start the Bot**:
    ```bash
    python main.py
    ```

## 🕹️ Usage

-   **Data Sync**: `!ingest [TICKER]` - Fetch latest financials to database.
-   **Standard Analysis**: `!stock [tiếng Việt]` - General analysis request.
-   **Full Report**: `!full_analysis [TICKER]` - Execute the entire analytical pipeline.
-   **Shorthand**: `!VNM` - Quick ticker lookup.

## 📂 Project Structure

-   `ai/`: Gemini analyst and advisor prompts.
-   `bot/`: Discord bot client and command definitions.
-   `data_collectors/`: Market data providers and scrapers.
-   `database/`: ClickHouse client and schema management.
-   `webhooks/`: External integration logic.

---
*Generated with support from Gemini 2.0 and Antigravity.*