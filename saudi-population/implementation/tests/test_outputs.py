import json,sqlite3,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class OutputChecks(unittest.TestCase):
    def test_quality(self):
        q=json.loads((ROOT/'outputs/quality_report.json').read_text())
        self.assertTrue(q['checks_passed'])
    def test_reconciliation(self):
        s=json.loads((ROOT/'outputs/summary.json').read_text());db=sqlite3.connect(ROOT/'outputs/analysis.sqlite')
        if 'line_items' in s:
            row=db.execute('SELECT COUNT(*),SUM(sales),COUNT(DISTINCT order_id) FROM sales').fetchone()
            self.assertEqual(row[0],s['line_items']);self.assertAlmostEqual(row[1],s['sales'],places=5);self.assertEqual(row[2],s['orders'])
        elif 'snapshot_date' in s:
            row=db.execute('SELECT COUNT(*),SUM(monetary),COUNT(DISTINCT segment) FROM rfm').fetchone()
            self.assertEqual(row[0],s['customers']);self.assertAlmostEqual(row[1],s['sales'],places=5);self.assertEqual(row[2],s['segments'])
        else:
            row=db.execute('SELECT COUNT(*),COUNT(DISTINCT region) FROM population').fetchone()
            self.assertEqual(row,(169,13));self.assertEqual(db.execute('SELECT SUM(population) FROM population WHERE year=2022').fetchone()[0],s['population_2022'])
        db.close()
if __name__=='__main__':unittest.main()
