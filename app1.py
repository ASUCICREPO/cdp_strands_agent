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

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Strands and MCP imports
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

# Page configuration
st.set_page_config(
    page_title="CDP Project Analysis Agent",
    page_icon="🚀",
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
        background: #fffff;
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

def run_architecture_analysis(agent, requirements_text, project_name):
    """Simplified architecture with draw.io XML"""
    prompt = f"""
Design AWS serverless architecture for {project_name}:

{requirements_text}

Provide:
1. **Architecture Overview** (2-3 sentences)
2. **Key AWS Services** (bullet list with justification)
3. **Data Flow** (brief description)
4. **Security Approach** (3-4 points)
5. **Draw.io XML Diagram** (complete XML that can be imported into draw.io)

Focus on serverless AWS services. Keep text minimal. Include complete draw.io XML for architecture diagram.
"""
    
    try:
        response = agent(prompt)
        return str(response)
    except Exception as e:
        return f"Architecture analysis failed: {e}"

def run_typescript_cdk_generation(agent, requirements_text, project_name):
    """Generate TypeScript CDK only"""
    prompt = f"""
Generate TypeScript CDK for {project_name}:

{requirements_text}

Create a simple, working TypeScript CDK stack with:
- Basic AWS services (Lambda, API Gateway, DynamoDB)
- Proper imports and exports
- Clean, readable code
- Essential configurations only

Provide ONLY TypeScript CDK code, no explanations.
"""
    
    try:
        response = agent(prompt)
        return str(response)
    except Exception as e:
        return f"TypeScript CDK generation failed: {e}"

def run_python_cdk_generation(agent, requirements_text, project_name):
    """Generate Python CDK only"""
    prompt = f"""
Generate Python CDK for {project_name}:

{requirements_text}

Create a simple, working Python CDK stack with:
- Basic AWS services (Lambda, API Gateway, DynamoDB)
- Proper imports and constructs
- Clean, readable code
- Essential configurations only

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

def run_documentation_generation(agent, requirements_text, project_name):
    """Simplified documentation"""
    prompt = f"""
Create documentation for {project_name}:

{requirements_text}

Provide:
1. **Project Overview** (2-3 sentences)
2. **Setup Instructions** (step-by-step)
3. **API Endpoints** (if applicable)
4. **Deployment Steps** (simplified)

Keep it practical and concise. Focus on what developers need to know.
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
        <h1>🚀 CDP Project Analysis Agent</h1>
        <p>ASU Cloud Innovation Center - DevGenius Edition</p>
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
        'requirements_analysis', 'architecture_analysis', 'typescript_cdk', 'python_cdk',
        'cost_analysis', 'documentation', 'project_initialized'
    ]
    
    processing_types = [
        'processing_requirements', 'processing_architecture', 'processing_typescript',
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
    st.markdown("## 🎯 Project Analysis Workflow")
    
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
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Requirements", "🏗️ Architecture", "💻 CDK Code", "💰 Costs", "📚 Documentation"
        ])
        
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
                    st.session_state.project_name
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
                        st.session_state.project_name
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
                        st.session_state.project_name
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
                    st.session_state.project_name
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
