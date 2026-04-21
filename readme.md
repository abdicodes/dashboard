python3 -m venv .venv

.venv/bin/pip install -r requirements.txt

.venv/bin/python app.py

Then open http://127.0.0.1:8050 (see app.py).

Data is mock in each widget module; you can later replace those structures with queries or a shared data layer per hotel using hotel-selector as Input in callbacks.

Note: employee_widget used zip(..., strict=False), which needs Python 3.10+; it’s been changed to plain zip(...) so Python 3.9 works (as in the smoke test).
