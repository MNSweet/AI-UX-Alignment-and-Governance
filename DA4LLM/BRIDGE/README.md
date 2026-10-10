# DA4LLM BRIDGE

BRIDGE will own provider-, tool-, connector-, and runtime-specific mappings, including concrete invocation behavior, substitutions, access distinctions, and deterministic missing-capability handling.

CORE defines the `CapabilityBridge` interface and calls generic capability names through `CALL_CAPABILITY`; BRIDGE will supply ecosystem-specific implementations. If no suitable BRIDGE is present, CORE emits `CAPABILITY_UNAVAILABLE`, and the calling procedure determines whether to continue or halt.

[`placeholder.json`](placeholder.json) deliberately contains no mappings or implementation claims. Historical provider-specific procedures remain review inputs and are not represented as current APIs.
