# Capstone setup (one time)

**Capstone index:** [Capstone plan](README.md) &nbsp;·&nbsp; **Next:** [Guide 1, Problem 1](guide/01-accessing-claude-with-the-api.md#problem-1-make-your-first-api-call)

Do this once, before guide 1. **Mac** commands run in the Terminal app. **Windows** commands run in PowerShell. Commands with no label work on both.

**Done when:** `uv --version` prints a version, `.env` holds your key, and `.env` never shows in `git status`.

---

**Step 1. Check that Git is installed.** Git saves versions of your work. Run:

```bash
git --version
```

If it prints a version, such as `git version 2.46.0`, go to step 2. If it says `command not found` (Mac) or `not recognized` (Windows), open the panel below.

<details>
<summary>Git is missing: how to install it</summary>

- **Mac:** a window appears offering to install Apple's free *Command Line Tools*, which include Git. Click **Install**, then run `git --version` again.
- **Windows:** download and install Git from [git-scm.com](https://git-scm.com/downloads). Close and reopen PowerShell, then run `git --version` again.

</details>

**Step 2. Check that uv is installed.** uv installs Python and the project's packages, and runs your code. Run:

```bash
uv --version
```

If it prints a version, such as `uv 0.9.5`, go to step 3. If it says `command not found` or `not recognized`, open the panel below.

<details>
<summary>uv is missing: how to install it</summary>

Run the command for your computer. It downloads uv's official installer and runs it.

**Mac:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen the terminal, then run `uv --version` again.

</details>

**Step 3. Go to the capstone folder.** Every later command runs there.

**Mac:**

```bash
cd ~/Documents/ClaudeArchitectStudyGuide/02_BuildingWithTheClaudeAPI/00_Capstone_Plan
```

**Windows:**

```powershell
cd $HOME\Documents\ClaudeArchitectStudyGuide\02_BuildingWithTheClaudeAPI\00_Capstone_Plan
```

If your study-notes folder is somewhere else, use that path instead.

**Step 4. Make the folder a Python project and install the packages.** uv is a helper that sets up a Python project for you, like a kitchen assistant: you name the recipe, and it brings the right oven and ingredients. It gets the right Python and add-on packages and keeps them inside this one project, so nothing else on your computer breaks.

```bash
uv init --name claude-capstone --python 3.12 --no-readme
uv add anthropic python-dotenv
uv add --dev pytest
rm main.py
```

| Command | In plain words |
|---|---|
| `uv init --name claude-capstone --python 3.12 --no-readme` | "Make this folder a Python project called claude-capstone, using Python 3.12. Don't create a README file, because this folder already has one." |
| `uv add anthropic python-dotenv` | "Install two add-ons. `anthropic` lets my code talk to Claude. `python-dotenv` reads my secret key from the `.env` file." |
| `uv add --dev pytest` | "Install `pytest`, a tool that tests my code. I only need it while building." |
| `rm main.py` | "Delete the sample file uv made. I don't need it." |

**Step 5. Create the code folders.**

**Mac:**

```bash
mkdir app experiments
touch app/__init__.py experiments/__init__.py
```

**Windows:**

```powershell
New-Item -ItemType Directory app, experiments
New-Item app\__init__.py, experiments\__init__.py
```

`app/` holds the app's code, and `experiments/` holds practice scripts. The empty `__init__.py` file lets one file import code from another, such as `from app.client import ask`. Later guides create the other folders when they need them.

**Step 6. Keep your key and packages out of Git.** `.gitignore` is a list of files that Git never saves.

**Mac:**

```bash
printf ".env\n.venv\n" >> .gitignore
```

**Windows:**

```powershell
Add-Content .gitignore ".env", ".venv"
```

This adds two lines to `.gitignore`. `.env` will hold your secret key. `.venv` is the folder where uv keeps the installed packages.

**Step 7. Save your API key in `.env`.** Open the file in a text editor.

**Mac:**

```bash
nano .env
```

**Windows:**

```powershell
notepad .env
```

Type these two lines, with your own key from the Claude Console. In nano, save with Ctrl+O, then Return, then Ctrl+X. In Notepad, save with Ctrl+S and close it.

```text
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
CLAUDE_MODEL=claude-haiku-5-5
```

**Step 8. Check that Git ignores your key.**

```bash
git status
```

**Warning:** if `.env` or `.venv` appears in the list, stop and fix `.gitignore`. Git keeps every old version, so a key committed once would still be readable on GitHub if you push later, even after you delete the file.

Setup is done. Go to [guide 1, Problem 1](guide/01-accessing-claude-with-the-api.md#problem-1-make-your-first-api-call).
