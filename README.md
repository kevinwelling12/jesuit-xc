# Jesuit XC portal (web)

The page template for the Jesuit High School Sacramento cross country results portal: race results, athlete histories,
championship projections and team scoring simulations for the coaching staff.

This repository holds code only. Athlete names and results are minors' data: they stay in a private pipeline and reach the
page only after a coach signs in (Firebase, coaches only). Nothing in this repo contains or links to that data.

- `templates/portal_template.html`: the portal. The private pipeline injects its data at `__DATA__`.
- `src/`: sign-in gate (coming with the Firebase setup).
