# DA4LLM TESTS

TESTS contains the initial executable conformance suite and will also hold future golden traces, package-boundary tests, and regression cases.

The current suite covers lexical defaults, semantic type precedence, normal/debug/strict modes, partial and absent semantics, the semantic/control-flow boundary, missing-BRIDGE continue and halt behavior, a provider-neutral test bridge, and optional GOVERNANCE hook ordering.

Run it from the repository root:

```sh
python3 -m unittest discover -s DA4LLM/TESTS -v
```

Future test registration does not promote domain logic into CORE. JobEval remains outside this POC.
