# NOTES — news-image-20261124 v1 (early edition)

- Built: Tue 24 Nov 2026, ~07:30–08:05 WIB (00:30–01:05 UTC), by subagent.
- Bounty: "Sum up 24 November's world news in one image", $100, 50 paid
  places. Entries opened 24 Nov 07:00 WIB; blind rounds 24 Nov 19:00 WIB,
  25 Nov 07:00 + 19:00 WIB, final 26 Nov 07:00 WIB; entries close
  26 Nov 07:00 WIB; results 8 Dec 2026.
- Quota at build: day cap 6, left 6, can_submit true. Field at build:
  submissionCount 903 (API, ~00:30 UTC).
- v1 = EARLY EDITION: 31 stories, 6 regions (EUROPE 2, MIDDLE EAST 3,
  ASIA 10, AFRICA 1, AMERICAS 3, OCEANIA 12). Every story verified as
  first reported Tue 24 Nov 2026 in some time zone; verification basis
  per story in BRIEF.md. The two biggest 23-Nov stories (Nvidia/Huang,
  COP31) appear ONLY in the 2-item DATE CHECK as excluded.
- Visual language: "night-desk atlas" — deep navy ground, cream cards,
  gold rules, dark world map. NOT the cream newspaper front page the
  field copies. 3 heroes + 10 illustrated cards + KPI strip + map with
  numbered pins 1–13 + dots 14–31 + ALSO ON list + DATE CHECK + sources.
- Render: 1024x1024 RGB PNG, 465,711 bytes, sha256
  79cb2e41146be67296d25a5b4395cb3de2666c97fa0cbe81676910c8b2fdb36f.
  Sharpened (UnsharpMask r2, 150%). preview-300.png included.
- Tests: 12/12 pass (python3 -m unittest discover -s tests), incl.
  determinism (two renders identical sha), clearance 0, main.py stdlib
  only, main.py copies byte-identical output as uid 65534 on a
  read-only repo copy.
- Visual fixes applied (3 passes): (1) timeline events were clipped by
  hero cards — band extended to 157, events moved up; featured cards
  had the region label drawn over the scene strip — badge row moved
  above the strip; KPI labels clipped by the bottom rule; footer
  sources line at the canvas edge. (2) featured source text failed the
  2px clearance test by 1px — scene strip shortened, headline moved
  up. (3) KPI numbers overlapped their labels — number 22px at y=620,
  label at y=645.
- main.py: pure stdlib, copies bundled entry.png to
  $MAKEFUN_OUTPUT_DIR/entry.png (else /output/entry.png, else
  output.png), chmod 0644.
- Lessons applied from NI22: 31 verified stories instead of padding
  to 50 with off-day stories (v2 fell 971,449 → 953,261 on that);
  DATE CHECK small and neutral; pins staggered where cities share
  coordinates (Doha/Tehran, Delhi x2, Melbourne/Sydney); Japan flash
  PMI numbers dropped (release only, no number — actuals unpublished
  at build time).
- NOT submitted. Submit needs Joni's 'Setuju' on the exact entry.
- Next: v2/v3 later in the day add verified daytime stories (German
  Ifo, UK–EU statement, US markets, evening wires) before the final
  round 26 Nov 07:00 WIB. Read the judge's hidden reasons after the
  live score before building v2.
