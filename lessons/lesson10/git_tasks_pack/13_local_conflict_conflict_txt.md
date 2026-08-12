# Extra task - conflict.txt and manual conflict resolution

What you practice:
- a second, separate conflict scenario,
- merging and manually combining file contents.

Commands:

```bash
mkdir conflict-demo
cd conflict-demo
git init
git branch -M main
echo "First line of text." > conflict.txt
git add conflict.txt
git commit -m "feat: add initial text"
```

Branch A:

```bash
git checkout -b branch-A
echo "First line of text." > conflict.txt
echo "Line added in branch-A." >> conflict.txt
git add conflict.txt
git commit -m "feat: add line from branch-A"
```

Main:

```bash
git checkout main
echo "First line of text." > conflict.txt
echo "Line added in main." >> conflict.txt
git add conflict.txt
git commit -m "feat: add line from main"
git merge branch-A
```

After the conflict, edit the final file so it keeps both added lines, then run:

```bash
git add conflict.txt
git commit -m "merge: resolve conflict in conflict.txt"
```

Important note:
- the conflict appears because both branches changed the same area of the file,
- Git does not guess which version should win, so it requires a manual decision.
