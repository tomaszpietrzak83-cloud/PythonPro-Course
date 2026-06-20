# Task 9 - Advanced use of Conventional Commits

What you practice:
- proper commit types,
- optional scopes,
- optional commit body text.

Example commits:

```bash
git commit -m "feat(auth): add login entry point"
git commit -m "fix(ui): center gallery table"
git commit -m "docs: describe project idea"
git commit -m "style: reformat example commands"
```

Example of a commit with a body:

```bash
git commit -m "feat(products): add registration persistence" -m "The change stores new entries in SQLite so the registration form has a real backend flow instead of a temporary in-memory result."
```

How it works:
- `feat` = new feature,
- `fix` = fix or correction,
- `docs` = documentation change,
- `style` = formatting or style-only change,
- `(scope)` helps show which area the commit affects,
- the body explains why the change was introduced.
