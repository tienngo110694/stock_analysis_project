# Stock Analysis Discord Bot

This project implements a Discord bot that analyzes Vietnamese stocks using natural language processing with Google Gemini AI and data from vnstock library.

## Project Flow

1. **Discord Chat**: Users chat in Vietnamese about stock codes and requests
2. **Gemini Summarization**: First Gemini node extracts stock code and information type from the message
3. **Data Collection**: StockInformationCollector class gathers relevant financial data
4. **Response Generation**: Second Gemini node summarizes all data into a natural response
5. **Discord Reply**: Bot responds to the user on Discord

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   - Copy `.env` and fill in your tokens:
     - `DISCORD_TOKEN`: Your Discord bot token from https://discord.com/developers/applications
     - `GEMINI_API_KEY`: Your Google Gemini API key from https://makersuite.google.com/app/apikey

3. **Run the Bot**:
   ```bash
   python discord_listen_reply.py
   ```

## Usage

- Mention a stock code (e.g., "VNM", "VCB") in Vietnamese
- Ask questions about price, financials, overview, etc.
- The bot will analyze, collect data, and provide summarized responses

## Files

- `discord_listen_reply.py`: Main bot implementation
- `stock_information_collector.py`: Stock data collection class
- `stock_information_collector.ipynb`: Jupyter notebook version
- `project_description.txt`: Project overview

## Dependencies

- discord.py
- google-generativeai
- vnstock
- python-dotenv
- pandas