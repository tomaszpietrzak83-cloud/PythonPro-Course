# Project preparation - remote repository and basic structure

What you practice:
- creating a repository on GitHub or GitLab,
- adding basic project files,
- starting a simple folder structure.

Local commands after creating the remote repository:

```bash
git clone YOUR_REPO_URL
cd PROJECT_NAME
mkdir src tests docs
echo "# Project" > README.md
echo "__pycache__/" > .gitignore
echo ".venv/" >> .gitignore
echo "*.pyc" >> .gitignore
git add README.md .gitignore
git commit -m "docs: add initial project files"
```

If you want a `develop` branch immediately:

```bash
git checkout -b develop
git push -u origin develop
```

On the remote platform:
- configure branch protection for `main`,
- if available, require reviews and passing tests.
