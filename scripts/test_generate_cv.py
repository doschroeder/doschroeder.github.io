"""Run: .venv-cv/bin/python -m unittest discover -s scripts -p 'test_generate_cv.py'."""
import contextlib
import io
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import yaml
import generate_cv as cv

class CVTests(unittest.TestCase):
    def test_text_and_links_are_safe(self):
        self.assertEqual(cv.clean(r'IT Security \& Law<br> A~B'), 'IT Security & Law A B')
        self.assertEqual(cv.escape('Research & <b>privacy</b>'), 'Research &amp; privacy')
        self.assertEqual(cv.link('Paper','javascript:alert(1)'), 'Paper')
        self.assertEqual(cv.dates('2024 - '), '2024-present')
        self.assertEqual(cv.dates('10/2006 -- 11/2010'), '10/2006-11/2010')

    def test_all_publications_and_students_are_mapped(self):
        site=cv.Website(cv.ROOT); sections=cv.build_sections(site)
        papers=[p for g in site.data('publications','publications','years') for p in g['papers']]
        self.assertEqual([p['title'] for p in papers], [row[1] for row in sections['publications'][1]])
        self.assertEqual(len(sections['doctoral-students'][1]),len(site.data('PhDStudents','PhDStudents','list')))
        self.assertNotIn('data/en/currentPositions.yml',site.sources)

    @unittest.skipUnless(shutil.which('pdftotext'),'pdftotext is required for PDF integration checks')
    def test_source_edit_reaches_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'website';root.mkdir()
            shutil.copytree(cv.ROOT/'data',root/'data')
            shutil.copy(cv.ROOT/'hugo.toml',root/'hugo.toml')
            (root/'static').mkdir();(root/'static/fonts').symlink_to(cv.ROOT/'static/fonts',target_is_directory=True)
            path=root/'data/en/employment.yml'
            data=yaml.safe_load(path.read_text().replace('\t','    '))
            data['employment']['items'][0]['institution']='TEST New Institution & Research'
            path.write_text(yaml.safe_dump(data,allow_unicode=True))
            output=Path(tmp)/'result.pdf'
            with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
                cv.main(['--site-root',str(root),'--output',str(output),'--sections','appointments,publications','--as-of','2026-09-19'])
            text=subprocess.check_output(['pdftotext',str(output),'-'],text=True)
            self.assertIn('TEST New Institution & Research',text)
            self.assertIn('2026-09-19',text)
            normalized=' '.join(text.split())
            site=cv.Website(root)
            for group in site.data('publications','publications','years'):
                for paper in group['papers']:
                    self.assertIn(cv.clean(paper['title']),normalized)
            self.assertTrue((root/'output/cv/result.sources.json').exists())

if __name__=='__main__': unittest.main()
