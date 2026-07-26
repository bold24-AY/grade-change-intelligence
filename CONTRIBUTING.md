# Contributing to Grade Change Intelligence

We love your contributions! Please review the guidelines below to help keep our codebase clean, robust, and professional.

---

## 💡 Code of Conduct
We adhere to standard open-source behaviors. Be respectful, inclusive, and professional in all communication and pull requests.

## 🚀 How to Contribute

### 1. Fork & Clone
1. Fork this repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/grade-change-intelligence.git
   ```

### 2. Setup Virtual Environment
Create a fresh environment and install all developer checks:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create a Feature Branch
Use descriptive branch naming prefixes:
- `feat/some-feature` for new attributes.
- `fix/bug-fix` for patching regressions.
- `docs/updating-docs` for guides.

```bash
git checkout -b feat/add-new-regressor
```

### 4. Code Quality & Standards
We maintain high standards to impress judges and users:
- **PEP 8**: Adhere to standard Python formatting rules.
- **Type Hinting**: All functions must include strict type annotations.
- **No Duplication**: Extract common mathematical formulas (gains, clipping) to shared modules.
- **Run Pytest**: Before pushing, ensure the entire test suite passes:
  ```bash
  python -m pytest
  ```

### 5. Submit a Pull Request
1. Commit changes locally with descriptive messages.
2. Push your feature branch:
   ```bash
   git push origin feat/add-new-regressor
   ```
3. Open a Pull Request (PR) against our `main` branch. Provide a summary of modifications and attach unit test logs.

---

## 🛠 Project Standards Checklist
- [ ] Code compiles without warnings.
- [ ] No raw `except:` catches; handle specific errors (e.g., `FileNotFoundError`, `yaml.YAMLError`).
- [ ] Docstrings provided on all public functions/classes.
