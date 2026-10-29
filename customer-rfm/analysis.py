from pathlib import Path
import sys

# Keep the command simple while implementation modules live in src/.
sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))
from portfolio_engine import run
from powerbi_builder import build as build_powerbi
from dashboard_builder import build as build_dashboard

if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    run(root, 'rfm')
    build_powerbi(root, 'rfm')
    build_dashboard(root)
