# Task 10 - Working with Git Flow

What you practice:
- `main`, `develop`, `feature`, and `release` branches,
- the lifecycle of a change in Git Flow.

If you have the `git-flow` tool installed:

```bash
mkdir git-flow-demo
cd git-flow-demo
git init
git branch -M main
git flow init
git flow feature start my-feature
```

Create a few commits on the feature branch:

```bash
echo "print('feature start')" > feature.py
git add feature.py
git commit -m "feat: add feature file"
echo "# another change" >> feature.py
git add feature.py
git commit -m "feat: extend feature file"
```

Finish the feature:

```bash
git flow feature finish my-feature
```

Release:

```bash
git flow release start 1.0.0
echo "# release note" > RELEASE.txt
git add RELEASE.txt
git commit -m "docs: add release note"
git flow release finish 1.0.0
```

If you do not have `git-flow`:
- simulate it manually with `git checkout -b develop`,
- then `git checkout -b feature/...`,
- and finally a normal `git merge`.
