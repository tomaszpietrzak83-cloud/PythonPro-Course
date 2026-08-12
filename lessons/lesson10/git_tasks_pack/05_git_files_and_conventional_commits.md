# Task 5 - Working with files and commits

What you practice:
- creating and modifying a file,
- `git status`,
- Conventional Commits.

Commands:

```bash
cd team-project-basic
echo "def helloWorld():" > app.py
echo "    return 'Hello, world!'" >> app.py
git add app.py
git commit -m "feat: add hello world function"
```

Modify the file and create a second commit:

```bash
echo "def helloWorld():" > app.py
echo "    return 'Hello from the updated app!'" >> app.py
git status
git add app.py
git commit -m "fix: update hello world message"
git log --oneline
```

How it works:
- `feat:` means a new feature,
- `fix:` means a bug fix or correction,
- `git status` shows what changed and whether it is already staged.
