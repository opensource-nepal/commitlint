# Conventional Commits

A conventional commit message follows a specific format that includes a prefix indicating the type of change, an optional scope for context, and a concise description of the modification.
This structure improves readability, facilitates automated changelog generation, and ensures a consistent commit history.

The commit message should follow this structure:

```
<type>(<optional scope>): <description>

[Optional body]
```

**Type:** Indicates the type of change, such as build, ci, docs, feat, fix, perf, refactor, style, test, chore, revert, or bump.
E.g., `feat: add JSON parser`.

**Scope:** Additional contextual information.
E.g., `feat(parser): add JSON parser`.

**Description:** Brief description of the commit.

**Body:** A detailed description of the commit.

For more details, please refer to the Conventional Commits specification at https://www.conventionalcommits.org/en/v1.0.0/

> NOTE: commitlint also checks the length of the commit header (**max 72 characters**). The commit header refers to the first line of the commit message (excluding the body).
