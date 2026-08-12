# Task 4 - Basic project configuration

What you practice:
- creating a new repository,
- local configuration of `user.name` and `user.email`.

Commands:

```bash
mkdir team-project-basic
cd team-project-basic
git init
git branch -M main
git config user.name "Tomek Pietrzak"
git config user.email "your.email@example.com"
git config --list --local
```

How it works:
- `git config ... --local` stores the values only for this repository,
- `git config --list --local` lets you confirm that the settings were saved correctly.
