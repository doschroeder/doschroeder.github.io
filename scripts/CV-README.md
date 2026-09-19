# Generate the academic CV

The generator reads the website's source files each time it runs and creates a
multi-page A4 PDF using the approved Lora/charcoal design: right-aligned dates,
no vertical dividers, and a separate venue/year column for publications. Your
name is subtly emphasized in author lists. Venue names remain as recorded in
the website data. No internet connection,
Hugo server, or manual copying of CV entries is needed after installation.

## Run on this computer

Double-click `generate-cv.command` in the website folder, or run:

```sh
./generate-cv.command
```

Output: `static/cv/Dominique-Schroeder-CV.pdf`. Each run replaces that generated
PDF and a companion `.sources.json` report in `output/cv/` listing input files, section counts,
and data warnings. It does not change the website data. The PDF is included in the next website deployment.

## Set up on another computer

Requires Python **3.11 or newer**. In the website folder:

```sh
python3 -m venv .venv-cv
.venv-cv/bin/python -m pip install -r scripts/requirements-cv.txt
./generate-cv.command
```

On Windows, use `.venv-cv\Scripts\python` for the Python commands and invoke
`scripts/generate_cv.py` directly. The script resolves the website relative to
its own location, so running from another working directory also works.

## Options

```sh
# Choose the destination.
./generate-cv.command --output /path/to/my-cv.pdf

# Choose a shorter selection and its order (not a fixed page count).
./generate-cv.command --sections appointments,education,research,awards,publications

# Use another copy of the website.
.venv-cv/bin/python scripts/generate_cv.py --site-root /path/to/website

# See all section keys.
./generate-cv.command --help
```

`--as-of YYYY-MM-DD` changes the generation-date footer, not the date of the data
or which records are included. Records dated in future years are retained and
reported in the build notes; the generator does not infer publication status.

## Where to edit content

| CV content | Website source |
|---|---|
| Name, role line, email | `hugo.toml` title and params |
| Research introduction, parliamentary hearings | `data/editorial.json` |
| Appointments, education, awards, visits | Corresponding `data/en/*.yml` files |
| Publications, patents, projects | `publications.yml`, `patents.yml`, `projects.yml` |
| Doctoral students and postdocs | `PhDStudents.yml`, `Postdocs.yml` |
| Teaching | `lectures.yml` |
| Conference, editorial, committee and reviewing service | `pchairs.yml`, `editor.yml`, `pc.yml`, `grants.yml`, `journal.yml`, `PhDCommittee.yml`, `admin.yml` |
| Talks | `talks.yml` |

The role line comes from the first sentence of the website description, with
the name removed. The generator does not maintain a separate biography.

Teaching is compacted by course title, institution and degree level, with all
recorded years listed. Long course descriptions and publication abstracts are
omitted. Publications retain source order within each year, newest years first;
recorded external PDF links are clickable. Local-only PDF names are not turned
into guessed public URLs. Entries stay together across page breaks.

The old `currentPositions.yml` conflicts with the website's appointment history
and is deliberately not used. `teaching.yml` contains descriptive course cards;
`lectures.yml` is used for the dated teaching record. Journal reviewing is sourced from `journal.yml`; editorial positions are sourced
separately from `editor.yml`. Legacy LaTeX punctuation is normalized only during rendering. Wording, financial
amounts, names and dates otherwise remain as recorded; source typos or outdated
facts should be corrected in the website data. The generator does not verify
facts or infer whether funding was awarded or submitted.

## Check after changes

```sh
.venv-cv/bin/python -m unittest discover -s scripts -p 'test_generate_cv.py'
```

The PDF integration check requires `pdftotext` (Poppler). It edits a temporary
copy of the website, verifies the edit appears in the PDF, and checks that every
publication title is included. The real website data is untouched.

## Automatic refresh

Run `./setup-cv.command` once in each clone to install dependencies and enable
the local commit hook. It builds from staged files and stages only the generated
PDF. A normal push then uploads both. GitHub Actions also regenerates the PDF
before deployment; see the main README for details.
