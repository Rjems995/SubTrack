# Contributing to SubTrack

Thank you for considering contributing to SubTrack! We welcome contributions from developers of all skill levels.

---

## Code of Conduct

* Be respectful and inclusive toward all contributors.
* Focus on constructive feedback when reviewing pull requests.

---

## How to Get Started

### 1. Fork and Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/subtrack.git
cd subtrack
```

### 2. Set Up Python Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Backend locally

```bash
uvicorn main:app --reload
```

### 4. Run Automated Tests

```bash
pytest
```

---

## Submitting Pull Requests

1. Create a descriptive branch: `git checkout -b feature/add-new-chart`
2. Commit your changes: `git commit -m "Add new breakdown chart"`
3. Push to your branch: `git push origin feature/add-new-chart`
4. Open a Pull Request on GitHub describing your additions.