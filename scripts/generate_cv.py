#!/usr/bin/env python3
"""Generate a charcoal/Lora academic CV from the Hugo website's source data."""
from __future__ import annotations
import argparse
from datetime import date
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import tomllib
from urllib.parse import urlparse

import yaml
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ('appointments', 'education', 'research', 'awards', 'visits', 'funding',
            'publications', 'patents', 'doctoral-students', 'postdocs', 'teaching',
            'chairs', 'editorial', 'program-committees', 'grant-reviewing',
            'journal-reviewing', 'doctoral-committees', 'administration', 'public-service', 'talks')

class PlainHTML(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts = []
    def handle_data(self, data): self.parts.append(data)
    def handle_starttag(self, tag, attrs):
        if tag in ('br', 'p', 'div', 'li'): self.parts.append(' ')
    def handle_endtag(self, tag):
        if tag in ('p', 'div', 'li'): self.parts.append(' ')

def clean(value):
    """Convert the site's HTML and legacy LaTeX punctuation to ordinary text."""
    if value is None: return ''
    s = str(value)
    s = re.sub(r'\\([&$%_#])', r'\1', s).replace('~', ' ')
    s = s.replace('``', '“').replace("''", '”')
    s = re.sub(r'\\(?:textit|textbf|emph)\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', s)
    parser = PlainHTML(); parser.feed(s)
    s = html.unescape(''.join(parser.parts))
    s = re.sub(r'[–—]|--+', '-', s)
    return re.sub(r'\s+', ' ', s).strip()

def escape(value): return html.escape(clean(value), quote=True)
def joined(*values): return ' · '.join(clean(v) for v in values if clean(v))
def dates(value):
    s = re.sub(r'\s*-\s*', '-', clean(value))
    return s + 'present' if s.endswith('-') else s

def link(label, url):
    u = str(url or '').strip()
    if urlparse(u).scheme not in ('https', 'http', 'mailto'): return escape(label)
    return '<link href="' + html.escape(u, quote=True) + '">' + escape(label) + '</link>'

class Website:
    def __init__(self, root):
        self.root = root; self.sources = []; self.warnings = []; self.cache = {}
        self.config = tomllib.loads(self.read('hugo.toml'))
        self.editorial = json.loads(self.read('data/editorial.json'))
    def read(self, relative):
        self.sources.append(relative)
        return (self.root / relative).read_text(encoding='utf-8')
    def data(self, filename, key, member='items'):
        if filename not in self.cache:
            # The legacy Hugo data contains tabs after YAML separators.
            self.cache[filename] = yaml.safe_load(self.read('data/en/' + filename + '.yml').replace('\t', '    '))
        value = self.cache[filename][key][member]
        if not isinstance(value, list): raise ValueError(f'{filename}.{key}.{member} must be a list')
        return value

def doctoral_detail(student):
    lines=[clean(student.get('thesis') or student.get('topic'))]
    if student.get('finished'):
        if student.get('nextPos'):
            lines.append('First position after PhD: '+clean(student['nextPos']))
        if student.get('currentPos'):
            lines.append('Current position: '+clean(student['currentPos']))
    else:
        lines.append('Ongoing')
    return '\n'.join(line for line in lines if line)

def build_sections(site):
    """Return title and (date, title, detail, optional URL) entries per section."""
    sections = {}
    def add(key, title, rows): sections[key] = (title, list(rows))
    d = site.data
    add('appointments', 'Academic appointments', ((dates(x['date']), x['institution'], x.get('description'), None) for x in d('employment','employment')))
    add('education', 'Education', ((dates(x['date']), x['institution'], joined(x.get('degree'), x.get('subject'), x.get('topics')), None) for x in d('education','education')))
    add('research', 'Research interests', [('', site.editorial.get('intro',''), site.editorial.get('description',''), None)])
    add('awards', 'Honors and awards', ((x.get('date'), x['name'], joined(x.get('agency'),x.get('venue')), None) for x in d('awards','awards')))
    add('visits', 'Research visits', ((dates(x.get('date')), joined(x['name'],x.get('location')), 'Host: '+clean(x['host']) if x.get('host') else '', None) for x in d('visits','visits')))
    add('funding', 'Research funding and projects', ((dates(x.get('duration')),x['title'],joined(x.get('sponsor'),x.get('role'),x.get('amount')),None) for x in d('projects','projects','item')))
    papers=[]
    for group in sorted(d('publications','publications','years'), key=lambda x:int(x['year']), reverse=True):
        for x in group['papers']:
            # Prefer an explicitly recorded external link. Never emit localhost links.
            url = x.get('pdf') or None
            if url and urlparse(str(url)).scheme not in ('http','https'): url=None
            papers.append((group['year'], x['title'], joined(x.get('authors'),x.get('published'),x.get('pages')),url))
    add('publications','Publications',papers)
    add('patents','Patents', ((g['year'],x['title'],joined(x.get('authors'),joined(x.get('office'),x.get('number'))),x.get('url')) for g in d('patents','patents','years') for x in g['papers']))
    add('doctoral-students','Doctoral supervision', ((joined(x.get('start'))+' - '+(clean(x.get('graduated')) if x.get('finished') else 'present'),x['name'],doctoral_detail(x),None) for x in d('PhDStudents','PhDStudents','list')))
    add('postdocs','Postdoctoral mentoring', ((joined(x.get('start'))+' - '+(clean(x.get('end')) if x.get('finished') else 'present'),x['name'],('Subsequent position: '+clean(x.get('nextpos'))) if x.get('nextpos') else '',None) for x in d('Postdocs','postdocs','list')))
    courses={}
    for group in d('lectures','lectures'):
        for x in group['lecture']:
            key=(clean(x['title']),clean(x.get('university')),clean(x.get('turnus')))
            courses.setdefault(key, set()).add(int(group['year']))
    add('teaching','Teaching', ((', '.join(map(str,sorted(years,reverse=True))),title,joined(university,level),None) for (title,university,level),years in sorted(courses.items(), key=lambda item:(-max(item[1]),item[0]))))
    for key,filename,title in [('chairs','pchairs','Conference leadership'),('editorial','editor','Editorial boards'),('program-committees','pc','Program committees (selected)'),('grant-reviewing','grants','Grant reviewing'),('journal-reviewing','journal','Journal reviewing'),('administration','admin','Administrative service')]:
        add(key,title,((dates(x.get('date')),x['name'],'',None) for x in d(filename,filename)))
    add('doctoral-committees','Doctoral committees',((g['year'],x['name'],joined(x.get('role'),x.get('institution')),None) for g in d('PhDCommittee','phdcomm') for x in g['candidate']))
    add('public-service','Expert contributions and public service',((x['year'],'Deutscher Bundestag · Health Committee', 'Independent expert contribution: '+clean(x['title']), x.get('url')) for x in site.editorial['hearings']))
    add('talks','Selected talks and appearances',((x['year'],x['title'],x.get('location'),None) for x in sorted(d('talks','talks'),key=lambda x:int(x['year']),reverse=True)))
    return sections

class Renderer:
    def __init__(self, site, output, as_of):
        self.site=site; self.as_of=as_of; self.name=clean(site.config['title']); self.width=A4[0]-108
        fontdir=site.root/'static/fonts'
        for name,file in [('Lora','lora-regular.ttf'),('LoraMedium','lora-medium.ttf')]:
            pdfmetrics.registerFont(TTFont(name,str(fontdir/file)))
        pdfmetrics.registerFontFamily('Lora',normal='Lora',bold='LoraMedium',italic='Lora',boldItalic='LoraMedium')
        self.styles={
            'body':ParagraphStyle('body',fontName='Lora',fontSize=10,leading=13.7,textColor=colors.HexColor('#202020')),
            'detail':ParagraphStyle('detail',fontName='Lora',fontSize=9.4,leading=13,textColor=colors.HexColor('#505050')),
            'date':ParagraphStyle('date',fontName='Lora',fontSize=8.5,leading=11.5,alignment=2,textColor=colors.HexColor('#505050')),
            'heading':ParagraphStyle('heading',fontName='LoraMedium',fontSize=10.5,leading=14,textColor=colors.HexColor('#292929'),spaceBefore=18,spaceAfter=10,keepWithNext=True),
            'name':ParagraphStyle('name',fontName='Lora',fontSize=19,leading=24,spaceAfter=8),
        }
        self.doc=SimpleDocTemplate(str(output),pagesize=A4,leftMargin=48,rightMargin=48,topMargin=51,bottomMargin=49,title=self.name+' - Curriculum Vitae',author=self.name)
        self.story=[]
    def p(self,s,style='body'): return Paragraph(s,self.styles[style])
    def header(self):
        self.story.append(self.p(escape(self.name),'name'))
        # Use the website description verbatim; avoid a second hard-coded biography.
        description=clean(self.site.config.get('params',{}).get('description',''))
        prefix=self.name+', '
        if description.startswith(prefix): description=description[len(prefix):]
        role=description.split('. Research',1)[0].rstrip('.')
        self.story.append(self.p(escape(role),'detail'))
        email=self.site.config.get('params',{}).get('email','')
        if email: self.story.append(self.p(link(email,'mailto:'+email),'detail'))
        self.story.append(Spacer(1,5))
    def section(self,key,title,rows):
        if not rows: return
        heading=self.p(escape(title),'heading');heading._cv_section=key
        self.story.append(heading)
        if key == 'publications':
            self.publications()
            return
        for dt,title,detail,url in rows:
            title_markup=link(title,url) if url else escape(title)
            if clean(dt):
                table=Table([[self.p(title_markup),self.p(escape(dt),'date')]],
                            colWidths=[self.width-112,112],hAlign='LEFT')
                table.setStyle(self.table_style(12))
                body=[table]
            else:
                body=[self.p(title_markup)]
            if clean(detail):
                for line in str(detail).split('\n'):
                    body.append(self.p(escape(line),'detail'))
            body.append(Spacer(1,7))
            self.story.append(KeepTogether(body))

    @staticmethod
    def table_style(gap):
        return TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),0),
            ('RIGHTPADDING',(0,0),(0,0),gap),
            ('RIGHTPADDING',(1,0),(1,0),0),
            ('TOPPADDING',(0,0),(-1,-1),0),
            ('BOTTOMPADDING',(0,0),(-1,-1),0),
        ])

    def publications(self):
        venue_style=ParagraphStyle('venue',parent=self.styles['body'],
                                   fontName='LoraMedium',fontSize=9.2,leading=12,alignment=2)
        for group in sorted(self.site.data('publications','publications','years'),
                            key=lambda g:int(g['year']),reverse=True):
            for paper in group['papers']:
                authors=escape(paper.get('authors','')).replace(
                    escape(self.name),'<b>'+escape(self.name)+'</b>')
                main=[self.p(link(paper['title'],paper.get('pdf'))),
                      self.p(authors,'detail')]
                if clean(paper.get('pages')):
                    main.append(self.p('pp. '+escape(paper['pages']),'detail'))
                venue=[Paragraph(escape(paper.get('published','')),venue_style),
                       self.p(escape(group['year']),'date')]
                table=Table([[main,venue]],colWidths=[self.width-116,116],hAlign='LEFT')
                table.setStyle(self.table_style(24))
                table.spaceAfter=16
                self.story.append(table)
    def footer(self,c,doc):
        c.saveState();c.setFillColor(colors.HexColor('#505050'));c.setFont('Lora',8)
        if doc.page>1: c.drawString(48,A4[1]-29,self.name+' · Curriculum Vitae')
        c.drawString(48,27,'Generated '+self.as_of.isoformat())
        c.drawRightString(A4[0]-48,27,'Curriculum Vitae  |  '+str(doc.page));c.restoreState()
    def save(self): self.doc.build(self.story,onFirstPage=self.footer,onLaterPages=self.footer)

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-root',type=Path,default=ROOT,help='Hugo website root (default: script parent)')
    parser.add_argument('--output',type=Path,help='PDF path (default: SITE/static/cv/Dominique-Schroeder-CV.pdf)')
    parser.add_argument('--sections',default=','.join(SECTIONS),help='Comma-separated section keys, in desired order: '+', '.join(SECTIONS))
    parser.add_argument('--as-of',type=date.fromisoformat,default=date.today(),help='Generation date YYYY-MM-DD; does not filter source records')
    args=parser.parse_args(argv)
    selected=[s.strip() for s in args.sections.split(',') if s.strip()]
    if not selected or set(selected)-set(SECTIONS): parser.error('Provide valid section keys; see --help.')
    if len(selected)!=len(set(selected)): parser.error('Section keys must not be repeated.')
    output=(args.output or args.site_root/'static/cv/Dominique-Schroeder-CV.pdf').resolve()
    if output.suffix.lower()!='.pdf': parser.error('--output must have a .pdf extension')
    site=Website(args.site_root.resolve());sections=build_sections(site)
    output.parent.mkdir(parents=True,exist_ok=True)
    renderer=Renderer(site,output,args.as_of);renderer.header()
    for key in selected:
        title,rows=sections[key];renderer.section(key,title,rows)
    renderer.save()
    future=[str(y) for y,_,_,_ in sections['publications'][1] if int(y)>args.as_of.year]
    warnings=[]
    if future: warnings.append('Future-dated publications retained as recorded on website: '+', '.join(sorted(set(future))))
    manifest={'generated':args.as_of.isoformat(),'sources':sorted(set(site.sources)), 'sections':{key:len(sections[key][1]) for key in selected},'warnings':warnings}
    (args.site_root/'output/cv').mkdir(parents=True,exist_ok=True)
    (args.site_root/'output/cv'/output.with_suffix('.sources.json').name).write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(output)
    print('Included '+', '.join(f'{v} {k}' for k,v in manifest['sections'].items()))
    for warning in warnings: print('Note: '+warning,file=sys.stderr)
    return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except (OSError,ValueError,KeyError,yaml.YAMLError) as exc:
        print('CV generation failed: '+str(exc),file=sys.stderr);raise SystemExit(1)
