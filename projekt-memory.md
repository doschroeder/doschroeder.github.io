# Projekt-Memory: Website doschroeder.github.io

Laufender Stand aus Claude-Sessions. Updates gehören hierher, nicht in die
Haupt-`memory.md`. Migriert aus der Haupt-`memory.md` am 2026-08-25.
ACHTUNG: Diese Datei ist neu und noch nicht committet.

## Datenstand (`data/en/`)

`currentPositions.yml` und `teaching.yml` sind veraltet (noch FAU-Stand);
`employment.yml`, `projects.yml`, `publications.yml`, `PhDStudents.yml`,
`Postdocs.yml`, `awards.yml`, `pc.yml`, `pchairs.yml` sind brauchbar. Zwei Namen in
`editor.yml`/`journal.yml` waren vermutlich falsch geschrieben: korrekt heißen die
Journale "IACR Communications in Cryptology" (nicht "in Cryptography") und "ACM
Transactions on Privacy and Security" (nicht "on Security and Privacy"). Im IAB-CV
wurden die korrekten Namen verwendet.

## Änderungen vom 2026-08-24 (commit-bereit, noch nicht committet)

Vier geänderte Dateien: `editor.yml`, `journal.yml`, `projects.yml`,
`publications.yml`. Im Einzelnen: neue Publikation "Fair Distributed Exchange via
Threshold Adaptor Signatures" (Ruben Baecker, Paul Gerhart, Jonathan Katz,
Dominique Schroeder, ASIACRYPT 2026, https://eprint.iacr.org/2025/388.pdf) an den
Anfang des 2026-Blocks in `publications.yml` eingefügt (eprint.iacr.org blockt
automatisierte Zugriffe, Abstract manuell nachtragen, `has_info: false`); Editorial
Board IACR Communications in Cryptology auf "2024 - 2026" gesetzt (Tätigkeit
beendet, Endjahr von Claude auf 2026 gesetzt, noch nicht von Dominique bestätigt)
und aus der aktuellen Liste in `journal.yml` entfernt; in `projects.yml` der Google
Unrestricted Gift von `role: PI` auf `role: sole PI` korrigiert (Dominique ist
alleiniger PI).

## Änderungen vom 2026-09-01 (noch nicht committet)

Neue Publikation "Fully Adaptive FROST with Identifiable Aborts from AOMDL"
(Ruben Baecker, Paul Gerhart, Davide Li Calsi, Luigi Russo, Dominique Schröder,
Arkady Yerukhimovich, ASIACRYPT 2026, https://eprint.iacr.org/2025/1950.pdf) an
den Anfang des 2026-Blocks in `publications.yml` eingefügt (`has_info: false`,
Link von paul-gerhart.de/publications übernommen). Abstract am 2026-09-01 über
den Browser von der ePrint-Seite geholt und eingetragen (`has_info: true`).
Achtung: ePrint 2025/1950 trägt einen anderen Titel ("Fully Adaptive FROST in
the Algebraic Group Model From Falsifiable Assumptions", Revision 2025-11-12);
auf der Website steht der von Dominique genannte Titel "... with Identifiable
Aborts from AOMDL" (so auch bei Paul Gerhart). "Fair
Distributed Exchange" war bereits seit 2026-08-24 drin, nichts geändert.

## Änderungen vom 2026-09-15 (noch nicht committet)

Neue Publikation "BitPriv: A Privacy-Preserving Protocol for DeFi Applications
on Bitcoin" (Ioannis Alexopoulos, Zeta Avarikioti, Paul Gerhart, Matteo Maffei,
Dominique Schröder, NDSS 2027, https://eprint.iacr.org/2025/1575.pdf) als
neuer 2027-Block vor dem 2026-Block in `publications.yml` eingefügt
(Abstract am selben Tag von der ePrint-Seite geholt, `has_info: true`). Erster Eintrag mit
Jahr 2027. Die Änderungen vom 24.08. und 01.09. waren laut git log bereits committet (Commit "AC paper").
