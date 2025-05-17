# Talk-with-database

# Steps to commit

- Checkout to your branch  
```bash
git checkout <branch-name>
```

- Pull the branch before doing any changes  
```bash
git pull
```

- Make the changes then create a PR  
```bash
git add .
git commit -m "Your meaningful commit message"
git push origin <branch-name>
```

- Create a pull request (PR) on GitHub:
  1. Go to your repository on GitHub.
  2. Click the **"Compare & pull request"** button that appears after your push.
  3. Fill in the PR title and description.
  4. Select the base branch (e.g., `main`) and compare it with your feature branch.
  5. Click **"Create pull request"**.

> 💡 Alternatively, if you're using the GitHub CLI(But recommended to do it in the first way):
```bash
gh pr create --base main --head <branch-name> --title "Your PR title" --body "Description of your changes"
```
