#!/usr/bin/env python3
"""
Enhanced CDP Project Analysis Agent
Complete CIC development workflow with CDK, architecture diagrams, and documentation
"""

from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters
import json
import os

def main():
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
            print(f"🔌 Connecting to {name} MCP server...")
            client.start()
            tools = client.list_tools_sync()
            working_clients.append(client)
            print(f"✅ {name}: {len(tools)} tools loaded")
        except Exception as e:
            print(f"⚠️  {name} MCP server failed: {e}")
            print(f"   Continuing without {name}...")

    print(f"\n🛠️  Working MCP servers: {len(working_clients)}")

    if len(working_clients) == 0:
        print("❌ No MCP servers available. Running in basic mode...")
        agent = Agent()
    else:
        # Create enhanced agent with comprehensive system prompt
        agent = Agent(
            tools=working_clients,
            system_prompt="""You are the CDP (Cloud Development Platform) Project Analysis Agent for ASU CIC.

MISSION: Transform project requirements into complete, production-ready AWS solutions.

WORKFLOW FOR NEW PROJECTS:
1. REQUIREMENTS ANALYSIS
   - Parse 2-pager documents following CIC methodology
   - Extract functional & non-functional requirements
   - Identify stakeholder needs and success criteria

2. RESEARCH & ARCHITECTURE
   - Search ASUCICREPO for similar projects and patterns
   - Design serverless-first AWS architecture
   - Generate detailed architecture diagrams (draw.io compatible)
   - Select appropriate AWS services with justification

3. CDK CODE GENERATION
   - Generate both TypeScript AND Python CDK stacks
   - Include proper constructs, permissions, and configurations
   - Follow CIC best practices for infrastructure as code
   - Add monitoring, logging, and security by default

4. COST ANALYSIS
   - Provide detailed cost breakdowns by service
   - Include monthly and yearly estimates
   - Suggest cost optimization strategies
   - Consider different usage scenarios

5. TECHNICAL DOCUMENTATION
   - Create comprehensive documentation
   - Include deployment instructions
   - Add troubleshooting guides
   - Document API specifications and usage

ALWAYS:
- Use actual CIC project patterns from ASUCICREPO
- Generate production-ready, secure code
- Include comprehensive error handling
- Follow AWS Well-Architected principles
- Provide actionable, implementable solutions

For architecture diagrams, generate draw.io compatible XML that can be directly imported."""
        )
    
    return agent, working_clients

def analyze_project_requirements(agent, requirements_doc):
    """Complete project analysis workflow"""
    
    prompt = f"""
COMPLETE CIC PROJECT ANALYSIS

Project Requirements:
{requirements_doc}

Please provide a COMPREHENSIVE analysis following the CIC development process:

1. 📋 REQUIREMENTS ANALYSIS
   - Extract and categorize all functional requirements
   - Identify non-functional requirements (performance, security, scalability)
   - List stakeholder needs and success criteria
   - Estimate project complexity (Low/Medium/High)

2. 🔍 RESEARCH SIMILAR PROJECTS
   - Search ASUCICREPO for relevant projects
   - Identify reusable patterns and constructs
   - Recommend architectural approaches based on past success

3. 🏗️ SOLUTION ARCHITECTURE
   - Design comprehensive AWS serverless architecture
   - Generate draw.io compatible architecture diagram XML
   - Justify service selections with pros/cons
   - Include data flow and security considerations

4. 💻 CDK IMPLEMENTATION
   - Generate COMPLETE TypeScript CDK stack
   - Generate COMPLETE Python CDK stack
   - Include all necessary constructs, permissions, monitoring
   - Add proper error handling and logging

5. 💰 COST ANALYSIS
   - Detailed cost breakdown by AWS service
   - Monthly/yearly estimates for different usage levels
   - Cost optimization recommendations
   - TCO analysis including operational costs

6. 📚 TECHNICAL DOCUMENTATION
   - Deployment guide with step-by-step instructions
   - API documentation and usage examples
   - Troubleshooting guide
   - Monitoring and maintenance procedures

Please be thorough and provide production-ready, implementable solutions.
"""
    
    print("🤖 Analyzing project requirements...")
    print("=" * 60)
    
    response = agent(prompt)
    return response

def save_project_analysis(project_name, analysis_response):
    """Save the analysis results to files"""
    
    # Create project directory
    project_dir = f"projects/{project_name}"
    os.makedirs(project_dir, exist_ok=True)
    
    # Save complete analysis
    with open(f"{project_dir}/complete_analysis.md", "w") as f:
        f.write(str(analysis_response))
    
    print(f"📁 Analysis saved to {project_dir}/")
    return project_dir

if __name__ == "__main__":
    print("🚀 Enhanced CDP Project Analysis Agent - ASU CIC Edition")
    print("=" * 70)
    
    agent, working_clients = main()
    
    try:
        print("\n💬 Enhanced Interactive Mode")
        print("Commands:")
        print("- 'analyze: <paste your 2-pager requirements>'")
        print("- 'project: <project-name>' (for focused analysis)")
        print("- Regular questions about AWS services")
        print("- 'exit' to quit")
        
        while True:
            user_input = input("\n> ")
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                break
            
            # Check if this is a project analysis request
            if user_input.startswith('analyze:'):
                requirements = user_input[8:].strip()
                if requirements:
                    # Get project name
                    project_name = input("Project name: ").strip() or "new-project"
                    
                    # Run complete analysis
                    analysis = analyze_project_requirements(agent, requirements)
                    print(f"\n🤖 COMPLETE PROJECT ANALYSIS:\n{analysis}")
                    
                    # Save results
                    save_project_analysis(project_name, analysis)
                else:
                    print("Please provide requirements after 'analyze:'")
            
            elif user_input.startswith('project:'):
                project_name = user_input[8:].strip()
                if project_name:
                    requirements = input(f"Paste requirements for {project_name}:\n")
                    analysis = analyze_project_requirements(agent, requirements)
                    print(f"\n🤖 ANALYSIS FOR {project_name.upper()}:\n{analysis}")
                    save_project_analysis(project_name, analysis)
            
            else:
                # Regular question
                response = agent(user_input)
                print(f"\n🤖 {response}")
                
    except KeyboardInterrupt:
        print("\n")
    finally:
        # Clean up MCP clients
        for client in working_clients:
            try:
                client.stop()
            except:
                pass
    
    print("👋 Thanks for using Enhanced CDP Agent!")