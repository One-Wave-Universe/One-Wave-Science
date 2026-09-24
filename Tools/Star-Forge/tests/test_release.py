import os, tempfile
os.environ["XDG_DATA_HOME"] = tempfile.mkdtemp()

from star_forge.state import (
    add_plan_step, assign_pair, load_state, mediator_continue,
    record_validation_evidence, resolve_active, set_step_scope,
    set_usefulness, upsert_toc_entry,
)

s=load_state()
s["project"]["goal"]="Build useful, simple, verified programs"
step=add_plan_step(s,"Build smallest program","Create one bounded program and test it",2)
set_step_scope(
    s, step["id"],
    branch_scope="field/first-program",
    allowed_files=["src/hello.py","tests/test_hello.py"],
    protected_files=["PROJECT_PLAN.md"],
    validation_stage="CONCEPT",
)
upsert_toc_entry(
    s,"first-program","First Program","software",
    path="src/hello.py",layer=2,branch="field/first-program",
    program="python",tests=["tests/test_hello.py"],
    validation_stage="CONCEPT",purpose="Prove Star Forge build loop"
)
a=assign_pair(s,"Field AI","Void AI")
assert a["branch"]=="field/first-program"
assert a["allowed_files"]==["src/hello.py","tests/test_hello.py"]

blocked=False
try:
    resolve_active(s,"ALLOW","")
except ValueError:
    blocked=True
assert blocked

resolve_active(s,"ALLOW","Field test PASS; Void independently checked diff and result.")
assert s["project"]["status"]=="COMPLETE"

record_validation_evidence(s,"CIRCUIT_SIMULATION","Simulator passed",source="future-ngspice")
set_usefulness(
    s,problem="Need reliable program building",
    expected_user_value="Programs built with less drift",
    simplest_usable_outcome="One tested program per bounded branch",
    observed_value="Loop completed with independent check",
    status="USEFUL",
)
assert s["validation"]["usefulness"]["status"]=="USEFUL"
assert s["toc"][0]["protected"] is False
print("STAR_FORGE_RELEASE_TEST_PASS")
