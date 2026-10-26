# Lesson 3 — Installing Claude Code

**Course:** [Claude Code 101](https://academy.claude.com/courses/claude-code-101) &nbsp;·&nbsp; **Chapter 2:** Your first prompt &nbsp;·&nbsp; **Completed:** October 17, 2026

| Previous | Course | Next |
|:---|:---:|---:|
| [← How Claude Code works](02-how-claude-code-works.md) | [📚 Course index](README.md) | [Your first prompt →](04-your-first-prompt.md) |

---

**On this page**

| # | Section |
|:---:|:---|
| 1 | [Revision summary](#revision-summary) |
| 2 | [The big picture](#the-big-picture) |
| 3 | [1. Terminal](#1-terminal) |
| 4 | [2. Visual Studio Code](#2-visual-studio-code) |
| 5 | [3. JetBrains IDEs](#3-jetbrains-ides) |
| 6 | [4. Claude Desktop](#4-claude-desktop) |
| 7 | [5. Web](#5-web) |
| 8 | [Which one should I use?](#which-one-should-i-use) |
| 9 | [Recap](#recap) |
| 10 | [My notes / practice](#my-notes--practice) |
| 11 | [FAQ](#faq) |

---

### Revision summary

#### In one sentence

You install Claude Code by pasting one command into your terminal, then you sign in with a paid Claude account, and after that you can use the same Claude Code in five places: the terminal, VS Code, JetBrains editors, the Claude Desktop app, and the web.

#### Five places to use Claude Code

You can use Claude Code in the terminal, VS Code, JetBrains editors, the Claude Desktop app (its "Code" tab), and the web at claude.ai/code. It is the same program everywhere; only the screen changes.

#### Installing Claude Code in the terminal

Paste the command for your system into the terminal and press Enter.

| Your system | Install command | Updates itself? |
|---|---|---|
| macOS, Linux, or WSL | `curl -fsSL https://claude.ai/install.sh \| bash` | Yes |
| macOS with Homebrew | `brew install --cask claude-code` | No |
| Windows PowerShell | `irm https://claude.ai/install.ps1 \| iex` | Yes |
| Windows CMD | `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd` | Yes |
| Windows with winget | `winget install Anthropic.ClaudeCode` | No |

- **Homebrew and winget installs don't update themselves.** Run `brew upgrade claude-code` or `winget upgrade Anthropic.ClaudeCode` from time to time, or you will miss features and fixes.
- **PowerShell or CMD?** PowerShell's prompt starts with `PS C:\...`; CMD's has no `PS`.
- **Check the install** with `claude --version`. If the terminal says "command not found," open a new terminal: a terminal only finds programs installed before it opened.

#### Starting Claude Code for the first time

- **To start it,** move into your project folder with `cd` (for example `cd ~/projects/my-app`) and type `claude`.
- **On the first run,** pick a color theme, then sign in with a paid Claude account (Pro, Max, or Enterprise) or an API key, a secret code where you pay per use. If your company has Claude Enterprise, choose that.
- **It can reach the start folder and everything inside it,** but nothing outside. Always start it in the project folder; started in your home folder, it could reach all your personal files.

#### Setting up the other four places

- **VS Code:** in the Extensions panel, install "Claude Code" by Anthropic with the blue check mark, which proves it is the official extension. Open it with Ctrl+Shift+P (Cmd+Shift+P on Mac) and "Claude Code: Open in New Tab," or the Claude logo.
- **JetBrains:** install the Claude Code plugin from the JetBrains Marketplace, restart, and click the Claude logo. The terminal version opens in a pane beside your code.
- **Claude Desktop:** the "Code" tab works in a folder on your computer, can change permission modes, and can run work on a remote computer in the cloud.
- **The web:** works only with code stored on GitHub. It can't open a folder on your computer.

#### Choosing where to use it

The terminal gets new features first. Use VS Code or JetBrains if you spend your day in that editor, Desktop to let Claude Code work in the background, and the web on another computer or to run several sessions at once.

#### Exam takeaways

- **A team is rolling out Claude Code.** Prefer installs that update themselves (or plan how Homebrew and winget get updated), use the company's Enterprise sign-in so usage and settings are managed centrally, and teach people to start in the project folder. (Developer Productivity & Operational Enablement)
- **A security team asks why the start folder matters.** It sets how much Claude Code can reach. Starting in the project folder limits it to what the task needs, a principle called *least privilege*. (Governance, Safety & Risk)

---

### The big picture

You can use Claude Code in five places. It's the same Claude Code underneath. What changes is the window you use it through.

| Where | What it looks like | How you get it |
|---|---|---|
| **Terminal** | A text interface in your command line | Run an install command |
| **VS Code** | A panel inside the editor | Install the extension |
| **JetBrains IDEs** | A pane inside IntelliJ, PyCharm, etc. | Install the plugin |
| **Claude Desktop** | A "Code" tab in the desktop app | Install Claude Desktop |
| **Web** | A page in your browser | Go to claude.ai/code. Nothing to install. |

The rest of this lesson walks through setting up each one, then helps you pick.

---

### 1. Terminal

The **terminal** (also called the command line) is a text window where you type commands. On Mac and Linux it's the Terminal app. On Windows it's **PowerShell** or **CMD** (Command Prompt).

#### Step 1: Install

Pick the command for your system, paste it into the terminal, and press Enter.

| Your system | Command | Auto-updates? |
|---|---|---|
| macOS, Linux, or WSL | `curl -fsSL https://claude.ai/install.sh \| bash` | ✅ Yes |
| macOS with Homebrew | `brew install --cask claude-code` | ❌ No |
| Windows PowerShell | `irm https://claude.ai/install.ps1 \| iex` | ✅ Yes |
| Windows CMD | `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd` | ✅ Yes |
| Windows with winget | `winget install Anthropic.ClaudeCode` | ❌ No |

What the terms mean:
- **WSL** (Windows Subsystem for Linux) lets you run Linux inside Windows. If you use it, follow the Linux command.
- **curl** downloads something from the internet. Here it downloads the installer and runs it.
- **Invoke-RestMethod** (`irm` for short) is PowerShell's version of the same thing.
- **Homebrew** (`brew`) and **winget** are *package managers*: apps that install other apps for you on Mac and Windows.

**Why "auto-updates" matters:** Claude Code changes often. The `curl` and PowerShell installers update it for you in the background. With Homebrew or winget you have to update it yourself, for example with `brew upgrade claude-code` or `winget upgrade Anthropic.ClaudeCode`. If you forget, you miss new features and fixes.

**Not sure if you're in PowerShell or CMD on Windows?** Look at the prompt. PowerShell shows `PS C:\...`. CMD shows `C:\...` without the `PS`.

<!-- IMAGE: Terminal showing Claude Code successfully installed via curl → images/03-terminal-install.png -->

#### Step 2: Check it worked

Run:

```bash
claude --version
```

If you see a version number, it's installed. If you see "command not found" or "not recognized," **close the terminal and open a new one**. A terminal only learns about newly installed programs when it starts, so the old window doesn't know `claude` exists yet.

#### Step 3: Start Claude Code in your project

Go to your project folder with `cd`, then run `claude`:

```bash
cd ~/projects/my-app
claude
```

The first time, it walks you through setup:
1. **Choose a color theme**, such as light or dark.
2. **Sign in.** You have two choices:
   - **A Claude account** with a paid plan: Pro, Max, or Enterprise. If your company has Claude Enterprise, pick that option, so your usage goes through your company's account and its settings.
   - **An API key**: a secret code from the Claude developer platform. You pay per use instead of a monthly plan.

<!-- IMAGE: Claude Code login method selection: subscription, API, or third-party platform → images/03-login-method.png -->

#### Important: Claude Code can see the folder you start it in

Whatever folder you run `claude` in, Claude Code can access **that folder and every folder inside it**.

For example, if you run it in `~/projects/my-app`, it can read `my-app/src`, `my-app/tests`, and so on. It can't see `~/projects/other-app`.

That's why you should **always start it inside the project folder**, not your home folder. If you run it in your home folder, it can reach all your personal files, not just your code.

---

### 2. Visual Studio Code

1. Open the **Extensions** panel (the icon made of four squares on the left side).
2. Search for **"Claude Code."**
3. Pick the one **by Anthropic with the blue verification check**. The check proves it's the official extension and not a copy made by someone else.
4. Click **Install**.
5. Restart VS Code if it asks you to.

To open Claude Code:
- Press **Ctrl+Shift+P** (Windows/Linux) or **Cmd+Shift+P** (Mac) to open the **Command Palette**, a search box for every VS Code command. Then type **"Claude Code: Open in New Tab."**
- Or click the **Claude logo** if you see it in your sidebar.

<!-- IMAGE: Claude Code extension page in VS Code marketplace → images/03-vscode-extension.png -->

The extension works very much like the terminal version, but with buttons and panels. If you prefer the plain terminal look, you can switch the extension to it in your settings.

---

### 3. JetBrains IDEs

JetBrains makes IDEs such as IntelliJ IDEA, PyCharm, and WebStorm.

1. Open the **JetBrains Marketplace** (the plugins section of your IDE).
2. Install the **Claude Code** plugin.
3. Restart the IDE.
4. Click the **Claude logo** that appears.

This opens a pane with the terminal version of Claude Code running alongside your editor. You write code on one side and talk to Claude on the other.

<!-- IMAGE: Claude Code plugin in the JetBrains Marketplace → images/03-jetbrains-plugin.png -->

---

### 4. Claude Desktop

1. Install the Claude Desktop app and sign in.
2. Click the **"Code"** tab at the top.

It looks like the normal Claude chat, but it can do more:
- **Work in a specific folder** on your computer.
- **Change permissions** (the permission modes from lesson 2).
- **Work in a cloud environment**, so the work runs on a remote computer instead of your own.

<!-- IMAGE: Claude Desktop Code view showing recent project folders → images/03-desktop-code-view.png -->

---

### 5. Web

Go to **claude.ai/code**, or click **"Code"** in the sidebar of the Claude chat app.

It works much like the desktop app, with one big limit: **it only works with GitHub repositories**. It can't open a folder on your computer. Your code has to be on GitHub.

<!-- IMAGE: Claude Code on the web at claude.ai/code with repository selection → images/03-web-repo-selection.png -->

---

### Which one should I use?

| If you want... | Use | Why |
|---|---|---|
| The newest features first | **Terminal** | New features ship here first. |
| Claude built into your code editor | **VS Code or JetBrains** | Almost the same as the terminal, but inside the editor you already use. |
| Claude working in the background while you do other things | **Desktop** | It runs on its own while you work in other apps. |
| To work from anywhere, or run several sessions at once | **Web** | Nothing to install. Works on any GitHub repo from any computer. |

Examples:
- You spend all day in VS Code → install the **VS Code extension**.
- You want Claude to fix a bug while you're in a meeting → start it in **Desktop** and check back later.
- You're on a borrowed laptop and need to change a GitHub project → use the **web**.

There's no wrong choice. Many people use more than one.

### Recap

- You can use Claude Code in the **terminal, VS Code, JetBrains, Claude Desktop, or the web**.
- **Terminal:** install with one command. `curl` and PowerShell installs auto-update. Homebrew and winget don't.
- **First run:** go to your project folder, run `claude`, pick a theme, and sign in with a Pro, Max, or Enterprise account or an API key.
- **Claude Code can access the folder you start it in, plus everything inside it.** Start it in your project folder.
- **VS Code / JetBrains:** install the official extension or plugin from Anthropic.
- **Desktop:** use the "Code" tab. **Web:** go to claude.ai/code. GitHub repos only.
- **Terminal gets features first.** Pick whichever fits how you work.

---

## My notes / practice

- [ ] Install Claude Code in the terminal and run `claude --version`.
- [ ] `cd` into a test project and run `claude`. Complete the theme and sign-in steps.
- [ ] Ask Claude Code "what files can you see?" to confirm it's limited to the project folder.
- [ ] Install the VS Code extension (check for the blue verified badge) and open it from the Command Palette.
- [ ] Open the "Code" tab in Claude Desktop, or try claude.ai/code with a GitHub repo.
- [ ] Write down which option I'll use day to day, and why.

---

## FAQ

**Q1. Where can I use Claude Code?**
In five places: the terminal, VS Code, JetBrains IDEs, the Claude Desktop app, and the web (claude.ai/code). It's the same Claude Code in each. Only the interface changes.

**Q2. How do I install Claude Code in the terminal?**
Run the install command for your system:
- **macOS, Linux, WSL:** `curl -fsSL https://claude.ai/install.sh | bash`
- **Windows PowerShell:** `irm https://claude.ai/install.ps1 | iex`
- **Windows CMD:** `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`
- **Homebrew:** `brew install --cask claude-code`
- **winget:** `winget install Anthropic.ClaudeCode`

**Q3. What's the downside of installing with Homebrew or winget?**
They don't auto-update Claude Code. You have to run the upgrade command yourself, or you'll fall behind on features and fixes. The `curl` and PowerShell installers update automatically.

**Q4. I installed Claude Code, but my terminal says `claude` isn't found. What do I do?**
Close the terminal and open a new one. A terminal only picks up newly installed programs when it starts.

**Q5. What happens the first time I run `claude`?**
It asks you to choose a color theme, then sign in. You can sign in with a Claude account (Pro, Max, or Enterprise) or use an API key. If your company has Claude Enterprise, choose that option.

**Q6. Which files can Claude Code access?**
The folder you start it in, plus every folder inside it. For example, starting it in `~/projects/my-app` gives it access to `my-app` and its subfolders, but not `~/projects/other-app`. That's why you should start it in your project folder, never your home folder.

**Q7. How do I install and open Claude Code in VS Code?**
Search "Claude Code" in the Extensions panel and install the one by Anthropic with the blue check. Restart VS Code if needed. Then press Ctrl/Cmd+Shift+P and run "Claude Code: Open in New Tab," or click the Claude logo in the sidebar.

**Q8. Why does the blue check mark on the VS Code extension matter?**
It shows the extension is the official one published by Anthropic. Without it, you could install a copy made by someone else, and that copy would be able to see your code.

**Q9. How do I use Claude Code in a JetBrains IDE, like IntelliJ or PyCharm?**
Install the Claude Code plugin from the JetBrains Marketplace and restart the IDE. Click the Claude logo to open a pane with the terminal version running next to your editor.

**Q10. What can the "Code" tab in Claude Desktop do?**
It works like the chat, but it can work in a specific folder on your computer, change permission modes, and run in a cloud environment.

**Q11. What can't Claude Code on the web do?**
It only works with GitHub repositories. It can't open a folder on your computer.

**Q12. Which option gets new features first?**
The terminal. New features ship there first.

**Q13. (Exam angle) A team wants to roll out Claude Code. What setup choices should an architect think about?**
- **Install method:** prefer installs that auto-update so everyone stays on a current version. If you use Homebrew or winget, plan how updates will happen.
- **Sign-in:** have people use the company's Enterprise account rather than personal accounts, so usage and settings are managed centrally.
- **Folder access:** teach people to start Claude Code in the project folder, because it can reach everything below where it starts.
- **Interface:** let people choose. The terminal and IDEs work on local code. The web is limited to GitHub repos.

**Q14. (Exam angle) A security team asks why it matters which folder you start Claude Code in. What do you tell them?**
The starting folder sets how much Claude Code can reach. Starting it too high, such as in a home folder, could expose files that have nothing to do with the task, like private documents or credentials. Starting it in the project folder keeps it limited to what the task needs. This idea, giving only the access a task needs, is called *least privilege*.

---

| Previous | Course | Next |
|:---|:---:|---:|
| [← How Claude Code works](02-how-claude-code-works.md) | [📚 Course index](README.md) | [Your first prompt →](04-your-first-prompt.md) |
