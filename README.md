# Canu Public Pages

Public support, privacy policy and terms pages for the iOS app Canu.

Entry points:

- `/` German support hub for Switzerland, EU and EEA
- `/de/`, `/en/`, `/es/`, `/fr/`, `/it/`, `/pt/` and `/ru/` localized support hubs
- `/international/` English support hub for the United States and other regions
- `/cn/` Simplified Chinese support hub for Mainland China

Regional legal URLs:

- `/ch/datenschutz/` and `/ch/nutzungsbedingungen/`
- `/eu/datenschutz/` and `/eu/nutzungsbedingungen/`
- `/us/privacy/` and `/us/terms/`
- `/cn/privacy/` and `/cn/terms/`
- `/international/privacy/` and `/international/terms/`
- `/de/copyright/`, `/international/copyright/` and `/cn/copyright/`

The app links directly to the correct regional path. The support hubs include
a language selector; the legal pages remain organized by applicable region.

## Landing pages

The support hubs (`/<language>/index.html` and `/autometronom/<language>/index.html`) are generated:

    python3 _build/build.py

Texts per language live in `_build/canu_strings.py` and `_build/am_strings.py`, the design in `styles.css`.
Legal pages are hand-written HTML that only share the stylesheet. `assets/store.js` shows AutoMetronom's
App Store button and the cross-link on the Canu pages once Apple's lookup lists the app.
