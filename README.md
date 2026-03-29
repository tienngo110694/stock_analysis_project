# Vietnamese Stock Analysis Bot

A professional-grade Discord bot designed to provide deep financial insights into the Vietnamese stock market by combining the power of **Google Gemini AI** and the **vnstock** library.

## 🚀 Key Features

- **AI-Driven Intent Recognition**: Uses Gemini to understand natural language requests (e.g., "Cho mình xem tài chính của VNM") and extract stock tickers and data requirements.
- **Modular Data Collection**: High-performance fetching using `vnstock`'s modular `Quote`, `Finance`, and `Company` modules for historical prices, financial ratios, and company profiles.
- **Smart Command Handling**: Supports explicit `!stock <query>` commands and automatic shorthand ticker lookup (e.g., `!VCB`).
- **Workflow Automation**: Integrated with **n8n** webhooks to trigger complex financial processing pipelines and external reporting.
- **Optimized Architecture**: Built with a subclassed `commands.Bot` and persistent asynchronous HTTP sessions for world-class performance.

## 🛠️ Tech Stack

- **Language**: Python 3.12+
- **AI**: Google GenAI (Gemini)
- **Market Data**: vnstock
- **Bot Framework**: Discord.py
- **Networking**: aiohttp

## 📋 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd stock_analysis_project
   ```

2. **Install dependencies**:
   ```bash
   pip install discord.py google-genai vnstock pandas python-dotenv aiohttp
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   DISCORD_TOKEN=your_discord_bot_token
   GEMINI_API_KEY=your_google_gemini_api_key
   N8N_WEBHOOK_URL=your_n8n_webhook_url
   ```

4. **Start the Bot**:
   ```bash
   python main.py
   ```

## 🕹️ Usage

- **General Analysis**: `!stock [yêu cầu của bạn]`
  - *Example*: `!stock hãy phân tích kỹ thuật và xem hồ sơ công ty của mã FPT`
- **Shorthand Ticker**: `![MÃ_CHỨNG_KHOÁN]`
  - *Example*: `!VCB` (Directly fetches price and default info for VCB)

## 📊 Data Scope

- **Price History**: Last 30 trading days of OHLC data.
- **Financial Ratios**: Comprehensive quarterly indicators.
- **Company Profile**: Detailed overview including industry and business activity.