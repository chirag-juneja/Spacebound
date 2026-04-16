# Spacebound: Agent Instructions

## 🛠️ Project Setup & Execution
1. **Dependencies**: Always run `pip install -r requirements.txt` first to set up the environment.
2. **Execution**: The primary entry point for running the game simulation is `python main.py`.
3. **Assets**: Art assets (images/sound) are in `assets/` and are essential.

## 📚 Architecture Notes
*   **Game Loop**: Core logic is in `spacebound/game.py`.
*   **Entities/Behavior**: Entity-specific behaviors (sprites) are defined in `spacebound/sprites/`.
*   **Levels**: Different level implementations are stored in `spacebound/levels/` (e.g., `duel.py`).
*   **Imports**: Relative imports are heavily used within the `spacebound/` package.

## 💡 Dev Workflow Gotchas
*   **Truth Source**: Always trust executable configurations (CI/pre-commit hooks) over prose documentation.
*   **Verification**: Before committing, always check the repository state using `git status` and `git diff` to understand the full scope of changes.