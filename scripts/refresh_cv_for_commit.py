#!/usr/bin/env python3
"""Build the CV from the Git index, never from unstaged website edits."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile

PDF = 'static/cv/Dominique-Schroeder-CV.pdf'
def git(*args, **kwargs):
    return subprocess.run(['git', *args], check=True, **kwargs)

def main():
    root=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
    os.chdir(root)
    # Never overwrite a user's unstaged PDF edit.
    if subprocess.run(['git','diff','--quiet','--',PDF]).returncode:
        sys.exit('CV has unstaged edits. Stage or save them before committing.')
    with tempfile.TemporaryDirectory(prefix='website-cv-') as temp:
        snapshot=Path(temp)/'staged';snapshot.mkdir()
        git('checkout-index','--all','--prefix='+str(snapshot)+os.sep)
        generated=snapshot/PDF
        subprocess.run([sys.executable,str(snapshot/'scripts/generate_cv.py'),
                        '--site-root',str(snapshot),'--output',str(generated)],check=True)
        (root/PDF).parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(generated,root/PDF)
        git('add','--',PDF)
    print('Fresh CV generated from staged website data and included in this commit.')

if __name__=='__main__': main()
