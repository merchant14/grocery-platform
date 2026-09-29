---
name: django
description: "Use when working on this Django repository and follow its required task-based Git branch workflow."
---

## Git & Branch Workflow

The repository follows a task-based branch workflow.

Before making any code changes for a task, developers and AI coding agents MUST synchronize with the latest `main` branch and create a dedicated task branch.

### Required Workflow

For every new task:

#### 1. Check current Git status

```text
git status
```

Do not blindly discard existing local changes.

If there are uncommitted changes, determine whether they belong to the current task before proceeding.

#### 2. Switch to main

```text
git checkout main
```

If the repository uses `git switch`, this is also acceptable:

```text
git switch main
```

#### 3. Pull the latest main

```text
git pull origin main
```

The task must start from the latest available `main` branch unless there is an explicitly documented reason not to.

#### 4. Create a task branch

Create a branch using:

```text
<task-id>/<short-description>
```

Examples:

```text
DEV-340576/use-cluster-based-report-path
DEV-123456/add-merchant-product
```

Branch naming rules:

- Use the actual task/JIRA ID.
- Use lowercase for the description.
- Use hyphens between words.
- Keep the description concise.
- Do not use spaces.
- Do not use generic names such as `feature`, `test`, `changes`, or `work`.
- Do not work directly on `main`.

Create the branch with either command:

```text
git checkout -b DEV-123456/add-merchant-product
```

```text
git switch -c DEV-123456/add-merchant-product
```

## Development After Branch Creation

Only after the task branch has been created should implementation begin.

The normal flow is:

```text
main
  ↓
git pull origin main
  ↓
create task branch
  ↓
implement task
  ↓
run tests/checks
  ↓
review changes
  ↓
commit
  ↓
push task branch
  ↓
create Pull Request
  ↓
code review
  ↓
merge into main
```

## Before Starting Development

AI agents must verify:

```text
git status
git branch --show-current
git log -1 --oneline
```

The agent should confirm that:

1. The working tree is understood.
2. The task branch is based on the latest `main`.
3. The agent is not accidentally working directly on `main`.
4. The branch name follows the task-ID convention.

## Existing Local Changes

If `git status` shows changes before starting a task, do not automatically run:

```text
git reset --hard
git clean -fd
git checkout .
```

These commands can destroy developer work. Instead:

1. Inspect the changes.
2. Determine whether they belong to the current task.
3. If they belong to another task, stop and ask the developer how they should be handled.
4. If they belong to the current task, continue carefully.
5. Never discard another developer's work without explicit approval.

## Working on an Existing Task Branch

If the requested task branch already exists, do not automatically create another branch. First inspect:

```text
git branch
git status
```

If the branch corresponds to the requested task, continue on that branch after confirming its state.

If the branch is behind `main`, do not automatically rewrite history. Determine the appropriate synchronization strategy and follow the team's approved Git workflow.

## Commits

Commits should be small, logically grouped, related to the current task, descriptive, and free of unrelated changes.

Do not commit `.env` files, secrets, credentials, debug files, temporary files, or unrelated modifications.

Example:

```text
git add <relevant-files>
git commit -m "DEV-123456: add merchant product model"
```

Use the actual task ID in the commit message when the repository's task-tracking convention requires it.

## Push

Push the task branch rather than `main`:

```text
git push -u origin DEV-123456/add-merchant-product
```

Do not push development work directly to `main` unless explicitly authorized.

## Pull Requests

Deliver completed work through a Pull Request. The PR should contain:

- Task ID.
- Short description of the change.
- Relevant implementation details.
- Tests performed.
- Migration information if applicable.
- Known limitations or follow-up work.

The PR should target `main` unless the repository explicitly defines another integration branch.

## AI Agent Safety Rules

AI coding agents MUST NOT:

- Work directly on `main`.
- Create random branch names.
- Push directly to `main`.
- Delete branches without authorization.
- Force-push without explicit authorization.
- Reset or discard uncommitted developer changes.
- Use `git reset --hard` to solve an unknown problem.
- Use `git clean -fd` without explicit authorization.
- Rewrite Git history without explicit authorization.
- Commit unrelated changes.
- Modify another developer's work without understanding it.

Before destructive Git operations, ask for explicit approval.

## Task Branch Naming Examples

Valid:

```text
DEV-123456/add-merchant-product
DEV-234567/update-order-status
DEV-345678/add-shop-analytics
DEV-456789/fix-inventory-validation
```

Invalid:

```text
feature-branch
my-branch
test
changes
dev
new-feature
```

## Mandatory Rule

For a new development task, the default sequence is:

```text
git status
git checkout main
git pull origin main
git checkout -b <task-id>/<description>
```

Only then begin implementation.

If the repository's `AGENTS.md` or documented Git workflow specifies a more specific procedure, follow the documented project workflow.

Do not silently skip branch creation or synchronization because the task appears small.