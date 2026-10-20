from pathlib import Path
from portfolio_engine import run
from powerbi_builder import build as build_powerbi
from dashboard_builder import build as build_dashboard

if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    run(root, 'saudi')
    build_powerbi(root, 'saudi')
    build_dashboard(root)
