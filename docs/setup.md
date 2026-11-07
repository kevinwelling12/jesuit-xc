# Setup: signed-in web portal

The site is a static page on GitHub Pages. It holds no athlete data. After a coach signs in with Google, Firestore checks
`members/{email}` and only then lets the browser read the portal data, which the private pipeline uploads.

1. **Firebase project**: console.firebase.google.com > Add project (no Google Analytics needed).
2. **Google sign-in**: Build > Authentication > Get started > Sign-in method > Google > Enable.
3. **Firestore**: Build > Firestore Database > Create database, production mode, a US location. Then Rules: paste
   `firestore.rules` and Publish.
4. **Web app config**: Project settings > General > Your apps > Web (</>), any nickname, no Hosting. Copy the
   `firebaseConfig` values into `src/firebase-config.js` as `window.FIREBASE_CONFIG = {...}`.
5. **Service account key** (for publishing): Project settings > Service accounts > Generate new private key. Save it as
   `~/.config/jesuit-xc/firebase-admin.json`, outside iCloud and outside this repo. Never commit it.
6. **First admin**: `python3 scripts/publish_web.py --add <your email> admin` from ../pipeline.
7. **GitHub**: create the repo, push, Settings > Pages > Source: GitHub Actions. The workflow builds `dist/` on each push.
8. **Authorized domain**: Firebase Authentication > Settings > Authorized domains > add `<user>.github.io`.
9. **Publish data**: `python3 scripts/update.py --web` from ../pipeline.
10. **Checks**: signed out, an unauthenticated read of `portals/xc` must be denied; an email not on the list sees
    "Not on the list yet"; a member sees the portal.
