# Data Pivot Table Tool

Current build: `Build Version 3 | Build Date: May 2026`

Data Pivot Table Tool is a lightweight desktop analytics application
built with Python, PySide6, and pandas.

It allows analysts to:

- import large CRM CSV datasets
- map required reporting fields
- filter included countries, job levels, and industries
- apply proportional database count adjustments
- save and reload reporting sessions
- export pivot-style summary counts to CSV

## Current Flow

The app now behaves as a single guided workflow:

1. Import CSV
2. Column Mapping
3. Filter Data
4. Analytics Report

Only one primary workflow window is visible at a time. Back-navigation is
available from later steps so users can return to import, mapping, or
filtering without relaunching the app.

## Key Features In V3

- Consistent `Inter -> Proxima Nova -> Segoe UI -> default` font stack
- Shared app icon from `assets/data-pivot.ico`
- Country presets that support both full names and 2-letter country codes
- Session save/load tools for repeatable workflows
- Cleaner analytics header layout and improved table alignment

## Project Layout

```text
assets/   icons and design assets
charts/   optional chart helpers
engine/   data loading, summary logic, adjustments, sessions
gui/      workflow windows and shared UI styles
sessions/ saved reporting sessions generated at runtime
main.py   application entry point
config.py app metadata and shared paths
```

## Dependencies

Direct project dependencies are listed in `requirements.txt`:

- `pandas`
- `PySide6`
- `matplotlib`
- `pyinstaller`

Install them with:

```bash
pip install -r requirements.txt
```

## Packaging

The repository includes a PyInstaller spec for the current release:

- `data_pivot_tool_v3.spec`

Example build command:

```bash
pyinstaller data_pivot_tool_v3.spec
```

Generated build output belongs in `build/` and `dist/` and is already
ignored by git.
