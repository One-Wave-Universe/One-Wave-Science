"""Query-time answer generation from the active field.

This is the module that enforces the core rule in the running code, not
just in the schema: `query_concept` NEVER merges definitions or relations
from different fields into one asserted answer. With `active_field` set,
only that field's claims are returned. Without it, results are grouped by
field and each group keeps its own epistemic status -- the caller (or the
deterministic renderer below) is responsible for presenting them as
separate, clearly-labeled interpretations, never as a single flattened
truth.

No LLM here by design (brief section 24): `render_answer` is plain
deterministic templating. An LLM, if ever added, sits above this module
and verbalizes its structured output -- it does not replace it.
"""

from __future__ import annotations

from dataclasses import dataclass, field as dc_field

from onewave.concepts import (
    Concept,
    DefinitionRecord,
    get_concept,
    get_current_definitions,
    get_definition_history,
    find_concept,
)
from onewave.epistemic import EpistemicStatus
from onewave.events import PathEvent
from onewave.fields import Field, get_field as get_field_record
from onewave.relations import Relation, get_relations
from onewave.storage.sqlite import Storage


def _resolve_concept(db: Storage, concept: str | Concept) -> Concept | None:
    if isinstance(concept, Concept):
        return concept
    resolved = get_concept(db, concept)
    if resolved is not None:
        return resolved
    return find_concept(db, concept)


def _normalize_status_filter(
    epistemic_filter: EpistemicStatus | str | list | tuple | set | None,
) -> set[EpistemicStatus] | None:
    if epistemic_filter is None:
        return None
    if isinstance(epistemic_filter, (EpistemicStatus, str)):
        epistemic_filter = [epistemic_filter]
    return {EpistemicStatus(s) for s in epistemic_filter}


@dataclass(frozen=True)
class FieldAnswer:
    field_id: str
    field_name: str
    definitions: tuple[DefinitionRecord, ...] = ()
    relations: tuple[Relation, ...] = ()


@dataclass(frozen=True)
class QueryResult:
    concept: Concept
    active_field: str | None
    answers: tuple[FieldAnswer, ...] = ()
    history: dict = dc_field(default_factory=dict)  # definition_id -> revisions


def query_concept(
    db: Storage,
    concept: str | Concept,
    active_field: str | None = None,
    include_relations: bool = True,
    include_history: bool = False,
    epistemic_filter: EpistemicStatus | str | list | tuple | set | None = None,
) -> QueryResult:
    resolved = _resolve_concept(db, concept)
    if resolved is None:
        raise ValueError(f"unknown concept: {concept!r}")

    status_filter = _normalize_status_filter(epistemic_filter)

    definitions = get_current_definitions(db, resolved.concept_id, field_id=active_field)
    if status_filter is not None:
        definitions = [d for d in definitions if d.epistemic_status in status_filter]

    by_field: dict[str, list[DefinitionRecord]] = {}
    for d in definitions:
        by_field.setdefault(d.field_id, []).append(d)

    field_ids = set(by_field)
    if active_field is not None:
        field_ids.add(active_field)
    elif include_relations:
        for r in get_relations(db, resolved.concept_id):
            field_ids.add(r.field_id)

    answers = []
    for field_id in sorted(field_ids):
        field_record: Field | None = get_field_record(db, field_id)
        field_name = field_record.name if field_record else field_id
        relations: tuple[Relation, ...] = ()
        if include_relations:
            relations = tuple(get_relations(db, resolved.concept_id, field_id=field_id))
        answers.append(
            FieldAnswer(
                field_id=field_id,
                field_name=field_name,
                definitions=tuple(by_field.get(field_id, ())),
                relations=relations,
            )
        )

    history: dict[str, list[DefinitionRecord]] = {}
    if include_history:
        for d in definitions:
            history[d.definition_id] = get_definition_history(db, d.definition_id)

    return QueryResult(
        concept=resolved,
        active_field=active_field,
        answers=tuple(answers),
        history=history,
    )


def render_answer(result: QueryResult) -> str:
    """Deterministic, template-based rendering of a QueryResult.

    Groups strictly by field; never states one field's claim as if it
    were another's. See module docstring.
    """
    lines: list[str] = [f"Concept: {result.concept.canonical_name}"]
    if result.concept.aliases:
        lines.append(f"Aliases: {', '.join(result.concept.aliases)}")

    if not result.answers or all(not a.definitions and not a.relations for a in result.answers):
        scope = f" in field '{result.active_field}'" if result.active_field else ""
        lines.append(f"(No stored interpretations{scope}.)")
        return "\n".join(lines)

    for answer in result.answers:
        if not answer.definitions and not answer.relations:
            continue
        lines.append("")
        lines.append(f"Field: {answer.field_name} ({answer.field_id})")
        if not answer.definitions:
            lines.append("  (no definition on record in this field)")
        for d in answer.definitions:
            lines.append(f"  Status: {d.epistemic_status.value}")
            lines.append(f"  Definition: {d.text}")
            if d.confidence is not None:
                lines.append(f"  Confidence: {d.confidence}")
            if d.source:
                lines.append(f"  Source: {d.source}")
        if answer.relations:
            lines.append("  Relations:")
            for r in answer.relations:
                arrow = "->" if r.source_concept_id == result.concept.concept_id else "<-"
                other = r.target_concept_id if arrow == "->" else r.source_concept_id
                lines.append(
                    f"    {arrow} {r.relation_type.value} {other} "
                    f"[{r.epistemic_status.value}"
                    + (f", weight={r.weight}" if r.weight is not None else "")
                    + "]"
                )
        if result.history:
            for d in answer.definitions:
                revisions = result.history.get(d.definition_id, [])
                if len(revisions) > 1:
                    lines.append(f"  History ({len(revisions)} revisions):")
                    for rev in revisions:
                        lines.append(
                            f"    rev {rev.revision}: [{rev.epistemic_status.value}] {rev.text}"
                        )

    return "\n".join(lines)


def render_path(events: list[PathEvent]) -> str:
    """Deterministic rendering of an event history, e.g. for answering
    "show the path that caused this runtime record to enter RETURN"."""
    if not events:
        return "(no events)"
    lines = [f"Path ({len(events)} events):"]
    for e in events:
        if e.kind == "genesis":
            lines.append(f"  [{e.seq}] genesis -> field={e.resulting_field.name}")
            continue
        lines.append(
            f"  [{e.seq}] A={e.a.name} B={e.b.name} -> gate={e.gate_result.name} "
            f"field {e.previous_field.name}->{e.resulting_field.name} "
            f"disp {e.previous_displacement:g}->{e.resulting_displacement:g} "
            f"mem {e.previous_memory:g}->{e.resulting_memory:g}"
        )
        if e.causal_parents:
            lines.append(f"       causal_parents={list(e.causal_parents)}")
    return "\n".join(lines)
