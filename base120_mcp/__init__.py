"""base120-mcp: 120 Mental Models for LLMs via Model Context Protocol."""

from .models import MODELS, MentalModel
from .server import Base120MCPServer

__version__ = "0.1.0"
__all__ = ["MODELS", "MentalModel", "Base120MCPServer"]
