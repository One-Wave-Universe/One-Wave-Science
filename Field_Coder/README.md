# Field Coder — Project Control Index

This directory governs the **Field-side coding agent project only**.

Void is a separate future project. Do not merge Void responsibilities into this build.

## Mandatory read order before every coding pass

1. `BUILD_SCOPE.md`
2. `CORE_RULES.md`
3. `BUILD_STEPS.md`
4. `PROGRESS.md`
5. latest entry in `BUILD_DIARY.md`
6. the active step section in `BUILD_STEPS.md`

No code change may begin until this read order is complete.

## Mandatory write order after every coding pass

1. record the exact test/result
2. update `BUILD_DIARY.md`
3. update `PROGRESS.md`
4. stop if the active step's hard-stop condition has been reached

The full ruleset carries forward automatically to every Field Coder branch and every later step.