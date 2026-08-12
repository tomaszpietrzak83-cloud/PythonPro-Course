# Extra task - project.md, branch, PR, and branch cleanup

What you practice:
- a documentation branch,
- push,
- Pull Request,
- merge,
- deleting branches.

Commands:

```bash
git clone YOUR_REPO_URL
cd PROJECT_NAME
echo "# Project idea" > projekt.md
echo "A simple task management application." >> projekt.md
git checkout -b feature-readme
git add projekt.md
git commit -m "docs: add project idea description"
git push -u origin feature-readme
```

After creating the Pull Request and merging it:

```bash
git checkout main
git pull origin main
git branch -d feature-readme
git push origin --delete feature-readme
```

How it works:
- `git branch -d` deletes the local branch,
- `git push origin --delete ...` deletes the remote branch.
