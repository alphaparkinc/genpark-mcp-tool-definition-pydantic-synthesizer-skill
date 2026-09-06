"""
Demonstration of genpark-mcp-tool-definition-pydantic-synthesizer-skill
"""

from client import MCPToolDefinitionSynthesizerClient

def calculate_mortgage(principal: float, annual_rate: float, years: int = 30) -> float:
    """Calculates monthly mortgage payment based on loan amount and interest."""
    monthly_rate = (annual_rate / 100.0) / 12.0
    num_payments = years * 12
    return (principal * monthly_rate) / (1 - (1 + monthly_rate) ** (-num_payments))

def main():
    synthesizer = MCPToolDefinitionSynthesizerClient()
    mcp_schema = synthesizer.synthesize_mcp_tool(calculate_mortgage)

    import json
    print("=== SYNTHESIZED MCP TOOL DEFINITION ===")
    print(json.dumps(mcp_schema, indent=2))

if __name__ == "__main__":
    main()
