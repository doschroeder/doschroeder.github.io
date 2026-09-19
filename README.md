# Dominique Schröder — personal website

Hugo website deployed to https://www.dominique-schroeder.de/ by GitHub Pages.

## Preview locally

```sh
hugo server --bind 127.0.0.1 --port 1313 --baseURL http://localhost:1313/
```

## Update content

- `data/en/`: publications, appointments, teaching, students, awards, projects and service.
- `data/editorial.json`: research introduction and parliamentary hearings.
- `content/english/`: page descriptions and content.
- `hugo.toml`: name, email and public site configuration.
- `assets/css/site.css` and `layouts/`: design and page structure.

The home page shows the five newest publications automatically. Publications are
ordered by year and retain source order within each year.

## PDF CV: local commits and deployment

On this computer the CV environment and Git hook are installed. Each normal
local commit generates `static/cv/Dominique-Schroeder-CV.pdf` from the **staged**
website files and adds that PDF to the same commit. Unstaged content stays out.
The hook stops the commit if generation fails. It does not push anything.

After committing, push normally to publish both the website and PDF. GitHub
Actions also generates the PDF before building and deploying the website, so
edits made on GitHub or from another computer still produce a fresh download.
This build does not create an extra bot commit. GitHub cannot execute commands
on your laptop; the local hook runs only for commits made on a configured computer.

For a new clone, install Python 3.11+ and run `./setup-cv.command` once. To choose
a specific interpreter: `CV_PYTHON=python3.12 ./setup-cv.command`. Git hooks are
local settings and must be enabled in every clone. Commits made with `--no-verify`
(or a client that bypasses hooks) skip local generation; deployment still builds
its own fresh copy. Do not hand-edit the generated PDF.

To regenerate without committing: `./generate-cv.command`.
The CV is linked from `/cv/` and `/about/`. The same URL always serves the latest
published version: `/cv/Dominique-Schroeder-CV.pdf`.

[Generator details](scripts/CV-README.md)

## Verification

```sh
.venv-cv/bin/python -m unittest discover -s scripts -p 'test_generate_cv.py'
hugo --destination /private/tmp/dominique-site-check
python3 scripts/check_site.py /private/tmp/dominique-site-check
```

Original site backup (on this computer):
`/Users/dosch/Documents/website-backups/doschroeder.github.io-20260919-104717`.
It includes the previous files and Git history. The old version is also preserved
in Git history before the redesign commit. No backup files are served publicly.
