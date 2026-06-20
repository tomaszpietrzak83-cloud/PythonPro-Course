# Task 2 - Working with branches

What you practice:
- creating branches,
- switching between branches,
- committing on a branch,
- merging into `main`.

Commands:

```bash
cd git-task-01
git checkout -b feature-login
echo "print('login feature')" > login.py
git add login.py
git commit -m "feat: add login entry file"
git checkout main
git merge feature-login
git log --oneline --graph --all
```

How it works:
- `git checkout -b feature-login` creates a new branch and switches to it immediately,
- a commit on that branch saves changes only in that branch,
- `git merge feature-login` merges the completed work into `main`,
- `git log --graph --all` helps you see branches and merge history.

If a conflict appears:
- open the conflicted file,
- keep the correct final content,
- remove the conflict markers `<<<<<<<`, `=======`, `>>>>>>>`,
- then run:

```bash
git add FILE_NAME
git commit
```
