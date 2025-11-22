# Stock Agent

An intelligent stock analysis agent that provides comprehensive analysis of stocks and assets using multiple specialized AI agents. This project is based on the investment philosophy and criteria outlined in Peter Lynch's classic book **"One Up on Wall Street"**. The system evaluates stocks based on 18 different criteria inspired by Lynch's value investing principles to determine whether a stock should be bought.

## About

This project implements the stock analysis framework from **Peter Lynch's "One Up on Wall Street"**, one of the most influential investment books of all time. Lynch, who managed the Fidelity Magellan Fund and achieved an average annual return of 29.2% from 1977 to 1990, developed a systematic approach to evaluating stocks. This agent automates and applies his criteria using modern AI technology, making Lynch's investment wisdom accessible through an intelligent multi-agent system.

## Features

The Stock Agent analyzes stocks through a multi-agent system that evaluates:

1. **Insider Buying** - Whether company insiders are buying shares
2. **Share Buybacks** - If the company is repurchasing its own shares
3. **Name Analysis** - Whether the stock name sounds dull or ridiculous
4. **Business Nature** - If the company does something dull or disagreeable
5. **Spinoff Detection** - Whether the stock is a spinoff
6. **Institutional Ownership** - Institutional ownership and analyst coverage
7. **Rumors & Controversy** - Negative associations (toxic waste, mafia, etc.)
8. **Depressing Factors** - Negative aspects about the company
9. **Industry Growth** - Whether it's a no-growth industry
10. **Niche Market** - If the company has a niche
11. **Recurring Revenue** - Whether customers must keep buying the products
12. **Technology Usage** - If the company is a technology user
13. **P/E Ratio** - Price-to-earnings ratio analysis
14. **Earnings Growth** - Record of earnings growth and consistency
15. **Balance Sheet** - Debt-to-equity ratio and financial strength
16. **Cash Position** - Company's cash reserves
17. **Stock Category** - Classification (slow grower, stalwart, fast grower, cyclical, turnaround, asset play, or new issue)
18. **Financial Metrics** - Comprehensive financial analysis

## Requirements

- **Python**: >= 3.13
- **Operating System**: Windows (with specific setup instructions below)
- **Poppler**: External dependency required for PDF processing (see installation instructions)
- **API Keys**: 
  - Gemini API key (required)
  - Optional: OpenRouter API key

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd stockAgent
```

### 2. Install Poppler (Windows)

**Poppler is required for PDF to image conversion.** It must be installed separately on Windows:

#### Option A: Using Chocolatey (Recommended)

If you have Chocolatey installed:

```powershell
choco install poppler
```

#### Option B: Manual Installation

1. Download Poppler for Windows from: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract the ZIP file to a location like `C:\poppler` or `C:\Program Files\poppler`
3. Add Poppler's `bin` directory to your system PATH:
   - Open System Properties → Environment Variables
   - Edit the `Path` variable
   - Add the path to Poppler's `bin` folder (e.g., `C:\poppler\Library\bin`)
   - Restart your terminal/PowerShell

#### Verify Poppler Installation

After installation, verify it's working:

```powershell
pdftoppm -h
```

If the command shows help text, Poppler is correctly installed.

### 3. Set Up Python Environment

This project uses `uv` for dependency management. Install dependencies:

```bash
# If you don't have uv installed
pip install uv

# Install project dependencies
uv sync
```

Or if using traditional pip:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 4. Install Playwright Browsers

The project uses Playwright for web scraping. Install the required browsers:

```bash
playwright install chromium
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_KEY=your_gemini_api_key_here
OPENROUTER_KEY=your_openrouter_key_here  # Optional
```

Get your Gemini API key from: https://aistudio.google.com/apikey

## Usage

### Running the Application

Start the Gradio UI:

```bash
python main.py
```

The application will launch a web interface. Open the provided URL (typically `http://127.0.0.1:7860`) in your browser.

### Using the Stock Agent

1. Enter a stock ticker symbol (e.g., "DANGCEM", "BUAFOODS", "UACN")
2. The agent will:
   - Fetch company information from NGX (Nigerian Exchange)
   - Analyze the stock through all 18 criteria using specialized agents
   - Provide a comprehensive analysis and buy recommendation

### Example Stock Tickers

The system is configured to analyze Nigerian stocks. Example tickers include:
- `DANGCEM` - Dangote Cement PLC
- `BUAFOODS` - BUA Foods PLC
- `UACN` - UACN PLC
- `CADBURY` - Cadbury Nigeria PLC
- `PRESCO` - Presco PLC

## Project Structure

```
stockAgent/
├── main.py                 # Main application entry point
├── llms.py                 # LLM model configurations
├── pyproject.toml          # Project dependencies and metadata
├── tools/                  # Analysis tools
│   ├── get_company_info.py # Company information fetcher
│   ├── corporate_disclosures.py  # PDF processing and analysis
│   ├── director_disclosure.py    # Director information extraction
│   ├── earnings_growth.py        # Earnings analysis
│   ├── image_analysis.py         # Image processing
│   └── ocr.py                    # OCR functionality
├── sub_agents/             # Specialized analysis agents
│   ├── name_agent.py
│   ├── pe_ratio_agent.py
│   ├── balance_sheet_agent.py
│   ├── cash_position.py
│   └── ... (18 total agents)
└── stock_crawler/          # Scrapy-based web crawler
```

## Dependencies

Key dependencies include:
- `smolagents[litellm]` - Multi-agent framework
- `gradio` - Web UI
- `pdf2image` - PDF to image conversion (requires Poppler)
- `playwright` - Web scraping
- `camelot-py` - PDF table extraction
- `pytesseract` - OCR
- `transformers` - AI models
- `torch` - Deep learning framework

## Troubleshooting

### Poppler Not Found Error

If you encounter errors like "poppler not found" or "pdftoppm not found":

1. Verify Poppler is installed: `pdftoppm -h`
2. Check that Poppler's `bin` directory is in your PATH
3. Restart your terminal/PowerShell after adding to PATH
4. If using a virtual environment, ensure it's activated

### Playwright Issues

If Playwright browsers aren't working:

```bash
playwright install --force chromium
```

### API Key Issues

Ensure your `.env` file is in the project root and contains valid API keys. The application requires at least a `GEMINI_KEY`.

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

