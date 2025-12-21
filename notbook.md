## Option 1: VS Code (in the browser) + Jupyter extension (GitHub Codespaces)

1. Open your repo in a **GitHub Codespace**.
2. In the **Extensions** panel, install:
   - **Python**
   - **Jupyter**
3. Ensure there’s a Python environment available in the Codespace (there usually is).
4. Open a `.ipynb` file → select a **kernel** when prompted → run cells like normal.

### If Jupyter/kernel isn’t available yet
Run these in the Codespace terminal:

```bash
python -m pip install -U pip
pip install jupyter ipykernel
python -m ipykernel install --user --name codespace --display-name "Python (codespace)"
'''

5.	Reload the notebook, then choose the kernel: Python (codespace).

