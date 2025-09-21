# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a data analysis repository containing an Excel dataset (`first-80-rows-agentic_ai_performance_dataset_20250622.xlsx`) focused on agentic AI performance metrics. The repository is in early setup phase for developing a data dashboard.

## Repository Structure

- `first-80-rows-agentic_ai_performance_dataset_20250622.xlsx` - Primary dataset with 80 rows of agentic AI performance data
- `.gitignore` - Comprehensive ignore rules for Python, Node.js, IDEs, and Excel files
- `use-deepseek-in-claude-code-with-api-key.ps1` - PowerShell script for DeepSeek API integration with Claude

## Development Environment Setup

### Python Environment (Recommended)
```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows
.venv\Scripts\activate

# Install common data analysis packages
pip install pandas numpy matplotlib seaborn openpyxl jupyter
```

### Node.js Environment (Alternative)
```bash
# Initialize Node.js project
npm init -y

# Install data visualization libraries
npm install d3.js chart.js pandas-js
```

## Common Development Tasks

### Data Exploration
```python
import pandas as pd

# Load Excel data
df = pd.read_excel('first-80-rows-agentic_ai_performance_dataset_20250622.xlsx')
print(df.info())
print(df.head())
```

### Excel File Operations
- Use `openpyxl` or `pandas` for reading/writing Excel files
- Handle Excel temporary files appropriately (see `.gitignore`)

## Project Setup Recommendations

1. **Choose a framework**: Consider Streamlit (Python) or React + D3.js (JavaScript) for dashboard
2. **Data processing**: Use pandas for data manipulation and cleaning
3. **Visualization**: matplotlib/seaborn for Python, D3.js/Chart.js for JavaScript
4. **Development server**: Configure appropriate run commands based on chosen framework

## Environment Configuration

The repository includes a PowerShell script for DeepSeek API integration:
```powershell
./use-deepseek-in-claude-code-with-api-key.ps1
```

## Next Steps
- Analyze dataset structure and create data schema
- Set up project structure with src/, data/, tests/ directories
- Choose and configure development framework
- Implement basic data loading and visualization components