# Task 7 - Rebase and interactive history editing

What you practice:
- several small commits on one branch,
- `git rebase -i`,
- combining commits into one.

Commands:

```bash
cd team-project-basic
git checkout -b feature-branch
echo "# line 1" >> app.py
git add app.py
git commit -m "feat: add first small change"

echo "# line 2" >> app.py
git add app.py
git commit -m "feat: add second small change"

echo "# line 3" >> app.py
git add app.py
git commit -m "feat: add third small change"
```

Interactive rebase:

```bash
git rebase -i HEAD~3
```

What to do in the editor:
- leave the first commit as `pick`,
- change the next two from `pick` to `squash` or `fixup`,
- save the file and close the editor,
- then set the final commit message, for example:

```text
feat: combine feature branch changes
```

If you need to push rewritten history:

```bash
git push --force
```

Important note:
- `git push --force` rewrites history on the remote repository,
- use it only when you understand the consequences.
