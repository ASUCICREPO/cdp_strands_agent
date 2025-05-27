# 🚀 CDP Strands Agent Console

**Automated Project Analysis Tool for ASU Cloud Innovation Center**

A Streamlit-based web application that analyzes 2-page requirement documents and generates comprehensive technical deliverables using AI agents with Model Context Protocol (MCP) integration.

## 📋 Overview

The CDP Strands Agent Console automates the project planning process by:
- Analyzing project requirements documents
- Researching similar projects in ASUCICREPO
- Designing AWS serverless architectures
- Generating CDK code (TypeScript & Python)
- Estimating costs and providing optimization tips
- Creating comprehensive technical documentation

## 🏗️ Architecture

### Technology Stack
- **Streamlit** - Web interface framework
- **Strands** - AI agent framework for orchestration
- **MCP (Model Context Protocol)** - Tool integration layer
- **Python** - Core implementation language

### MCP Integrations
- **AWS Documentation Server** - Access to AWS service documentation
- **AWS CDK Server** - Cloud Development Kit assistance
- **AWS Cost Analysis Server** - Cost estimation capabilities
- **AWS Diagram Server** - Architecture diagram generation
- **GitHub Server** - Repository analysis (ASUCICREPO)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js (for GitHub MCP server)
- Git access to ASUCICREPO repository

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ASUCICREPO/cdp_strands_agent.git
   cd cdp_strands_agent
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install required MCP servers:**
   ```bash
   # AWS MCP servers (installed via uvx)
   pip install uv
   
   # GitHub MCP server
   npm install -g @modelcontextprotocol/server-github
   ```

4. **Set up environment variables:**
   ```bash
   # GitHub token for ASUCICREPO access
   export GITHUB_PERSONAL_ACCESS_TOKEN="your_github_token"
   ```

### Running the Application

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser.

## 📖 Usage Guide

### 1. Input Requirements
- Paste your 2-page project requirements document
- Set a descriptive project name
- Click "Initialize Project"

### 2. Analysis Workflow
The tool provides six analysis modules:

#### 🔍 Similar Projects Research
- Searches ASUCICREPO for comparable projects
- Analyzes existing architectures and patterns
- Identifies reusable components

#### 📋 Requirements Analysis
- Extracts functional and non-functional requirements
- Identifies stakeholders and success criteria
- Provides structured analysis

#### 🏗️ Architecture Design
- Creates AWS serverless architecture
- Generates draw.io XML diagrams
- References CIC best practices

#### 💻 CDK Code Generation
- **TypeScript CDK** - Enterprise-grade infrastructure code
- **Python CDK** - Python-based infrastructure definitions
- Both include proper imports and configurations

#### 💰 Cost Analysis
- Estimates monthly AWS costs
- Identifies cost drivers
- Provides optimization recommendations

#### 📚 Documentation
- Creates technical documentation
- Includes setup and deployment instructions
- References related CIC projects

### 3. Export Results
- Download individual analysis reports as Markdown files
- Export CDK code as TypeScript or Python files
- Save draw.io XML for architecture diagrams

## 🔧 Configuration

### MCP Server Configuration
The application automatically initializes multiple MCP servers:

```python
# AWS MCP Servers
aws_docs_client = MCPClient(lambda: stdio_client(StdioServerParameters(
    command="uvx", args=["awslabs.aws-documentation-mcp-server@latest"]
)))

# GitHub MCP Server
github_client = MCPClient(lambda: stdio_client(StdioServerParameters(
    command="npx", args=["-y", "@modelcontextprotocol/server-github"]
)))
```

### Environment Variables
```bash
# Required for GitHub integration
GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here

# Optional: AWS credentials for enhanced functionality
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
```

## 📁 Project Structure

```
cdp_strands_agent/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── run.py                # Alternative run script
└── app1.py               # Backup/alternative version
```

## 🎯 Key Features

### Real Project Integration
- Searches actual ASUCICREPO projects (not hallucinated)
- References existing CIC patterns and best practices
- Leverages proven architectures and deployment strategies

### Background Processing
- Non-blocking analysis execution
- Real-time status updates in sidebar
- Session state management for results persistence

### Comprehensive Output
- **Markdown Reports** - Detailed analysis and documentation
- **CDK Code** - Ready-to-deploy infrastructure definitions
- **Architecture Diagrams** - Visual representations via draw.io XML
- **Cost Estimates** - Practical AWS pricing information

## 🔍 ASUCICREPO Project References

The tool references these actual CIC projects:

**Document Processing & AI:**
- `PDF_Accessibility` - PDF remediation with AI-powered alt-text
- `PDF_accessability_UI` - UI for PDF accessibility tools
- `CDM-generation-agent` - CDM generation agent

**Chatbots & AI Assistants:**
- `Brightpoint` - Chatbot implementation
- `kelvyn-park-chat-assistant` - Multi-lingual school assistant
- `boystown_perplexity_implementation` - Serverless Perplexity AI API

**AWS Infrastructure & CDK:**
- `BedrockKnowledgeBases` - Python CDK for Bedrock + OpenSearch
- `Project_Constructs` - Reusable AWS constructs
- `amazon-transcribe-live-call-multilingual-contact-center` - Transcribe service

**Data Analysis & Detection:**
- `open-earth` - Land cover analysis
- `phoenix-pd-gunshot-detection` - Detection system
- `tempe-graffiti` - Graffiti analysis
- `osu-blueberry` - Agricultural analysis

## 🛠️ Development

### Local Development
```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
streamlit run app.py --server.runOnSave true
```

### Adding New Analysis Types
1. Create analysis function in the format `run_[analysis_name](agent, requirements_text, project_name)`
2. Add processing state management
3. Create UI tab and processing logic
4. Update session state initialization

## 🔧 Troubleshooting

### Common Issues

**MCP Server Connection Failures:**
- Ensure `uvx` is installed: `pip install uv`
- Check GitHub token permissions
- Verify network connectivity

**Streamlit Session Issues:**
- Clear browser cache
- Restart Streamlit server
- Check Python version compatibility

**Analysis Processing Hangs:**
- Check MCP server logs in sidebar
- Verify requirements text is not empty
- Restart the application

## 📊 Performance

### Typical Processing Times
- **Similar Projects Research**: 30-60 seconds
- **Requirements Analysis**: 15-30 seconds
- **Architecture Design**: 45-90 seconds
- **CDK Generation**: 30-60 seconds
- **Cost Analysis**: 20-40 seconds
- **Documentation**: 30-60 seconds

### Optimization Tips
- Initialize project once and run analyses incrementally
- Use specific, well-structured requirements documents
- Clear analysis results periodically to free memory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with detailed description

## 📄 License

This project is developed for the ASU Cloud Innovation Center. Please refer to ASU's software usage policies.

## 🆘 Support

For issues and support:
- Create an issue in the ASUCICREPO repository
- Contact the ASU Cloud Innovation Center team
- Check the troubleshooting section above

---

**CDP Project Analysis Agent** | ASU Cloud Innovation Center | Powered by Strands & MCP