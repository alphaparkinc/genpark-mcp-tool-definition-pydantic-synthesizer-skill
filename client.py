"""
MCP Tool Schema Synthesizer from Python Function Signatures.
Zero external dependencies, standard library only.
"""

import inspect
from typing import Dict, List, Any, Optional, Callable, get_type_hints

class MCPToolDefinitionSynthesizerClient:
    """
    Introspects native Python functions, extracting docstrings, type annotations,
    and parameter defaults to synthesize standard Model Context Protocol (MCP) schemas.
    """

    def __init__(self):
        pass

    def _type_to_json_type(self, type_hint: Any) -> str:
        if type_hint in (int,):
            return "integer"
        elif type_hint in (float,):
            return "number"
        elif type_hint in (bool,):
            return "boolean"
        elif type_hint in (str,):
            return "string"
        elif type_hint in (list, List):
            return "array"
        elif type_hint in (dict, Dict):
            return "object"
        return "string"

    def synthesize_mcp_tool(self, fn: Callable) -> Dict[str, Any]:
        """Generates standard MCP tool schema from python function."""
        sig = inspect.signature(fn)
        type_hints = {}
        try:
            type_hints = get_type_hints(fn)
        except Exception:
            pass

        doc = inspect.getdoc(fn) or "No description provided."
        properties = {}
        required = []

        for p_name, param in sig.parameters.items():
            if p_name in ("self", "cls"):
                continue

            th = type_hints.get(p_name, str)
            json_type = self._type_to_json_type(th)

            properties[p_name] = {
                "type": json_type,
                "description": f"Parameter {p_name}"
            }

            if param.default == inspect.Parameter.empty:
                required.append(p_name)

        return {
            "name": fn.__name__,
            "description": doc.strip(),
            "inputSchema": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
