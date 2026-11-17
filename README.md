# MiniVIC Operation Manual

The operation manual of the **MiniVIC**, a W65C02S home computer with TMS9918A video,
two AY-3-8910 sound chips, a DIN5 keyboard, two joysticks, a serial port and an SD card.
Its layout and cover recall the 1976 Apple-1 Operation Manual: typewriter text, Bookman
headings, "SECTION I" chapter openings and an engraved plate on the cover.

## The PDFs

| File | Language | Edition |
|------|----------|---------|
| [MiniVIC_Manual_EN.pdf](MiniVIC_Manual_EN.pdf) | English | screen: cream paper, colour pictures |
| [MiniVIC_Manual_IT.pdf](MiniVIC_Manual_IT.pdf) | Italian | screen: cream paper, colour pictures |
| [MiniVIC_Manual_EN_print.pdf](MiniVIC_Manual_EN_print.pdf) | English | print: white paper, grey pictures |
| [MiniVIC_Manual_IT_print.pdf](MiniVIC_Manual_IT_print.pdf) | Italian | print: white paper, grey pictures |

The manual describes BIOS **16.11.26 KEYB/SD R2**:

- I. Overview: specification, memory map (with binary addresses), device map, address decoding
- II. The board: connectors, getting started
- III. Schematics: the ten pages of schematic v41
- IV. Bill of materials
- V. The devices: every register of the CPU, TMS9918A, W65C51 ACIA, the three W65C22 VIAs,
  keyboard, joysticks (with the DB9 pinout), SD card and AY-3-8910
- VI. Memory usage: the RAM used by the BIOS, the ROM, the jump table at $FD00
- VII. The BIOS and its menus
- VIII. The WozMon monitor
- IX. Microsoft BASIC
- X. The applications (WRITE, CALC, FILE, DESK, TERM, MON, DISK, ASM, JUKEBOX)
- XI. Games and music
- XII. The SD card format
- Appendix: emulator, firmware versions, links

## Building

The PDFs are made by the Python scripts in [build/](build/):

| File | Purpose |
|------|---------|
| `build.py` | builds the manuals: ReportLab lays out the text, PyMuPDF adds the schematic pages as vectors |
| `content.py` | the text, Italian and English side by side |
| `layout.py` | page layout, styles, helpers for headings, tables and pictures |
| `cover.py` | the cover, with the 6502 chip drawn as an engraving |
| `shots.ts`, `shots.mjs` | take the BIOS screenshots on the emulator core |

Requirements: Python 3 with `reportlab`, `pymupdf` and `pillow`; the Windows fonts Courier New
and Bookman Old Style. The scripts read the schematic, the photos and the screenshots from the
other MiniVIC projects, kept next to this folder:

```
miniVIC_65c02/        hardware: schematic, gallery
MiniVIC Apps/         application screenshots
MiniVIC Games/        game title screens
miniVIC BIOS/         BIOS image (for shots.mjs)
bo6502-emulator/      emulator core (for shots.mjs)
bo6502-SDbuilder/     SD card image (for shots.mjs)
```

```
python build/build.py                    # screen edition, IT and EN
MANUAL_PRINT=1 python build/build.py     # print edition
node build/shots.mjs                     # new BIOS screenshots into build/img/screens
```

## Related projects

- [miniVIC_65c02](https://github.com/Boogs77/miniVIC_65c02): hardware
- [miniVIC_bios](https://github.com/Boogs77/miniVIC_bios): BIOS
- [miniVIC_apps](https://github.com/Boogs77/miniVIC_apps): applications
- [miniVIC_games](https://github.com/Boogs77/miniVIC_games): games
- [miniVIC_music](https://github.com/Boogs77/miniVIC_music): music
- [BO6502-miniVIC-emulator](https://github.com/Boogs77/BO6502-miniVIC-emulator): browser emulator
