# CLAUDE.md: Jesuit XC web portal

Public repo. Never add athlete data, names, CSV or JSON data files here. The data pipeline lives in the sibling folder
../pipeline (private, not in git; read its CLAUDE.md for the model and data). Copied in design from Kevin's Delta Hawks web
portal (../../delta-hawks/web, read only); no shared code.

- templates/portal_template.html: the portal page, single source for the local build and the signed-in web build. The
  pipeline's scripts/build_portal.py replaces `__DATA__` with data/portal_data.json (from scripts/portal_data.py) and writes
  ../pipeline/portal/jesuit_xc_portal.html, which stays local. build.py writes dist/index.html with `window.D = null`
  and the app script as type text/x-jx-app; src/gate.js signs the coach in, reads portals/xc, sets window.D and runs it.
- Live: https://kevinwelling12.github.io/jesuit-xc/ (repo kevinwelling12/jesuit-xc, public, Pages from GitHub Actions on
  push to main). Firebase project jesuit-xc: Google sign-in, Firestore rules from firestore.rules (paste into the console
  and Publish after editing), authorized domain kevinwelling12.github.io. Firestore: members/{email lowercase}
  {role: admin|coach, name, added, by}; portals/xc {version, chunks, bytes, as_of, updated}; portals/xc/chunks/NNN
  {data: gzipped JSON}. Gate behavior and checks follow Delta Hawks web/CLAUDE.md (saved copy in IndexedDB 'jesuit-xc',
  member memo 'jx-member', 20 s watchdog, version stamp in the footer).
- Icons (src/static, copied to dist/ by build.py with manifest.webmanifest): made 2026-11-07 from the Jesuit mascot
  art Kevin supplied (JHS pirate in a gold ring): apple-touch-icon 180, icon-192, icon-512 (art at 92% on white so the
  ring clears iOS's rounded corners), favicon-32. Use the supplied art only; never redraw or alter the mark.
- After any gate or rules change: a signed-out REST read of portals/xc must return 403, and the live page must show the
  sign-in card with no console errors.
- Look: Kevin's Jesuit Sacramento design system (https://claude.ai/artifact/WennPLMmW69KLVtk1adtp3, project/tokens.json).
  Positive theme on white, reverse on JHS Black (#231F20); accent red #C41230 in light, gold #FDB913 in dark; gold never as
  text on white, red never as text on black; header band is block-deep with the athletic face (Eurostile, falling back to
  Helvetica Neue) in gold, a 4 px JHS Red rule under it. Header and sign-in screen show the mascot mark Kevin supplied
  (2026-11-07) at 96 px (the guide's minimum logo width), inlined in the template CSS as a 192 px PNG (.jx-logo): the
  supplied art cropped to its circle with clear corners, otherwise unchanged. Never redraw or recolor the mark. Header
  subtitle is "Results and projections" (Kevin dropped "coaches only"). Radii 0-4 px. Jesuit rows get a light gold
  tint with a gold left edge.
- Tabs: Roster (rating = Willow Hills 5K today), Runner (chart of every race as a Willow Hills 5K on its day; history with
  the strict pre-meet expected time, shifted by how the rest of the field ran, and the 8-in-10 range), Meets (Report,
  Results, Team scores), Courses (course ratings from
  portal_data's courses block: each course and distance vs the Section finals course, weather-neutral, with a Willow Hills
  5K time box that converts to time there; filters Jesuit this season, Jesuit any year, all), Projections (Section finals and State for every current runner, distinct places by projected
  time), Simulation (section_sim.py results, shown when data has D.sims), Model (strict backtest).
- Team scores are unofficial: teams of 5+, top 5 score, 6th and 7th displace, exhibition and unattached left out.
- Before any commit: run ../pipeline/scripts/check_web_clean.py, which searches this repo for every athlete name in the
  master and any data file. It must report clean. Never write a runner's name here, even as an example.
- Serve local test pages only on 127.0.0.1 from the scratchpad, never the pipeline's portal/ folder, never all interfaces.
- Kevin prefers plain, direct writing: no em dashes, no filler.
