# BotMan Digest

An automated intelligence gathering and analysis system for tracking Enterprise Agentic AI developments, multi-agent systems, and related industry developments.

## Overview

BotMan Digest is a GitHub Actions-powered automation that:
- **Creates daily digests** of AI & tech developments using xAI's Grok API
- **Maintains living documents** tracking the enterprise agentic AI landscape
- **Automatically updates baseline knowledge** by integrating daily findings into structured reference documents

The goal is to collect comprehensive industry intelligence on Enterprise Agentic Flow topics to inform the design of an enterprise open multi-agent communication protocol.

## 📁 Repository Structure

```
botman/
├── .github/
│   ├── scripts/
│   │   ├── create.daily.digest.py    # Generates daily AI news digest
│   │   └── update.py                  # Updates baseline documents
│   └── workflows/
│       └── daily-digest.yml           # GitHub Actions automation
├── docs/
│   ├── digest.md                      # Main knowledge base on Enterprise Agentic AI
│   ├── platforms.md                   # Platform capabilities summary
│   ├── update_summary.md              # Latest update log
│   └── raw_digest/                    # Archive of daily digests
│       ├── daily-digest_2026-02-XX_HH-MM.md
│       └── ...
└── prompts/
    ├── create_daily.digest.md         # Prompt for daily digest generation
    ├── update_digest.md               # Prompt for updating digest.md
    └── update_platforms.md            # Prompt for updating platforms.md
```

## 🚀 How It Works

### 1. Daily Digest Creation
Every day at 6 AM UTC (or on manual trigger):
- `create.daily.digest.py` calls the Grok API with the prompt from `prompts/create_daily.digest.md`
- Grok searches the web and summarizes the last 24 hours of AI developments
- Results are tagged by category:
  - Enterprise LLM frameworks
  - Multi-agent frameworks
  - Security
  - Blockchain for Gen AI
  - Regulatory news
  - Everything else
- Output is saved to `docs/raw_digest/daily-digest_{YYYY-MM-DD_HH-MM}.md`

### 2. Baseline Document Updates
Immediately after the daily digest:
- `update.py` reads the latest daily digest and current baseline documents
- Makes two separate API calls to update:
  - **digest.md**: Comprehensive reference on enterprise agentic AI, frameworks, models, and capabilities
  - **platforms.md**: Summary of major platforms (OpenAI, Anthropic, Google, etc.)
- Uses prompts from `prompts/update_digest.md` and `prompts/update_platforms.md`
- Preserves existing structure while integrating new information
- Generates `update_summary.md` with execution details

### 3. Git Automation
- Changes are automatically committed and pushed to the repository
- Commit message includes the date for easy tracking

## 🔧 Configuration

### Required Secrets
Set in GitHub repository settings → Secrets and variables → Actions:

- `GROK_DIGEST_API_KEY`: Your xAI API key for Grok access

### API Configuration

**Model**: `grok-4-1-fast-reasoning`
- Daily digest: 16,000 max tokens, temperature 0.3
- Digest update: 20,000 max tokens, temperature 0.2
- Platforms update: 12,000 max tokens, temperature 0.2

### Customization

**Modify prompts** in the `prompts/` directory to adjust:
- Categories/tags for daily digest
- Update rules for baseline documents
- Focus areas and priorities

**Adjust schedule** in `.github/workflows/daily-digest.yml`:
```yaml
schedule:
  - cron: '0 6 * * *'  # Change to your preferred time
```

## 📖 Key Documents

### [docs/digest.md](docs/digest.md)
The main intelligence document covering:
- Current state of enterprise agentic AI
- Major AI model releases (proprietary & open-source)
- Framework capabilities (orchestration, security, identity, routing, etc.)
- Industry trends and dominant themes

### [docs/platforms.md](docs/platforms.md)
Platform-by-platform breakdown of:
- OpenAI, Anthropic, Google, IBM, Corti, MiniMax, ByteDance, Glean, xAI
- Key features and recent developments
- Enterprise capabilities and integrations

### [docs/raw_digest/](docs/raw_digest/)
Complete archive of daily intelligence reports

## 🛠️ Local Development

### Prerequisites
- Python 3.12+
- `requests` library
- xAI API key

### Installation
```bash
pip install requests
```

### Environment Setup
```bash
# Set your API key
export GROK_API_KEY="your-api-key-here"
```

### Run Manually
```bash
# Generate a daily digest
python .github/scripts/create.daily.digest.py

# Update baseline documents
python .github/scripts/update.py
```

## 🎯 Focus Areas

The digest tracks developments in:
- **Enterprise Agentic AI platforms** (Cowork, Frontier, etc.)
- **Multi-agent frameworks** (AutoGen, LangChain, CrewAI, etc.)
- **Agent communication protocols** (MCP, A2A, ACP)
- **Model releases** (proprietary and open-source)
- **Security & privacy** frameworks
- **Blockchain integration** for Gen AI
- **Regulatory developments** (EU AI Act, etc.)
- **Infrastructure** (ultra-fast inference, quantum acceleration)

## 📊 Current State (Feb 2026)

Key themes being tracked:
- Agentic AI dominance in enterprise adoption
- Ultra-fast inference (1000+ tokens/sec)
- Chinese AI wave with affordable models
- Multi-agent orchestration frameworks
- Enterprise governance and compliance
- Open protocols and standards (MCP, A2A)

## 🤝 Contributing

To improve the automation:
1. Modify prompts in `prompts/` for better categorization or focus
2. Adjust API parameters in scripts for optimal results
3. Enhance the GitHub workflow for additional capabilities

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Resources

- [xAI Grok API Documentation](https://docs.x.ai/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Automated Intelligence for Enterprise Agentic AI**
