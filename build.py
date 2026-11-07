"""Build the signed-in web portal into dist/index.html. No athlete data inside: it loads from Firestore after a coach signs in.

  python3 build.py

The template in templates/ is shared with the local build (../pipeline/scripts/build_portal.py), which injects the data."""
import datetime, os, pathlib, re, subprocess
from zoneinfo import ZoneInfo
root = pathlib.Path(__file__).resolve().parent
FIREBASE_SDK = '10.12.2'
src = lambda f: (root / 'src' / f).read_text()
sdk = ''.join(f'<script src="https://www.gstatic.com/firebasejs/{FIREBASE_SDK}/firebase-{m}-compat.js"></script>\n' for m in ('app', 'auth', 'firestore'))

def _sha():
    try: return os.environ.get('GITHUB_SHA') or subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=root).stdout.strip()
    except Exception: return ''
# version stamp in the footer, Pacific time: tells whether an update has reached a device (Pages caches for 10 minutes)
_pt = datetime.datetime.now(ZoneInfo('America/Los_Angeles'))
BUILD = _pt.strftime('%b %-d, %-I:%M %p').replace('AM', 'am').replace('PM', 'pm') + (' · ' + _sha()[:7] if _sha() else '')

html = (root / 'templates' / 'portal_template.html').read_text()
DATA = '<script id="portal-data">window.D = __DATA__;</script>'
assert DATA in html and html.count('__DATA__') == 1
html = html.replace(DATA, '<script id="portal-data">window.D = null;</script>')
# the portal's own script waits until the gate has signed the coach in and loaded the data
APP = '<script id="portal-app">'
assert html.count(APP) == 1
html = html.replace(APP, '<script type="text/x-jx-app" id="portal-app">')
head = (f'<script>window.JX_BUILD={BUILD!r};window.JX_PORTAL="xc";</script>\n'
        '<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">\n'
        '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n<link rel="manifest" href="manifest.webmanifest">\n'
        '<meta name="theme-color" content="#231F20">\n<meta name="apple-mobile-web-app-capable" content="yes">\n'
        '<meta name="mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-title" content="Jesuit XC">\n'
        '<style>' + src('gate.css') + '</style>\n' + sdk + '<script>' + src('firebase-config.js') + '</script>\n')
html = html.replace('</head>', head + '</head>', 1)
html = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + '\n' + src('gate.html'), html, count=1)
html = html.replace('</body>', '<script>' + src('gate.js') + '</script>\n</body>', 1)
dest = root / 'dist' / 'index.html'
dest.parent.mkdir(exist_ok=True)
# home screen icons (src/static, made from the Jesuit mascot art Kevin supplied) and the Android install manifest
import json, shutil
for f in (root / 'src' / 'static').iterdir(): shutil.copy(f, root / 'dist' / f.name)
(root / 'dist' / 'manifest.webmanifest').write_text(json.dumps(dict(
    name='Jesuit XC', short_name='Jesuit XC', start_url='./', scope='./', display='standalone',
    background_color='#FFFFFF', theme_color='#231F20',
    icons=[dict(src='icon-192.png', sizes='192x192', type='image/png'), dict(src='icon-512.png', sizes='512x512', type='image/png')]), indent=1))
dest.write_text(html)
print(f'wrote dist/index.html ({len(html):,} bytes)')
