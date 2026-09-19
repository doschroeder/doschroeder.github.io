#!/usr/bin/env python3
"""Validate a Hugo output directory without fetching external websites."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import sys


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.ids = []
        self.h1_count = 0
        self.language = None
        self.images = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'html':
            self.language = attrs.get('lang')
        if tag == 'h1':
            self.h1_count += 1
        if tag == 'img':
            self.images.append(attrs)
        for key in ('href', 'src'):
            if key in attrs:
                self.references.append(attrs[key])
        for source in attrs.get('srcset', '').split(','):
            if source.strip():
                self.references.append(source.strip().split()[0])


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else 'public').resolve()
    documents = {}
    errors = []
    references = 0
    for file in root.rglob('*.html'):
        page = Page()
        page.feed(file.read_text())
        documents[file] = page
        name = file.relative_to(root)
        if page.h1_count != 1:
            errors.append(f'{name}: expected one h1, found {page.h1_count}')
        if not page.language:
            errors.append(f'{name}: missing document language')
        for anchor, count in Counter(page.ids).items():
            if count > 1:
                errors.append(f'{name}: duplicate ID {anchor}')
        for image in page.images:
            if not image.get('alt'):
                errors.append(f'{name}: missing image description')
    if not documents:
        errors.append(f'No HTML files found in {root}')
    for file, page in documents.items():
        for reference in page.references:
            url = urlparse(reference)
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            # Hugo serves this development endpoint dynamically.
            if path == '/livereload.js':
                continue
            target = root / path.lstrip('/') if path.startswith('/') else file.parent / path
            if not path:
                target = file
            if target.is_dir():
                target /= 'index.html'
            target = target.resolve()
            references += 1
            if not target.exists():
                errors.append(f'{file.relative_to(root)}: missing target {reference}')
            elif url.fragment and target in documents:
                if unquote(url.fragment) not in documents[target].ids:
                    errors.append(f'{file.relative_to(root)}: missing anchor {reference}')
    print(f'Checked {len(documents)} HTML pages and {references} internal references.')
    for error in errors:
        print(error)
    print(f'{len(errors)} errors.')
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
