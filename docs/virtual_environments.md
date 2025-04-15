# **Short Guide to Using Virtual Environments for Your Python Project**

Virtual environments help isolate project dependencies, preventing conflicts between different projects. Here’s how to set one up:

---

### **Index**

1. **[How to use it](#how-to-use-it)**

   - [1. Create a Virtual Environment](#1-create-a-virtual-environment)
   - [2. Activate the Virtual Environment](#2-activate-the-virtual-environment)
   - [3. Install Dependencies](#3-install-dependencies)
   - [4. Deactivate the Environment](#4-deactivate-the-environment)
   - [5. Restore the Environment Later](#5-restore-the-environment-later)

2. **[Best Practices](#-best-practices)**

3. **[VS Code Config](#vs-code-config)**

   - [What This Means](#what-this-means)
   - [What You Should Do](#what-you-should-do)
   - [How to Verify It Worked](#how-to-verify-it-worked)
   - [If You Missed the Prompt](#if-you-missed-the-prompt)
   - [Why This Matters](#why-this-matters)

4. **[Add dependency to requirements.txt](#add-dependency-to-requirementstxt)**

---

## How to use it

### **1. Create a Virtual Environment**

Run this command in your project folder:

```bash
python -m venv venv
```

- This creates a folder called `venv` containing the Python environment.

---

### **2. Activate the Virtual Environment**

#### **Windows (PowerShell or CMD)**

```bash
.\venv\Scripts\activate
```

#### **macOS / Linux (Bash/Zsh)**

```bash
source venv/bin/activate
```

✅ **You’ll see `(venv)` in your terminal, meaning the environment is active.**

---

### **3. Install Dependencies**

With the environment active, install packages (e.g., `pytest`):

```bash
pip install pytest
```

📌 **To save dependencies to `requirements.txt`:**

```bash
pip freeze > requirements.txt
```

---

### **4. Deactivate the Environment**

When done, exit the virtual environment:

```bash
deactivate
```

---

### **5. Restore the Environment Later**

If you return to the project later:

1. Activate the environment again.
2. Install dependencies (if needed):
   ```bash
   pip install -r requirements.txt
   ```

---

### **💡 Best Practices**

- **Always activate** the environment before working on the project.
- **Never commit `venv/`** to Git—add it to `.gitignore`.
- Use `requirements.txt` to keep track of dependencies.

That’s it! Now your project has a clean, isolated Python environment. 🚀

---

## VS Code Config

When **VS Code** detects a new virtual environment (like `venv`), it prompts:

> _"We noticed a new environment has been created. Do you want to select it for the workspace folder?"_

### **What This Means**

VS Code is asking if you want to use this virtual environment as the **default Python interpreter** for your project.

### **What You Should Do**

✅ **Click "Yes"** – This ensures:

- VS Code uses the correct Python version and packages from your `venv`.
- Tools like **IntelliSense (autocomplete), debugging, and testing** work properly.

### **How to Verify It Worked**

1. Open the **Command Palette** (`Ctrl+Shift+P` / `Cmd+Shift+P`).
2. Search for **"Python: Select Interpreter"**.
3. Check that the selected interpreter points to:
   ```
   .venv/Scripts/python (Windows)
   .venv/bin/python (macOS/Linux)
   ```

### **If You Missed the Prompt**

No worries! You can manually select the interpreter:

1. Click the Python version in the bottom-left corner of VS Code.
2. Choose the interpreter from your `venv` folder.

### **Why This Matters**

- Avoids conflicts between global and project-specific packages.
- Ensures VS Code’s tools (linter, debugger, etc.) use the right environment.

Once selected, VS Code will remember this choice for your workspace. 🎉

---

## Add dependency to requirements.txt

To add the `pytest` package to your `requirements.txt` file, follow these steps:

1. Open or create a `requirements.txt` file in your project's root directory.

2. Add the following line to the file:

   ```
   pytest
   ```

3. Save the file.

4. To install the packages listed in `requirements.txt`, run the following command in your terminal:
   ```bash
   pip install -r requirements.txt
   ```

If you want to specify a particular version of `pytest`, you can do so like this:

```
pytest==7.4.0  # or any other version you need
```

