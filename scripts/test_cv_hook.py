"""Integration test for the staged-data CV hook; uses an isolated Git repository."""
import os
import shlex
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

@unittest.skipUnless(shutil.which('git') and shutil.which('pdftotext'),'Git and Poppler required')
class HookTest(unittest.TestCase):
    def test_staged_snapshot_and_generation_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            for name in ('scripts','data','.githooks'):
                shutil.copytree(ROOT/name,root/name,ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copy(ROOT/'hugo.toml',root/'hugo.toml')
            (root/'static').mkdir();shutil.copytree(ROOT/'static/fonts',root/'static/fonts')
            (root/'.venv-cv/bin').mkdir(parents=True)
            launcher=root/'.venv-cv/bin/python'
            launcher.write_text('#!/bin/sh\nexec '+shlex.quote(sys.executable)+' \"$@\"\n')
            launcher.chmod(0o755)
            (root/'.gitignore').write_text('.venv-cv/\noutput/\n__pycache__/\n')
            env=os.environ.copy()
            for key in list(env):
                if key.startswith('GIT_'): env.pop(key)
            def run(*args,check=True):
                return subprocess.run(args,cwd=root,env=env,check=check,capture_output=True,text=True)
            run('git','init');run('git','config','user.name','CV test');run('git','config','user.email','cv-test@example.invalid')
            run('git','config','core.hooksPath','.githooks');run('git','add','.')
            path=root/'data/en/employment.yml';text=path.read_text()
            path.write_text(text.replace('Technische Universität Wien, Vienna, Austria','UNSTAGED_SENTINEL'))
            run('git','commit','-m','Test staged snapshot')
            pdf=root/'static/cv/Dominique-Schroeder-CV.pdf'
            content=run('pdftotext',str(pdf),'-').stdout
            self.assertNotIn('UNSTAGED_SENTINEL',content)
            self.assertIn('UNSTAGED_SENTINEL',path.read_text())
            self.assertIn('static/cv/Dominique-Schroeder-CV.pdf',run('git','ls-files').stdout)
            run('git','add',str(path));run('git','commit','-m','Include staged update')
            self.assertIn('UNSTAGED_SENTINEL',run('pdftotext',str(pdf),'-').stdout)
            previous=run('git','rev-parse','HEAD').stdout
            path.write_text('invalid: [\n');run('git','add',str(path))
            self.assertNotEqual(run('git','commit','-m','Must fail',check=False).returncode,0)
            self.assertEqual(previous,run('git','rev-parse','HEAD').stdout)

if __name__=='__main__':unittest.main()
