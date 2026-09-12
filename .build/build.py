#!/usr/bin/env python3
"""Renders the markdown archive into a single offline HTML document."""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).parent.parent


def parse(path):
    text = path.read_text()
    meta = {}
    if text.startswith('---\n'):
        fm, text = text[4:].split('\n---\n', 1)
        for line in fm.strip().split('\n'):
            k, _, v = line.partition(':')
            meta[k.strip()] = json.loads(v.strip())
    return meta, text.strip()


def dims(path):
    """Intrinsic pixel size, so images reserve layout space before they load."""
    p = ROOT / path
    if not p.exists():
        return None
    with p.open('rb') as f:
        head = f.read(32)
        if head[:8] == b'\x89PNG\r\n\x1a\n':
            return int.from_bytes(head[16:20], 'big'), int.from_bytes(head[20:24], 'big')
        if head[:2] == b'\xff\xd8':
            f.seek(2)
            while True:
                b1 = f.read(1)
                if not b1:
                    return None
                if b1 != b'\xff':
                    continue
                marker = f.read(1)
                while marker == b'\xff':
                    marker = f.read(1)
                if marker[0] in range(0xc0, 0xcf) and marker[0] not in (0xc4, 0xc8, 0xcc):
                    f.read(3)
                    h = int.from_bytes(f.read(2), 'big')
                    w = int.from_bytes(f.read(2), 'big')
                    return w, h
                size = int.from_bytes(f.read(2), 'big')
                f.seek(size - 2, 1)
    return None


def size_attrs(src):
    d = dims(src)
    return f' width="{d[0]}" height="{d[1]}"' if d else ''


def spans(s):
    s = html.escape(s)
    s = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'`([^`]+?)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', s)
    return s


def render(md, slug):
    out, buf, listbuf = [], [], []

    def flush_para():
        if buf:
            out.append(f'<p>{spans(" ".join(buf))}</p>')
            buf.clear()

    def flush_list():
        if listbuf:
            items = ''.join(f'<li>{spans(i)}</li>' for i in listbuf)
            out.append(f'<ul>{items}</ul>')
            listbuf.clear()

    lines = md.split('\n')
    i = -1
    while i + 1 < len(lines):
        i += 1
        line = lines[i].rstrip()
        if line.startswith('|') and i + 1 < len(lines) and re.fullmatch(r'\|[\s:|-]+\|', lines[i + 1].strip()):
            flush_para(); flush_list()
            cells = lambda r: [c.strip() for c in r.strip().strip('|').split('|')]
            head = ''.join(f'<th>{spans(c)}</th>' for c in cells(line))
            rows = []
            i += 1
            while i + 1 < len(lines) and lines[i + 1].strip().startswith('|'):
                i += 1
                rows.append('<tr>' + ''.join(f'<td>{spans(c)}</td>' for c in cells(lines[i])) + '</tr>')
            out.append(f'<table><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table>')
            continue
        img = re.fullmatch(r'!\[(.*?)\]\((.+?)\)', line.strip())
        if img:
            flush_para(); flush_list()
            alt = html.escape(img.group(1))
            src = img.group(2).replace('../../', '')
            cap = f'<figcaption>{alt}</figcaption>' if alt else ''
            out.append(f'<figure><a href="{src}"><img loading="lazy"{size_attrs(src)} src="{src}" alt="{alt}"></a>{cap}</figure>')
            continue
        h = re.match(r'^(#{1,4}) +(.*)', line)
        if h:
            flush_para(); flush_list()
            level = len(h.group(1))
            if level == 1:
                continue  # the document supplies its own title
            out.append(f'<h{level + 1}>{spans(h.group(2))}</h{level + 1}>')
            continue
        if line.startswith('- '):
            flush_para()
            listbuf.append(line[2:])
            continue
        if line.startswith('> '):
            flush_para(); flush_list()
            out.append(f'<blockquote>{spans(line[2:])}</blockquote>')
            continue
        if line.strip() == '---':
            flush_para(); flush_list()
            out.append('<hr>')
            continue
        if not line.strip():
            flush_para(); flush_list()
            continue
        buf.append(line.strip())
    flush_para(); flush_list()
    return '\n'.join(out)


SECTIONS = [
    ('pages', 'The site', 'How the site presented Tegwell: the home page, the story, the team and the investor pitch.'),
    ('technology', 'Technology', 'The two core technologies under development.'),
    ('solutions', 'Solutions', 'Where the technology was meant to be applied.'),
    ('news', 'News', 'Everything Tegwell announced publicly, oldest first.'),
]
PAGE_ORDER = ['home', 'about-us', 'team', 'investors']


def collect():
    out = []
    for folder, title, blurb in SECTIONS:
        files = sorted((ROOT / 'content' / folder).glob('*.md'))
        if folder == 'pages':
            files.sort(key=lambda p: PAGE_ORDER.index(p.stem))
        docs = []
        for f in files:
            meta, md = parse(f)
            slug = f'{folder}-{meta.get("slug", f.stem)}'
            docs.append((slug, meta, render(md, slug), f))
        out.append((folder, title, blurb, docs))
    return out


def build():
    sections = collect()
    toc, body = [], []
    for folder, title, blurb, docs in sections:
        links = ''.join(
            f'<li><a href="#{slug}">{html.escape(meta["title"])}</a></li>' for slug, meta, _, _ in docs
        )
        toc.append(f'<div class="toc-group"><h3>{title}</h3><ol>{links}</ol></div>')

        arts = []
        for slug, meta, content, f in docs:
            bits = []
            if meta.get('published'):
                bits.append(meta['published'])
            if meta.get('author'):
                bits.append(meta['author'])
            meta_line = f'<p class="byline">{html.escape(" · ".join(bits))}</p>' if bits else ''
            hero = ''
            if meta.get('main_image'):
                src = f'images/{meta["main_image"]}'
                if (ROOT / src).exists():
                    hero = f'<figure class="hero"><a href="{src}"><img loading="lazy"{size_attrs(src)} src="{src}" alt=""></a></figure>'
            arts.append(
                f'<article id="{slug}">'
                f'<h2>{html.escape(meta["title"])}</h2>{meta_line}{hero}{content}'
                f'</article>'
            )
        body.append(
            f'<section id="sec-{folder}"><header class="sec"><h1>{title}</h1><p>{blurb}</p></header>'
            + '\n'.join(arts) + '</section>'
        )

    readme = parse(ROOT / 'README.md')[1]
    overview = render(readme.split('## About this archive')[0].rstrip(), 'overview')

    pdf = ROOT / 'tegwell-archive.pdf'
    downloads = ''
    if pdf.exists():
        mb = round(pdf.stat().st_size / 1_000_000)
        downloads = (f'<a class="dl" href="{pdf.name}" download>'
                     f'Download as PDF <span>{mb} MB</span></a>')
    tpl = (ROOT / '.build' / 'template.html').read_text()
    out = (tpl.replace('{{TOC}}', '\n'.join(toc))
              .replace('{{OVERVIEW}}', overview)
              .replace('{{BODY}}', '\n'.join(body))
              .replace('{{DOWNLOADS}}', downloads))
    (ROOT / 'tegwell-archive.html').write_text(out)
    print('wrote tegwell-archive.html', len(out) // 1024, 'KB')


if __name__ == '__main__':
    build()
