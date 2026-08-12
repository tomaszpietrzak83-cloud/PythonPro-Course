# Git Cheat Pack

Compact reference for the most common Git commands.

## Repository Setup

```bash
git init
# Create a new local repository in the current folder.
# Use it once in the project root.
```

```bash
git clone YOUR_REPO_URL
# Download an existing remote repository to your computer.
# Use this when the project already exists on GitHub, GitLab, or Bitbucket.
```

```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
# Set the author identity used in commits.
# Add --local if you want these values only in one repository.
```

## Daily Work

```bash
git status
# Show what changed, what is staged, and what is still untracked.
# Run this often. It is one of the safest and most useful Git commands.
```

```bash
git add FILE_NAME
git add .
# Move changes into the staging area before a commit.
# Prefer git add FILE_NAME when learning, because it is more precise.
```

```bash
git commit -m "feat: add login form"
# Save staged changes as one meaningful history step.
# Common prefixes: feat, fix, docs, style, refactor, test, chore.
```

```bash
git log --oneline
# Show a short commit history.
# This is easier to read than the full default log while practicing.
```

## Branching

```bash
git branch
# List local branches.
```

```bash
git checkout -b feature-login
# Create a new branch and switch to it immediately.
# Feature branches are good for isolated work.
```

```bash
git checkout main
# Switch back to the main branch.
```

```bash
git merge feature-login
# Merge completed work from another branch into the current branch.
# Before merge, make sure you are on the branch that should receive changes.
```

## Remote Work

```bash
git remote -v
# Show connected remote repositories.
```

```bash
git push -u origin feature-login
# Push a local branch to the remote repository.
# -u sets the upstream branch, so future pushes can be shorter.
```

```bash
git pull origin main
# Download and merge the latest changes from the remote branch.
# Pull before new work if other people also change the repository.
```

## Inspecting Changes

```bash
git diff
# Show unstaged changes.
```

```bash
git diff --staged
# Show what is already staged for the next commit.
```

```bash
git show COMMIT_HASH
# Inspect one specific commit in detail.
```

```bash
git log --oneline --graph --all
# Visualize branches, merges, and commit flow.
```

## Undoing and Restoring

```bash
git reset HEAD FILE_NAME
# Remove a file from staging without deleting working-directory changes.
# Use this when you staged something by mistake.
```

```bash
git restore FILE_NAME
# Discard working-directory changes in a file.
# Warning: this removes local uncommitted edits in that file.
```

```bash
git reset --hard COMMIT_HASH
# Reset the repository exactly to an older commit.
# Warning: this is destructive and also removes local uncommitted changes.
```

## Rebasing

```bash
git rebase main
# Replay your current branch on top of the latest main.
# Use this when you want cleaner history than a merge-based flow.
```

```bash
git rebase -i HEAD~3
# Interactively edit the last 3 commits.
# Use it to squash, reorder, rename, or clean up history before pushing.
```

## Conflict Resolution

```bash
git merge branch-A
# Start a merge that may produce a conflict if both branches changed the same area.
```

```bash
git add FILE_NAME
git commit
# Use these after manually resolving a merge conflict in the file.
# First remove conflict markers and keep the final content you want.
```

## Force Push

```bash
git push --force
# Push rewritten history to the remote repository.
# Warning: this overwrites remote history and can hurt collaborators.
```

```bash
git push --force-with-lease
# Safer version of force push.
# It checks whether someone else pushed in the meantime.
```

## Stash

```bash
git stash
# Temporarily store local changes without committing them.
# Useful when you need to switch branches quickly.
```

```bash
git stash pop
# Restore the most recently stashed changes.
```

## Good Default Workflow

```bash
git status
git checkout -b feature-something
# edit files
git status
git add FILE_NAME
git commit -m "feat: describe your change"
git checkout main
git merge feature-something
git log --oneline --graph --all
# Safe basic workflow for many simple tasks.
```

## Safety Reminders

Use with extra care:
- `git reset --hard`
- `git push --force`
- deleting branches
- overwriting file content after conflicts

Safe commands to run often:
- `git status`
- `git log --oneline`
- `git diff`
- `git branch`
