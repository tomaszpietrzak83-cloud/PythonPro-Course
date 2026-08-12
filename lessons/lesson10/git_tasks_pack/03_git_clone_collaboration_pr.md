# Task 3 - Cloning and collaboration

What you practice:
- `git clone`,
- a new working branch,
- pushing to a remote repository,
- creating a Pull Request.

Commands:

```bash
git clone YOUR_REPO_URL
cd REPOSITORY_NAME
echo "Tomek Pietrzak" > contributors.txt
git checkout -b feature-contributors
git add contributors.txt
git commit -m "docs: add contributor list"
git push -u origin feature-contributors
```

What to do next on GitHub:
- open the repository in your browser,
- create a Pull Request from `feature-contributors` to `main`,
- explain in the PR description that you added `contributors.txt` with your name.

How it works:
- `git clone` downloads the repository locally,
- `git push -u origin ...` pushes the branch and sets the upstream tracking branch,
- a Pull Request is used to present changes before merging.
