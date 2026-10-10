"""Provider-neutral DA4LLM CORE proof of concept."""

from .model import ExecutionMode
from .validator import load_module

__all__ = ["ExecutionMode", "load_module"]
