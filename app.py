#!/usr/bin/env python3
"""
CDP Project Analysis Agent with Background Processing
Simplified Prompts and Separate CDK Triggers
"""

import streamlit as st
import json
import os
import time
from datetime import datetime
import sys
from pathlib import Path
import threading
import asyncio
import queue

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Strands and MCP imports
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

# Page configuration
st.set_page_config(
    page_title="CDP Strands Agent Console",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B35 0%, #F7931E 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .processing-indicator {
        background: black;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #FF6B35 0%, #F7931E 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_agent():
    """Initialize the Strands agent with MCP clients"""
    try:
        # AWS Documentation MCP Server
        aws_docs_client = MCPClient(
            lambda: stdio_client(StdioServerParameters(
                command="uvx", 
                args=["awslabs.aws-documentation-mcp-server@latest"]
            ))
        )

        # AWS CDK MCP Server
        aws_cdk_client = MCPClient(
            lambda: stdio_client(StdioServerParameters(
                command="uvx", 
                args=["awslabs.cdk-mcp-server@latest"]
            ))
        )

        # AWS Cost Analysis MCP Server  
        aws_cost_client = MCPClient(
            lambda: stdio_client(StdioServerParameters(
                command="uvx", 
                args=["awslabs.cost-analysis-mcp-server@latest"]
            ))
        )

        # AWS Diagram MCP Server for Architecture Diagrams
        aws_diagram_client = MCPClient(
            lambda: stdio_client(StdioServerParameters(
                command="uvx",
                args=["awslabs.aws-diagram-mcp-server@latest"]
            ))
        )

        # GitHub MCP Server for ASUCICREPO
        github_client = MCPClient(
            lambda: stdio_client(StdioServerParameters(
                command="npx",
                args=["-y", "@modelcontextprotocol/server-github"]
            ))
        )

        # Initialize tools with error handling
        working_clients = []
        mcp_clients = [
            ("AWS Docs", aws_docs_client),
            ("AWS CDK", aws_cdk_client), 
            ("AWS Cost", aws_cost_client),
            ("AWS Diagram", aws_diagram_client),
            ("GitHub", github_client)
        ]

        for name, client in mcp_clients:
            try:
                client.start()
                tools = client.list_tools_sync()
                working_clients.append(client)
                st.sidebar.success(f"✅ {name}: {len(tools)} tools")
            except Exception as e:
                st.sidebar.warning(f"⚠️ {name} failed: {str(e)[:50]}...")

        if len(working_clients) == 0:
            st.sidebar.error("❌ No MCP servers available")
            agent = Agent()
        else:
            agent = Agent(tools=working_clients)
        
        return agent, working_clients

    except Exception as e:
        st.error(f"Failed to initialize agent: {e}")
        return Agent(), []

def run_similar_projects_research(agent, requirements_text, project_name):
    """Research similar projects in ASUCICREPO"""
    prompt = f"""
Research similar projects in ASUCICREPO for {project_name}:

{requirements_text}

IMPORTANT: Search the GitHub repository ASUCICREPO for ACTUAL existing projects. The repository contains these real projects:

**Document Processing & AI:**
- PDF_Accessibility - PDF remediation tool for WCAG 2.1 compliance with AI-powered alt-text
- PDF_accessability_UI - UI for PDF accessibility tools
- CDM-generation-agent - CDM generation agent

**Chatbots & AI Assistants:**
- Brightpoint - Chatbot code
- kelvyn-park-chat-assistant - Multi-lingual chat assistant for school
- boystown_perplexity_implementation - Serverless API with Perplexity AI integration

**AWS Infrastructure & CDK:**
- BedrockKnowledgeBases - Python CDK construct for Bedrock Knowledge Base with OpenSearch
- Project_Constructs - AWS constructs collection
- amazon-transcribe-live-call-multilingual-contact-center - AWS Transcribe with multilingual support

**Data Analysis & Detection:**
- open-earth - Land cover analysis
- phoenix-pd-gunshot-detection - Detection system for Phoenix PD  
- tempe-graffiti - Graffiti detection/analysis
- osu-blueberry - Agricultural/analysis project

Use GitHub MCP tools to:
1. **Search ASUCICREPO** - Find projects that actually match the requirements from the list above
2. **Analyze Architecture** - Look at the actual code and architecture patterns used
3. **Identify Reusable Components** - Find CDK constructs, Lambda patterns, API designs
4. **Reference Real Projects** - Only mention projects that actually exist in the repository
5. **Extract Patterns** - Find common AWS services, deployment patterns, folder structures

Focus ONLY on projects that actually exist in ASUCICREPO. Do not invent or hallucinate project names.
"""
    
    try:
        response = agent(prompt)
        return str(response)
    except Exception as e:
        return f"Similar projects research failed: {e}"

def run_requirements_analysis(agent, requirements_text, project_name):
    """Simplified requirements analysis"""
    prompt = f"""
Analyze requirements for {project_name}:

{requirements_text}

Provide:
1. **Key Functional Requirements** (bullet points)
2. **Key Non-Functional Requirements** (bullet points)
3. **Main Stakeholders** (list)
4. **Success Criteria** (3-5 points)

Keep it concise and focused. No lengthy explanations.
"""
    
    try:
        response = agent(prompt)
        return str(response)
    except Exception as e:
        return f"Requirements analysis failed: {e}"

def run_architecture_analysis(agent, requirements_text, project_name, similar_projects_context=""):
    """Enhanced architecture with similar projects context"""
    prompt = f"""
Design AWS serverless architecture for {project_name}:

{requirements_text}

Similar Projects Context: {similar_projects_context}

Reference ACTUAL ASUCICREPO projects when relevant:
- **PDF_Accessibility** - For document processing with AI
- **BedrockKnowledgeBases** - For knowledge bases and RAG patterns  
- **boystown_perplexity_implementation** - For serverless APIs with AI integration
- **Brightpoint** or **kelvyn-park-chat-assistant** - For chatbot architectures

Provide:
1. **Architecture Overview** (2-3 sentences)
2. **Key AWS Services** (bullet list with justification based on CIC patterns)
3. **Data Flow** (brief description following CIC approaches)  
4. **Security Approach** (3-4 points using CIC best practices)
5. **CIC Project References** - Reference ONLY actual ASUCICREPO projects that use similar patterns
6. **Draw.io XML Diagram** (complete XML that can be imported into draw.io)

Focus on serverless AWS services. Leverage patterns from actual CIC projects. Include complete draw.io XML for architecture diagram.
"""
    
    try:
        response = agent(prompt)
        return str(response)
    except Exception as e:
        return f"Architecture analysis failed: {e}"

def run_diagram_generation(agent, requirements_text, project_name, architecture_context=""):
    """Generate draw.io XML diagram efficiently"""
    prompt = f"""
Create a SIMPLE draw.io XML diagram for {project_name}:

Requirements: {requirements_text}
Architecture: {architecture_context}

Generate a basic draw.io XML with 5-7 key AWS components:
- API Gateway
- Lambda function
- Database (DynamoDB/RDS)
- S3 bucket (if needed)
- CloudWatch

Create MINIMAL XML - keep it simple with basic rectangles and arrows.
Use standard AWS service names as labels.
Focus on core data flow only.

Provide ONLY the XML code, nothing else.
"""
    
    try:
        response = agent(prompt)
        return str(response)
    except Exception as e:
        return f"Diagram generation failed: {e}"

def run_typescript_cdk_generation(agent, requirements_text, project_name, similar_projects_context=""):
    """Generate TypeScript CDK with CIC project references"""
    prompt = f"""
Generate TypeScript CDK for {project_name}:

{requirements_text}

Similar Projects Context: {similar_projects_context}

Create a simple, working TypeScript CDK stack with:
- Basic AWS services (Lambda, API Gateway, DynamoDB)
- Proper imports and exports
- Clean, readable code following CIC patterns
- Essential configurations only
- Reference similar constructs from ASUCICREPO projects

Provide ONLY TypeScript CDK code, no explanations.
"""
    
    try:
        response = agent(prompt)
        return str(response)
    except Exception as e:
        return f"TypeScript CDK generation failed: {e}"

def run_python_cdk_generation(agent, requirements_text, project_name, similar_projects_context=""):
    """Generate Python CDK with CIC project references"""
    prompt = f"""
Generate Python CDK for {project_name}:

{requirements_text}

Similar Projects Context: {similar_projects_context}

Create a simple, working Python CDK stack with:
- Basic AWS services (Lambda, API Gateway, DynamoDB)
- Proper imports and constructs
- Clean, readable code following CIC patterns
- Essential configurations only
- Reference similar constructs from ASUCICREPO projects

Provide ONLY Python CDK code, no explanations.
"""
    
    try:
        response = agent(prompt)
        return str(response)
    except Exception as e:
        return f"Python CDK generation failed: {e}"

def run_cost_analysis(agent, requirements_text, project_name):
    """Simplified cost analysis"""
    prompt = f"""
Estimate costs for {project_name}:

{requirements_text}

Provide:
1. **Monthly Cost Estimate** (total number)
2. **Key Cost Drivers** (top 3 services)
3. **Cost Breakdown** (service costs)
4. **Optimization Tips** (3-4 points)

Keep it simple and practical. Focus on actual AWS pricing.
"""
    
    try:
        response = agent(prompt)
        return str(response)
    except Exception as e:
        return f"Cost analysis failed: {e}"

def run_documentation_generation(agent, requirements_text, project_name, similar_projects_context=""):
    """Enhanced documentation with CIC project references"""
    prompt = f"""
Create documentation for {project_name}:

{requirements_text}

Similar Projects Context: {similar_projects_context}

Reference ACTUAL ASUCICREPO projects for patterns and best practices:
- **PDF_Accessibility** - Document processing deployment patterns
- **BedrockKnowledgeBases** - CDK construct documentation style
- **boystown_perplexity_implementation** - Serverless API documentation  
- **Brightpoint** - Chatbot setup instructions
- **Project_Constructs** - AWS construct documentation patterns

Provide:
1. **Project Overview** (2-3 sentences)
2. **Setup Instructions** (step-by-step, following CIC documentation standards)
3. **API Endpoints** (if applicable, using CIC API documentation style)
4. **Deployment Steps** (simplified, using actual CIC deployment patterns)
5. **Related CIC Projects** - Reference ONLY actual projects from ASUCICREPO  
6. **Lessons Learned** - Insights from actual CIC implementations

Keep it practical and concise. Follow documentation patterns from actual CIC projects.
"""
    
    try:
        response = agent(prompt)
        return str(response)
    except Exception as e:
        return f"Documentation generation failed: {e}"

def background_analysis(analysis_func, *args):
    """Run analysis in background and update session state"""
    try:
        result = analysis_func(*args)
        return result
    except Exception as e:
        return f"Background analysis failed: {e}"


def render_header():
    """Render the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 CDP Strands Agent Console</h1>
        <p>ASU Cloud Innovation Center</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar"""
    st.sidebar.title("📋 Agent Dashboard")
    
    # Initialize agent and show status
    try:
        agent, working_clients = initialize_agent()
        st.sidebar.success(f"✅ Agent Ready")
        st.sidebar.info(f"🔌 {len(working_clients)} MCP Servers")
        
        # Show analysis status
        st.sidebar.markdown("### 📊 Analysis Status")
        
        analysis_status = {
            "Similar Projects": st.session_state.get('similar_projects_research', None) is not None,
            "Requirements": st.session_state.get('requirements_analysis', None) is not None,
            "Architecture": st.session_state.get('architecture_analysis', None) is not None,
            "TypeScript CDK": st.session_state.get('typescript_cdk', None) is not None,
            "Python CDK": st.session_state.get('python_cdk', None) is not None,
            "Cost Analysis": st.session_state.get('cost_analysis', None) is not None,
            "Documentation": st.session_state.get('documentation', None) is not None
        }
        
        for item, completed in analysis_status.items():
            if completed:
                st.sidebar.success(f"✅ {item}")
            else:
                st.sidebar.info(f"⏳ {item}")
        
        # Processing status
        processing_status = {
            "Similar Projects": st.session_state.get('processing_similar_projects', False),
            "Requirements": st.session_state.get('processing_requirements', False),
            "Architecture": st.session_state.get('processing_architecture', False),
            "TypeScript CDK": st.session_state.get('processing_typescript', False),
            "Python CDK": st.session_state.get('processing_python', False),
            "Cost": st.session_state.get('processing_cost', False),
            "Documentation": st.session_state.get('processing_docs', False)
        }
        
        active_processing = [item for item, processing in processing_status.items() if processing]
        if active_processing:
            st.sidebar.warning(f"🔄 Processing: {', '.join(active_processing)}")
        
        return agent, working_clients
    except Exception as e:
        st.sidebar.error(f"❌ Agent Error: {e}")
        return None, []

def main():
    """Main Streamlit application"""
    
    # Render header
    render_header()
    
    # Initialize session state
    analysis_types = [
        'similar_projects_research', 'requirements_analysis', 'architecture_analysis', 'typescript_cdk', 'python_cdk',
        'cost_analysis', 'documentation', 'project_initialized'
    ]
    
    processing_types = [
        'processing_similar_projects', 'processing_requirements', 'processing_architecture', 'processing_typescript',
        'processing_python', 'processing_cost', 'processing_docs'
    ]
    
    for analysis_type in analysis_types + processing_types:
        if analysis_type not in st.session_state:
            st.session_state[analysis_type] = None if 'processing_' not in analysis_type else False
    
    # Render sidebar and get agent
    agent, working_clients = render_sidebar()
    
    if not agent:
        st.error("❌ CDP Agent failed to initialize. Please check the logs in the sidebar.")
        st.stop()
    
    # Main content
    st.markdown("## 🎯 Project Workflow")
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 📝 Project Requirements")
        requirements_text = st.text_area(
            "Paste your 2-pager requirements document:",
            height=300,
            placeholder="""Problem Statement: Create a serverless document processing platform...

Functional Requirements:
- Users must be able to upload PDF documents
- The system shall extract text using AI
- Users should receive email notifications

Non-Functional Requirements:
- Process documents within 30 seconds
- Support 99.9% uptime
- Handle 500 concurrent users"""
        )
    
    with col2:
        st.markdown("### ⚙️ Analysis Settings")
        project_name = st.text_input("Project Name", value="my-project")
        
        st.markdown("### 🚀 Actions")
        
        # Initialize project button
        if st.button("🔄 Initialize Project", type="primary"):
            if requirements_text and project_name:
                st.session_state.project_name = project_name
                st.session_state.requirements_text = requirements_text
                st.session_state.project_initialized = True
                st.success("✅ Project initialized!")
                st.rerun()
            else:
                st.warning("⚠️ Please provide both project name and requirements")
        
        if st.button("🗑️ Clear All Analysis"):
            for analysis_type in analysis_types + processing_types:
                st.session_state[analysis_type] = None if 'processing_' not in analysis_type else False
            st.success("All analysis cleared!")
            st.rerun()
    
    # Show analysis results only if project is initialized
    if st.session_state.get('project_initialized'):
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")
        
        # Create tabs for results
        tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🔍 Similar Projects", "📋 Requirements", "🏗️ Architecture", "💻 CDK Code", "💰 Costs", "📚 Documentation"
        ])
        
        # Similar Projects Tab
        with tab0:
            st.markdown("### 🔍 Research Similar Projects")
            
            if st.button("🔍 Research Similar Projects", key="similar_btn"):
                st.session_state.processing_similar_projects = True
                st.rerun()
            
            # Show processing or results
            if st.session_state.get('processing_similar_projects') and not st.session_state.get('similar_projects_research'):
                st.markdown("""
                <div class="processing-indicator">
                    🤖 Agent is researching ASUCICREPO for similar projects...
                </div>
                """, unsafe_allow_html=True)
                
                # Run analysis in background
                result = background_analysis(
                    run_similar_projects_research,
                    agent,
                    st.session_state.requirements_text,
                    st.session_state.project_name
                )
                st.session_state.similar_projects_research = result
                st.session_state.processing_similar_projects = False
                st.rerun()
            
            elif st.session_state.get('similar_projects_research'):
                st.markdown(st.session_state.similar_projects_research)
                st.download_button(
                    label="📥 Download Similar Projects Research",
                    data=st.session_state.similar_projects_research,
                    file_name=f"{st.session_state.project_name}_similar_projects.md",
                    mime="text/markdown"
                )
            else:
                st.info("👆 Click 'Research Similar Projects' to search ASUCICREPO for relevant projects")
        
        # Requirements Tab
        with tab1:
            st.markdown("### 📋 Requirements Analysis")
            
            if st.button("🔍 Create Requirements Analysis", key="req_btn"):
                st.session_state.processing_requirements = True
                st.rerun()
            
            # Show processing or results
            if st.session_state.get('processing_requirements') and not st.session_state.get('requirements_analysis'):
                st.markdown("""
                <div class="processing-indicator">
                    🤖 Agent is analyzing requirements in the background...
                </div>
                """, unsafe_allow_html=True)
                
                # Run analysis in background
                result = background_analysis(
                    run_requirements_analysis,
                    agent,
                    st.session_state.requirements_text,
                    st.session_state.project_name
                )
                st.session_state.requirements_analysis = result
                st.session_state.processing_requirements = False
                st.rerun()
            
            elif st.session_state.get('requirements_analysis'):
                st.markdown(st.session_state.requirements_analysis)
                st.download_button(
                    label="📥 Download Requirements",
                    data=st.session_state.requirements_analysis,
                    file_name=f"{st.session_state.project_name}_requirements.md",
                    mime="text/markdown"
                )
            else:
                st.info("👆 Click 'Create Requirements Analysis' to start")
        
        # Architecture Tab
        with tab2:
            st.markdown("### 🏗️ Solution Architecture")
            
            if st.button("🏗️ Create Architecture", key="arch_btn"):
                st.session_state.processing_architecture = True
                st.rerun()
            
            # Show processing or results
            if st.session_state.get('processing_architecture') and not st.session_state.get('architecture_analysis'):
                st.markdown("""
                <div class="processing-indicator">
                    🤖 Agent is designing architecture in the background...
                </div>
                """, unsafe_allow_html=True)
                
                # Run analysis in background
                result = background_analysis(
                    run_architecture_analysis,
                    agent,
                    st.session_state.requirements_text,
                    st.session_state.project_name,
                    st.session_state.get('similar_projects_research', '')
                )
                st.session_state.architecture_analysis = result
                st.session_state.processing_architecture = False
                st.rerun()
            
            elif st.session_state.get('architecture_analysis'):
                arch_response = st.session_state.architecture_analysis
                
                # Extract and display XML separately if present
                if "<mxfile" in arch_response or "<?xml" in arch_response:
                    # Split text and XML
                    parts = arch_response.split("<?xml" if "<?xml" in arch_response else "<mxfile")
                    text_part = parts[0]
                    xml_part = ("<?xml" if "<?xml" in arch_response else "<mxfile") + parts[1] if len(parts) > 1 else ""
                    
                    st.markdown(text_part)
                    
                    if xml_part:
                        st.markdown("### 🎨 Draw.io Architecture Diagram")
                        st.code(xml_part, language="xml")
                        st.info("💡 Copy the XML above and paste it into draw.io to view the architecture diagram")
                else:
                    st.markdown(arch_response)
                
                st.download_button(
                    label="📥 Download Architecture",
                    data=st.session_state.architecture_analysis,
                    file_name=f"{st.session_state.project_name}_architecture.md",
                    mime="text/markdown"
                )
            else:
                st.info("👆 Click 'Create Architecture' to start")
        
        # CDK Code Tab
        with tab3:
            st.markdown("### 💻 CDK Implementation")
            
            # Separate tabs for TypeScript and Python
            ts_tab, py_tab = st.tabs(["TypeScript", "Python"])
            
            with ts_tab:
                if st.button("🔧 Generate TypeScript CDK", key="ts_btn"):
                    st.session_state.processing_typescript = True
                    st.rerun()
                
                # Show processing or results
                if st.session_state.get('processing_typescript') and not st.session_state.get('typescript_cdk'):
                    st.markdown("""
                    <div class="processing-indicator">
                        🤖 Agent is generating TypeScript CDK in the background...
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Run analysis in background
                    result = background_analysis(
                        run_typescript_cdk_generation,
                        agent,
                        st.session_state.requirements_text,
                        st.session_state.project_name,
                        st.session_state.get('similar_projects_research', '')
                    )
                    st.session_state.typescript_cdk = result
                    st.session_state.processing_typescript = False
                    st.rerun()
                
                elif st.session_state.get('typescript_cdk'):
                    st.code(st.session_state.typescript_cdk, language="typescript")
                    st.download_button(
                        label="📥 Download TypeScript CDK",
                        data=st.session_state.typescript_cdk,
                        file_name=f"{st.session_state.project_name}_cdk.ts",
                        mime="text/plain"
                    )
                else:
                    st.info("👆 Click 'Generate TypeScript CDK' to start")
            
            with py_tab:
                if st.button("🐍 Generate Python CDK", key="py_btn"):
                    st.session_state.processing_python = True
                    st.rerun()
                
                # Show processing or results
                if st.session_state.get('processing_python') and not st.session_state.get('python_cdk'):
                    st.markdown("""
                    <div class="processing-indicator">
                        🤖 Agent is generating Python CDK in the background...
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Run analysis in background
                    result = background_analysis(
                        run_python_cdk_generation,
                        agent,
                        st.session_state.requirements_text,
                        st.session_state.project_name,
                        st.session_state.get('similar_projects_research', '')
                    )
                    st.session_state.python_cdk = result
                    st.session_state.processing_python = False
                    st.rerun()
                
                elif st.session_state.get('python_cdk'):
                    st.code(st.session_state.python_cdk, language="python")
                    st.download_button(
                        label="📥 Download Python CDK",
                        data=st.session_state.python_cdk,
                        file_name=f"{st.session_state.project_name}_cdk.py",
                        mime="text/plain"
                    )
                else:
                    st.info("👆 Click 'Generate Python CDK' to start")
        
        # Cost Analysis Tab
        with tab4:
            st.markdown("### 💰 Cost Analysis")
            
            if st.button("💰 Create Cost Analysis", key="cost_btn"):
                st.session_state.processing_cost = True
                st.rerun()
            
            # Show processing or results
            if st.session_state.get('processing_cost') and not st.session_state.get('cost_analysis'):
                st.markdown("""
                <div class="processing-indicator">
                    🤖 Agent is analyzing costs in the background...
                </div>
                """, unsafe_allow_html=True)
                
                # Run analysis in background
                result = background_analysis(
                    run_cost_analysis,
                    agent,
                    st.session_state.requirements_text,
                    st.session_state.project_name
                )
                st.session_state.cost_analysis = result
                st.session_state.processing_cost = False
                st.rerun()
            
            elif st.session_state.get('cost_analysis'):
                st.markdown(st.session_state.cost_analysis)
                st.download_button(
                    label="📥 Download Cost Analysis",
                    data=st.session_state.cost_analysis,
                    file_name=f"{st.session_state.project_name}_costs.md",
                    mime="text/markdown"
                )
            else:
                st.info("👆 Click 'Create Cost Analysis' to start")
        
        # Documentation Tab
        with tab5:
            st.markdown("### 📚 Technical Documentation")
            
            if st.button("📚 Generate Documentation", key="doc_btn"):
                st.session_state.processing_docs = True
                st.rerun()
            
            # Show processing or results
            if st.session_state.get('processing_docs') and not st.session_state.get('documentation'):
                st.markdown("""
                <div class="processing-indicator">
                    🤖 Agent is creating documentation in the background...
                </div>
                """, unsafe_allow_html=True)
                
                # Run analysis in background
                result = background_analysis(
                    run_documentation_generation,
                    agent,
                    st.session_state.requirements_text,
                    st.session_state.project_name,
                    st.session_state.get('similar_projects_research', '')
                )
                st.session_state.documentation = result
                st.session_state.processing_docs = False
                st.rerun()
            
            elif st.session_state.get('documentation'):
                st.markdown(st.session_state.documentation)
                st.download_button(
                    label="📥 Download Documentation",
                    data=st.session_state.documentation,
                    file_name=f"{st.session_state.project_name}_docs.md",
                    mime="text/markdown"
                )
            else:
                st.info("👆 Click 'Generate Documentation' to start")
    
    else:
        st.info("🔄 Please initialize your project above to begin analysis")
    
    # Footer
    st.markdown("---")
    st.markdown("**CDP Project Analysis Agent** | ASU Cloud Innovation Center | Powered by Strands & MCP")

if __name__ == "__main__":
    main()