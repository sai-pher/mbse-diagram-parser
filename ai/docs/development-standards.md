# Development Standards: C.O.L.D (+S)

**Version:** 1.0 | **Status:** Mandatory

---

## Framework

| Principle | Focus |
|-----------|-------|
| **C** — Clean | Single responsibility, self-documenting names |
| **O** — Orthogonal | Independent components, injected dependencies |
| **L** — Lean | Minimal transformations, no dead code |
| **D** — Data-Driven | Explicit types, no NULLs, validated at boundaries |
| **S** — Side Effects | Pure functions isolated, I/O explicit |

---

## C — Clean Code

- One responsibility per function/class
- Names explain intent (verb phrases for functions, nouns for classes)
- No abbreviations, no generic names (`Manager`, `Helper`, `data`, `flag`)
- Comments explain **WHY**, never WHAT
- No commented-out code in version control

**Hard limits:**
- Max 20 lines per function
- Cyclomatic complexity < 10
- Max 4 parameters (use a dataclass/object for more)

---

## O — Orthogonal

- Dependencies always injected via `__init__`, never instantiated internally
- Interfaces are minimal and focused — one concern per interface
- A change to one component must not require changes to unrelated components
- Use `Protocol` or `ABC` for interface contracts

---

## L — Lean

- Prefer a single efficient query over multiple queries + transformations
- Extract complex blocks into named methods
- No unused code, no speculative features
- Minimise intermediate variables where clarity is not sacrificed

---

## D — Data-Driven

- No `None` / `NULL` returns — use empty objects, `Optional` explicitly, or `Result` types
- All function parameters and return types annotated
- Validate all external inputs at system boundaries
- Use `@dataclass` or `TypedDict` for data contracts

**Result pattern (standard for failable operations):**
```python
@dataclass
class Result:
    success: bool
    value: Any = None
    errors: List[str] = field(default_factory=list)

    @classmethod
    def ok(cls, value): return cls(success=True, value=value)

    @classmethod
    def fail(cls, errors): return cls(success=False, errors=errors)
```

---

## S — Side Effects

- Pure functions (no I/O, no mutation) are the default
- Functions with side effects (DB, file, network) are explicit and isolated
- Never mutate input parameters
- Side-effectful operations are composed at the service/orchestration layer only

---

## Standard Patterns

### Service Composition
```python
class SomeService:
    def __init__(self, repository: Repo, validator: Validator):
        self._repository = repository
        self._validator = validator

    def do_thing(self, request: Request) -> Result:
        validation = self._validator.validate(request)
        if not validation.success:
            return Result.fail(validation.errors)
        entity = self._build_entity(request)          # pure
        saved = self._repository.save(entity)          # impure, explicit
        return Result.ok(saved)

    def _build_entity(self, request: Request) -> Entity:  # pure helper
        ...
```

### Transformation Pipeline
```python
def process(raw: RawData) -> Output:
    cleaned   = clean(raw)
    validated = validate(cleaned)
    enriched  = enrich(validated)
    return format_output(enriched)
```

---

## Enforcement

**Automated (CI must pass):**
- `ruff` — linting and naming
- `black` — formatting
- `mypy` or `pyright` — type coverage
- `pytest --cov` — minimum 80% coverage on business logic
- Complexity check — cyclomatic complexity < 10

**PR requirements:**
- C.O.L.D compliance verified by reviewer
- All automated checks pass
- Tests included for new functionality

**Exceptions:** Require written justification, tech lead approval, and a TODO with a tracking ticket.
