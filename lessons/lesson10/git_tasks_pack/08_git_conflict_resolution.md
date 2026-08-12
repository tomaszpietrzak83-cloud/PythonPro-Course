# Task 8 - Resolving Git conflicts

What you practice:
- creating a conflict on purpose,
- resolving it manually,
- finishing the merge with a final commit.

Commands:

```bash
mkdir git-conflict-demo
cd git-conflict-demo
git init
git branch -M main
echo "Line 1 - main version" > conflict_example.txt
git add conflict_example.txt
git commit -m "feat: add first line"
```

Branch A:

```bash
git checkout -b branch-A
echo "Line 1 - main version" > conflict_example.txt
echo "Line 2 - from branch-A" >> conflict_example.txt
git add conflict_example.txt
git commit -m "feat: add second line in branch-A"
```

Return to `main` and make a different change:

```bash
git checkout main
echo "Line 1 - changed in main" > conflict_example.txt
echo "Line 2 - from main" >> conflict_example.txt
git add conflict_example.txt
git commit -m "fix: update first line and add second line in main"
```

Trigger the conflict:

```bash
git merge branch-A
```

After the conflict:
- open `conflict_example.txt`,
- keep the final version you want,
- remove the conflict markers,
- then run:

```bash
git add conflict_example.txt
git commit
```
