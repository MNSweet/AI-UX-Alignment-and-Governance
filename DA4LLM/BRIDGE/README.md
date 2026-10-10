# DA4LLM BRIDGE

BRIDGE will own provider-, tool-, connector-, and runtime-specific mappings, including concrete invocation behavior, substitutions, access distinctions, and deterministic missing-capability handling.

CORE may define abstract capabilities; BRIDGE supplies platform-specific implementations. No bridge implementation is promoted in the bootstrap phase.

The current paired placeholder intentionally contains no ecosystem, provider, tool, connector, or runtime mapping. CORE requests generic capabilities through `CALL_CAPABILITY`; a future BRIDGE will select the active ecosystem and provide the corresponding invocation contract.
