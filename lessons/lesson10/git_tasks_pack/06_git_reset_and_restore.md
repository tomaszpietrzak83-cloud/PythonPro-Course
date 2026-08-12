# Task 6 - Resetting and restoring changes

What you practice:
- removing changes from staging,
- creating another commit,
- returning to an older commit.

Commands:

```bash
cd team-project-basic
echo "# temporary note" >> app.py
git add app.py
git reset HEAD app.py
git status
```

Another change and a new commit:

```bash
echo "# final note after reset demo" >> app.py
git add app.py
git commit -m "docs: add comment after reset example"
git log --oneline
```

Return to an older commit:

```bash
git reset --hard OLDER_COMMIT_HASH
git log --oneline
```

Important note:
- `git reset --hard` removes local uncommitted changes and resets the repository exactly to the selected commit,
- do not use it on important work unless you fully understand the consequences.
