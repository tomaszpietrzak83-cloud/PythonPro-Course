# Task 1 - Repository initialization and first commit

What you practice:
- `git init`
- `git add`
- `git commit`
- `git log`

Commands:

```bash
mkdir git-task-01
cd git-task-01
git init
git branch -M main
echo "# Git Task 01" > README.md
git add README.md
git commit -m "docs: add initial project readme"
git log --oneline
```

How it works:
- `git init` creates a new local repository,
- `git branch -M main` sets the main branch name to `main`,
- `git add` places the file in the staging area,
- `git commit` saves a version of the changes in history,
- `git log --oneline` shows a short commit history.
