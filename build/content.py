"""content.py - the text of the miniVIC manual, Italian and English side by side (T(it, en)).

Sources: miniVIC_65c02 (hardware, schematic v41, BOM), miniVIC BIOS (16.11.26 KEYB/SD R2: jumptable.s,
boot_menu_multi.s, keyboard_drv.s, sdcard_drv.s, crt_text_drv.s, KEYB_SD.md), MiniVIC Apps README,
MiniVIC Games README, MiniVIC Sound README, bo6502-SDbuilder README, SD_SALVATAGGI.md."""
from pathlib import Path
from layout import (H1, H2, H3, P, NOTE, B, CODE, TBL, IMG_, IMGROW, SPACE, PB, Placeholder, BODY_W, IMG,
                    SECTION_WORD, make_toc, NextPageTemplate, PageBreak, Spacer, Paragraph, S, mm)

ROOT = Path(__file__).resolve().parent.parent.parent
GALLERY = ROOT / 'miniVIC_65c02' / 'gallery'
APPSHOT = ROOT / 'MiniVIC Apps' / 'screenshots'
GAMESHOT = ROOT / 'MiniVIC Games' / 'screenshots'
SCREENS = IMG / 'screens'
SCHEMATIC = ROOT / 'miniVIC_65c02' / 'schematics' / 'miniVIC_C6502_v41.pdf'


def binw(v):
    s = format(v, '016b')
    return s[:4] + ' ' + s[4:8] + ' ' + s[8:12] + ' ' + s[12:]


def story(L):
    def T(it, en):
        return it if L == 'it' else en

    SECTION_WORD[0] = T('SEZIONE', 'SECTION')
    st = []
    add = st.extend

    # ================================================================ INDEX
    add(make_toc(T('INDICE', 'INDEX')))

    # ================================================================ I. OVERVIEW
    add(H1('I', T('Panoramica', 'Overview')))
    add(P(T(
        "Il <b>miniVIC</b> (Boogs77-miniVIC) è un computer a 8 bit compatto, pensato per i giochi, costruito su "
        "una sola scheda. Riprende l'architettura modulare del sistema <b>BO6502</b> e mette tutti i suoi moduli "
        "su un unico circuito stampato: una CPU <b>W65C02S</b>, un processore video <b>TMS9918A</b> con uscita "
        "composita, due chip sonori <b>AY-3-8910</b> per l'audio stereo, una tastiera DIN5, due joystick, una "
        "porta seriale e una scheda SD per i programmi.",
        "The <b>miniVIC</b> (Boogs77-miniVIC) is a compact, arcade-oriented 8-bit computer built on a single "
        "board. It takes the modular architecture of the <b>BO6502</b> system and puts all of its modules on one "
        "PCB: a <b>W65C02S</b> CPU, a <b>TMS9918A</b> video processor with composite output, two <b>AY-3-8910</b> "
        "sound chips for stereo audio, a DIN5 keyboard, two joysticks, a serial port and an SD card for programs.")))
    add(P(T(
        "Questo manuale descrive la macchina come la vede chi la usa: le specifiche, la mappa della memoria e "
        "di tutti i dispositivi, la scheda, lo schema elettrico, la distinta dei componenti e il funzionamento "
        "di tutto il software: il BIOS con il suo menu, il monitor WozMon, il Microsoft BASIC, gli applicativi "
        "e i giochi della scheda SD.",
        "This manual describes the machine as its user sees it: the specification, the map of the memory and "
        "of every device, the board, the schematic, the bill of materials and how all the software works: the "
        "BIOS with its menu, the WozMon monitor, Microsoft BASIC, and the applications and games on the SD card.")))

    add(H2(T('Specifiche', 'Specification')))
    spec = [
        (T('MICROPROCESSORE', 'MICROPROCESSOR'), 'The Western Design Center W65C02S'),
        (T('   Frequenza di clock', '   Clock frequency'), T('1,0 MHz (oscillatore QG1)', '1.0 MHz (oscillator QG1)')),
        (T('MEMORIA ROM', 'ROM MEMORY'), T('28C256 (CAT28C256P) su zoccolo ZIF', '28C256 (CAT28C256P) on a ZIF socket')),
        (T('   Capacità', '   Capacity'), T('32 Kbyte, $8000-$FFFF', '32 Kbyte, $8000-$FFFF')),
        (T('MEMORIA RAM', 'RAM MEMORY'), 'HITACHI HM62256'),
        (T('   Capacità', '   Capacity'), T('32 Kbyte, $0000-$7FFF', '32 Kbyte, $0000-$7FFF')),
        (T('USCITA VIDEO', 'VIDEO OUTPUT'), T('Composito, connettore RCA', 'Composite, RCA connector')),
        (T('   Chip', '   Chip'), T('TI TMS9918A, quarzo 10,738635 MHz', 'TI TMS9918A, 10.738635 MHz crystal')),
        (T('   VRAM', '   VRAM'), T('16 Kbyte su HM62256', '16 Kbyte on an HM62256')),
        (T('   Modi', '   Modes'), T('testo 40x24, grafica 256x192, 15 colori, 32 sprite',
                                      'text 40x24, graphics 256x192, 15 colours, 32 sprites')),
        (T('AUDIO', 'AUDIO'), T('2 x GI AY-3-8910, stereo, 6 voci', '2 x GI AY-3-8910, stereo, 6 voices')),
        (T('   Uscite', '   Outputs'), T('2 connettori RCA (sinistro, destro)', '2 RCA connectors (left, right)')),
        (T('COMUNICAZIONE SERIALE', 'SERIAL COMMUNICATION'), T('W65C51 ACIA + MAX232, connettore DB9',
                                                                'W65C51 ACIA + MAX232, DB9 connector')),
        ('', T('19200 baud, 8 bit, nessuna parità, 1 bit di stop', '19200 baud, 8 bits, no parity, 1 stop bit')),
        (T('TASTIERA', 'KEYBOARD'), T('DIN5, layout US, tramite W65C22 VIA', 'DIN5, US layout, through a W65C22 VIA')),
        (T('JOYSTICK', 'JOYSTICKS'), T('2 porte DB9, tipo Sega Master System', '2 DB9 ports, Sega Master System type')),
        (T('MEMORIA DI MASSA', 'MASS STORAGE'), T('scheda SD (SDSC v1/v2, SDHC), SPI su W65C22',
                                                   'SD card (SDSC v1/v2, SDHC), SPI on a W65C22')),
        (T('ALIMENTAZIONE', 'POWER SUPPLY'), T('5 V DC stabilizzati, presa jack, LED di accensione',
                                               '5 V DC regulated, barrel jack, power LED')),
        ('FIRMWARE', T('BIOS 16.11.26 KEYB/SD R2: WozMon, Microsoft BASIC 1977, menu programmi SD',
                       'BIOS 16.11.26 KEYB/SD R2: WozMon, Microsoft BASIC 1977, SD programs menu')),
    ]
    add(TBL([[Paragraph(a, S['cellb'] if not a.startswith('   ') else S['cell']), b] for a, b in spec],
            [0.38, 0.62], header=False))

    add(H2(T('Mappa della memoria', 'Memory map')))
    add(P(T(
        "Lo spazio di indirizzamento della CPU è di 64 Kbyte. La metà bassa è RAM; la metà alta è la ROM, "
        "tranne la finestra <b>$B000-$DFFF</b>, che la logica di decodifica assegna ai dispositivi di "
        "ingresso e uscita. La tabella segue lo stile del manuale BO6502, con gli indirizzi anche in binario.",
        "The CPU address space is 64 Kbyte. The lower half is RAM; the upper half is the ROM, except the window "
        "<b>$B000-$DFFF</b>, which the decoding logic gives to the input and output devices. The table follows "
        "the style of the BO6502 manual, with the addresses in binary too.")))
    mm_rows = [
        ('RAM', 'ZEROPAGE', 0x0000, 0x00FF, T('pagina zero: BASIC, BIOS, WozMon', 'zero page: BASIC, BIOS, WozMon')),
        ('', 'STACK', 0x0100, 0x01FF, T('stack della CPU', 'CPU stack')),
        ('', 'IN BUFFER', 0x0200, 0x02FF, T('buffer di riga di WozMon ($0200-$027F)', 'WozMon line buffer ($0200-$027F)')),
        ('', 'BIOS VARS', 0x0300, 0x03FF, T('variabili BIOS, buffer tastiera $0380', 'BIOS variables, keyboard buffer $0380')),
        ('', 'BASRAM', 0x0400, 0x0EFF, T('programma BASIC (da $0400)', 'BASIC program (from $0400)')),
        ('', 'VECTORS', 0x0F00, 0x0FFF, T('trampolini IRQ $0FA0, NMI $0FD0', 'IRQ $0FA0 and NMI $0FD0 trampolines')),
        ('', 'PROGRAM', 0x1000, 0x7FFF, T('programmi caricati dalla SD', 'programs loaded from the SD')),
        ('ROM', 'BASROM', 0x8000, 0xAFFF, T('Microsoft BASIC e driver del BIOS', 'Microsoft BASIC and BIOS drivers')),
        ('I/O', 'VDU', 0xB000, 0xBFFF, T('TMS9918A ($B000-$B001)', 'TMS9918A ($B000-$B001)')),
        ('', 'SERIAL', 0xC000, 0xCFFF, T('W65C51 ($C000-$C003)', 'W65C51 ($C000-$C003)')),
        ('', 'I/O', 0xD000, 0xDFFF, T('tastiera, audio, joystick, SD', 'keyboard, audio, joysticks, SD')),
        ('ROM', 'PROGRAM', 0xE000, 0xFCFF, T('menu di avvio e BIOS', 'boot menu and BIOS')),
        ('', 'JUMPTBL', 0xFD00, 0xFDFF, T('tabella dei salti del sistema', 'system jump table')),
        ('', 'WOZMON', 0xFE00, 0xFFF9, T('monitor WozMon', 'WozMon monitor')),
        ('', 'VECTORS', 0xFFFA, 0xFFFF, 'NMI, RESET, IRQ'),
    ]
    rows = [[T('AREA', 'AREA'), T('USO', 'PURPOSE'), T('INIZ.', 'START'), T('FINE', 'END'), T('DIM.', 'SIZE'),
             T('COMMENTI', 'COMMENTS'), T('INIZIO BINARIO', 'BINARY START'), T('FINE BINARIO', 'BINARY END')]]
    for a, p_, s_, e_, cmt in mm_rows:
        size = e_ - s_ + 1
        sz = f'{size // 1024}K' if size % 1024 == 0 and size >= 1024 else str(size)
        rows.append([a, p_, f'${s_:04X}', f'${e_:04X}', sz, cmt, binw(s_), binw(e_)])
    add(TBL(rows, [0.06, 0.10, 0.08, 0.07, 0.06, 0.25, 0.19, 0.19], center_cols=(2, 3, 4), font=7))

    add(H2(T('Mappa dei dispositivi', 'Device map')))
    add(P(T(
        "Ogni dispositivo risponde a pochi indirizzi della finestra di I/O. Sono gli stessi che il BIOS mostra "
        "nella pagina <i>System Information</i>. Il valore decimale serve per <b>PEEK</b> e <b>POKE</b> dal BASIC.",
        "Every device answers a few addresses of the I/O window. They are the same that the BIOS shows on the "
        "<i>System Information</i> page. The decimal value is for <b>PEEK</b> and <b>POKE</b> from BASIC.")))
    dev = [[T('DISPOSITIVO', 'DEVICE'), 'CHIP', T('INDIRIZZI', 'ADDRESSES'), T('DECIMALE', 'DECIMAL'),
            T('INTERRUZIONE', 'INTERRUPT')],
           [T('Video (VDU)', 'Video (VDU)'), 'TMS9918A', '$B000-$B001', '45056-45057', 'NMI'],
           [T('Seriale', 'Serial'), 'W65C51 ACIA', '$C000-$C003', '49152-49155', 'IRQ'],
           [T('Tastiera', 'Keyboard'), 'W65C22 VIA', '$D180-$D18F', '53632-53647', T('IRQ (non usato)', 'IRQ (unused)')],
           ['Audio', '2x AY-3-8910', '$D380-$D381 R, $D384-$D385 L', '54144-54145, 54148-54149', '-'],
           ['Joystick', 'W65C22 VIA', '$D580-$D58F', '54656-54671', 'IRQ'],
           [T('Scheda SD', 'SD card'), 'W65C22 VIA', '$DD80-$DD8F', '56704-56719', 'IRQ'],
           ]
    add(TBL(dev, [0.16, 0.16, 0.27, 0.25, 0.16]))
    add(H3(T('Decodifica degli indirizzi', 'Address decoding')))
    add(P(T(
        "La ROM è attiva su <b>$8000-$AFFF</b> e su <b>$E000-$FFFF</b>. Un 74AC138 (IC54, ingressi A12-A14, "
        "abilitato da A15) divide la metà alta in blocchi da 4 Kbyte: <b>$Bxxx</b> va al video, <b>$Cxxx</b> "
        "alla seriale, <b>$Dxxx</b> alle altre schede. Dentro $Dxxx, IC55 (A9-A11, abilitato da A8) sceglie la "
        "scheda e IC56 (A4-A7) la riga <b>$Dx80</b>. Video e seriale rispondono in tutto il loro blocco "
        "(gli stessi registri si ripetono); per le schede in $Dxxx usate solo gli indirizzi della tabella.",
        "The ROM is enabled on <b>$8000-$AFFF</b> and on <b>$E000-$FFFF</b>. A 74AC138 (IC54, inputs A12-A14, "
        "enabled by A15) splits the upper half into 4 Kbyte blocks: <b>$Bxxx</b> goes to the video, <b>$Cxxx</b> "
        "to the serial port, <b>$Dxxx</b> to the other boards. Inside $Dxxx, IC55 (A9-A11, enabled by A8) picks "
        "the board and IC56 (A4-A7) the <b>$Dx80</b> row. Video and serial answer in their whole block (the same "
        "registers repeat); for the boards in $Dxxx use only the addresses of the table.")))

    # ================================================================ II. THE BOARD
    add(H1('II', T('La scheda', 'The board')))
    add(P(T(
        "Tutta la macchina sta su una scheda singola, \"C6502 COMMODORE MINIVIC ver 1.0\" (schema C6502 v41). "
        "Ogni sezione della scheda segue il progetto elettrico e logico di un modulo BO6502.",
        "The whole machine is on a single board, \"C6502 COMMODORE MINIVIC ver 1.0\" (schematic C6502 v41). "
        "Every section of the board follows the electrical and logical design of a BO6502 module.")))
    add(IMG_(GALLERY / 'miniVIC_pcb_top.png', 160, T('La scheda vista dall\'alto (render, PCB ver 1.0).',
                                                     'The board seen from above (render, PCB ver 1.0).'), border=False))
    add(IMG_(GALLERY / 'miniVIC_pcb_3d.png', 150, T('Render 3D della scheda.', '3D render of the board.'), border=False))
    add(IMG_(GALLERY / 'miniVIC_pcb_layout.png', 150, T('Disposizione delle piste in rame.', 'Copper layout.'), border=False))

    add(H2(T('Connettori', 'Connectors')))
    con = [[T('CONNETTORE', 'CONNECTOR'), T('FUNZIONE', 'FUNCTION')],
           [T('Presa jack DC', 'DC barrel jack'), T('alimentazione 5 V stabilizzati; LED di accensione accanto',
                                                    '5 V regulated power; power LED next to it')],
           [T('Pulsante RESET', 'RESET button'), T('riavvia la CPU (circuito NE555): si torna al menu del BIOS',
                                                  'restarts the CPU (NE555 circuit): back to the BIOS menu')],
           ['RCA VIDEO', T('video composito per un televisore o un monitor', 'composite video for a TV set or a monitor')],
           ['RCA AUDIO LEFT / RIGHT', T('audio stereo: sinistro = AY a $D384, destro = AY a $D380',
                                        'stereo audio: left = AY at $D384, right = AY at $D380')],
           [T('DB9 SERIALE', 'DB9 SERIAL'), T('RS-232 (MAX232), 19200 8N1, verso un PC o un terminale',
                                             'RS-232 (MAX232), 19200 8N1, to a PC or a terminal')],
           ['DB9 JOY 1 / JOY 2', T('due joystick tipo Sega Master System (su, giù, sinistra, destra, 2 pulsanti)',
                                   'two Sega Master System type joysticks (up, down, left, right, 2 buttons)')],
           [T('Tastiera DIN5', 'DIN5 keyboard'), T('tastiera DIN5 con layout US', 'DIN5 keyboard, US layout')],
           [T('Modulo SD', 'SD module'), T('pettine per un modulo con scheda SD', 'header for an SD card module')],
           [T('Zoccolo ZIF', 'ZIF socket'), T('EEPROM 28C256 del firmware: si cambia senza attrezzi',
                                              '28C256 firmware EEPROM: it can be changed without tools')],
           [T('Espansione', 'Expansion'), T('pettini con bus indirizzi, bus dati, PHI0 e le linee libere della VIA della SD',
                                            'headers with the address bus, the data bus, PHI0 and the free lines of the SD VIA')],
           ]
    add(TBL(con, [0.30, 0.70]))

    add(H2(T('Per cominciare', 'Getting started')))
    add(B([
        T("Collegate il televisore all'uscita <b>VIDEO</b> e, se volete il suono, le uscite <b>AUDIO</b> a un amplificatore.",
          "Connect the TV set to the <b>VIDEO</b> output and, for sound, the <b>AUDIO</b> outputs to an amplifier."),
        T("Collegate la tastiera DIN5 e, per i giochi, uno o due joystick.",
          "Connect the DIN5 keyboard and, for the games, one or two joysticks."),
        T("Inserite la scheda SD preparata con <b>bo6502-SDbuilder</b> (capitolo XI).",
          "Insert the SD card prepared with <b>bo6502-SDbuilder</b> (chapter XI)."),
        T("Facoltativo: collegate la porta seriale a un PC con un programma terminale a 19200 baud, 8N1.",
          "Optional: connect the serial port to a PC with a terminal program at 19200 baud, 8N1."),
        T("Date alimentazione (5 V): il LED si accende e dopo un istante compare il menu del BIOS.",
          "Apply power (5 V): the LED lights up and after a moment the BIOS menu appears."),
    ]))
    add(NOTE(T(
        "<b>Nota.</b> Il pulsante RESET riporta sempre al menu del BIOS. È l'unico modo per uscire da WozMon "
        "e dal BASIC; il contenuto della RAM non viene cancellato.",
        "<b>Note.</b> The RESET button always goes back to the BIOS menu. It is the only way out of WozMon and "
        "BASIC; the contents of the RAM are not erased.")))

    # ================================================================ III. SCHEMATICS
    add(H1('III', T('Schema elettrico', 'Schematics')))
    add(P(T(
        "Lo schema completo è <b>miniVIC_C6502_v41.pdf</b>, nella cartella <i>schematics</i> del repository "
        "miniVIC_65c02 (https://github.com/Boogs77/miniVIC_65c02). Le pagine seguenti lo riportano per intero, "
        "una pagina dello schema per pagina del manuale, ruotate per leggerle in orizzontale.",
        "The full schematic is <b>miniVIC_C6502_v41.pdf</b>, in the <i>schematics</i> folder of the miniVIC_65c02 "
        "repository (https://github.com/Boogs77/miniVIC_65c02). The following pages show all of it, one schematic "
        "page per manual page, rotated to be read in landscape.")))
    import pymupdf
    n = pymupdf.open(SCHEMATIC).page_count
    for i in range(n):
        add(PB())
        add([Paragraph(T('SCHEMA', 'SCHEMATIC') + f' {i + 1}/{n}', S['h3'])])
        add([Placeholder(f'schem{i}', 230 * mm)])

    # ================================================================ IV. BOM
    add(H1('IV', T('Distinta dei componenti', 'Bill of materials')))
    bom = [[T('COMPONENTE', 'COMPONENT'), T('DESCRIZIONE', 'DESCRIPTION'), T('Q.TÀ', 'QTY')],
           ['W65C02S', T('microprocessore CMOS a 8 bit', 'CMOS 8-bit microprocessor'), '1'],
           ['HM62256', T('RAM statica 32K x 8 (RAM e VRAM)', '32K x 8 static RAM (RAM and VRAM)'), '2'],
           ['28C256', T('EEPROM 32K x 8 (su zoccolo ZIF a 28 piedini)', '32K x 8 EEPROM (on a 28-pin ZIF socket)'), '1'],
           ['TMS9918A', T('processore video (VDP)', 'video display processor (VDP)'), '1'],
           ['AY-3-8910', T('generatore di suoni programmabile (PSG)', 'programmable sound generator (PSG)'), '2'],
           ['W65C22 (VIA)', T('interfaccia parallela (tastiera, joystick, SD)', 'versatile interface adapter (keyboard, joysticks, SD)'), '3'],
           ['W65C51 (ACIA)', T('interfaccia seriale asincrona', 'asynchronous communications interface adapter'), '1'],
           ['MAX232', T('driver di linea RS-232', 'RS-232 line driver'), '1'],
           ['NE555', T('timer (circuito di reset)', 'timer (reset circuit)'), '1'],
           ['74AC138', T('decodificatore 3 a 8', '3-to-8 decoder'), '7'],
           ['74HC08', T('4 porte AND', 'quad AND gate'), '4'],
           ['74HCT00', T('4 porte NAND', 'quad NAND gate'), '2'],
           ['74HC32', T('4 porte OR', 'quad OR gate'), '1'],
           ['74HCT04 / 74HC04', T('6 invertitori', 'hex inverter'), '1 + 1'],
           ['74HCT14', T('6 invertitori a trigger di Schmitt', 'hex Schmitt trigger inverter'), '1'],
           ['74HCT595', T('registro a scorrimento a 8 bit (tastiera DIN5)', '8-bit shift register (DIN5 keyboard)'), '2'],
           ['74HC574', T('8 flip-flop D (indirizzi della VRAM)', 'octal D flip-flop (VRAM address)'), '2'],
           ['74HC245', T('transceiver di bus a 8 bit (dati della VRAM)', 'octal bus transceiver (VRAM data)'), '1'],
           ['2N4401', T('transistor NPN (uscita video)', 'NPN transistor (video output)'), '1'],
           [T('Oscillatore', 'Oscillator'), '1 MHz', '1'],
           [T('Quarzi', 'Crystals'), T('10,738635 MHz (video), 1,8432 MHz (seriale)', '10.738635 MHz (video), 1.8432 MHz (serial)'), '1 + 1'],
           [T('Connettori', 'Connectors'), T('DB9 (seriale, 2 joystick), RCA (video, 2 audio), tastiera DIN5, modulo SD, jack DC',
                                             'DB9 (serial, 2 joysticks), RCA (video, 2 audio), DIN5 keyboard, SD card module, DC jack'), '-'],
           ]
    add(TBL(bom, [0.24, 0.64, 0.12], center_cols=(2,)))

    # ================================================================ V. HARDWARE REFERENCE
    add(H1('V', T('I dispositivi', 'The devices')))
    add(P(T(
        "Questa sezione descrive ogni dispositivo come lo vede un programma: gli indirizzi, i registri e il "
        "modo in cui il BIOS li imposta.",
        "This section describes every device as a program sees it: the addresses, the registers and the way "
        "the BIOS sets them up.")))

    add(H2(T('CPU, vettori e interruzioni', 'CPU, vectors and interrupts')))
    add(P(T(
        "La CPU è una W65C02S a 1 MHz: ha tutte le istruzioni del 65C02, comprese <b>RMB SMB BBR BBS</b>, "
        "<b>WAI</b> e <b>STP</b>. Il segnale INT del video va su <b>NMI</b> (60 volte al secondo, se abilitato); "
        "le tre VIA e l'ACIA condividono <b>IRQ</b> attraverso diodi Schottky.",
        "The CPU is a W65C02S at 1 MHz: it has the whole 65C02 instruction set, including <b>RMB SMB BBR BBS</b>, "
        "<b>WAI</b> and <b>STP</b>. The INT signal of the video drives <b>NMI</b> (60 times a second, when "
        "enabled); the three VIAs and the ACIA share <b>IRQ</b> through Schottky diodes.")))
    vec = [[T('VETTORE', 'VECTOR'), T('INDIRIZZO', 'ADDRESS'), T('PUNTA A', 'POINTS TO'), T('COSA FA', 'WHAT IT DOES')],
           ['NMI', '$FFFA-$FFFB', '$A7B0', T('salva A, X, Y; JSR $0FD0; legge lo stato del VDP ($B001); RTI',
                                             'saves A, X, Y; JSR $0FD0; reads the VDP status ($B001); RTI')],
           ['RESET', '$FFFC-$FFFD', '$E208', T('avvio: inizializza i dispositivi e mostra il menu',
                                               'start-up: sets up the devices and shows the menu')],
           ['IRQ/BRK', '$FFFE-$FFFF', '$AA01', T('salva A, X, Y; JSR $0FA0; RTI', 'saves A, X, Y; JSR $0FA0; RTI')],
           ]
    add(TBL(vec, [0.13, 0.17, 0.12, 0.58]))
    add(P(T(
        "Un programma che usa le interruzioni scrive la sua routine (che termina con <b>RTS</b>) ai "
        "trampolini in RAM <b>$0FD0</b> (NMI) e <b>$0FA0</b> (IRQ). I giochi e gli applicativi sono file che "
        "iniziano a $0FD0, quindi caricano il trampolino insieme al programma. Gli indirizzi a cui puntano i "
        "vettori possono cambiare con una nuova versione del BIOS: i programmi non devono usarli.",
        "A program that uses interrupts writes its routine (ending with <b>RTS</b>) at the RAM trampolines "
        "<b>$0FD0</b> (NMI) and <b>$0FA0</b> (IRQ). Games and applications are files that start at $0FD0, so "
        "they load the trampoline together with the program. The addresses the vectors point to can change with "
        "a new BIOS version: programs must not use them.")))

    # ---------------- VDP
    add(H2(T('Video: TMS9918A', 'Video: TMS9918A')))
    add(P(T(
        "Il VDP ha due porte: <b>$B000</b> (dati, A0=0) e <b>$B001</b> (registri e stato, A0=1). Ha 16 Kbyte "
        "di VRAM propria, che la CPU vede solo attraverso queste porte. Genera un quadro NTSC a 60 Hz: "
        "256x192 pixel, 15 colori più il trasparente, 32 sprite.",
        "The VDP has two ports: <b>$B000</b> (data, A0=0) and <b>$B001</b> (registers and status, A0=1). It has "
        "16 Kbyte of its own VRAM, which the CPU sees only through these ports. It makes an NTSC picture at "
        "60 Hz: 256x192 pixels, 15 colours plus transparent, 32 sprites.")))
    vdp_ops = [[T('OPERAZIONE', 'OPERATION'), T('SCRITTURE', 'WRITES')],
               [T('scrivere il registro n', 'write register n'), T('valore in $B001, poi $80+n in $B001', 'value to $B001, then $80+n to $B001')],
               [T('preparare la scrittura in VRAM', 'set up a VRAM write'), T('indirizzo basso in $B001, poi alto+$40 in $B001', 'low address to $B001, then high+$40 to $B001')],
               [T('preparare la lettura dalla VRAM', 'set up a VRAM read'), T('indirizzo basso in $B001, poi alto in $B001', 'low address to $B001, then high to $B001')],
               [T('scrivere / leggere i dati', 'write / read data'), T('$B000; l\'indirizzo avanza da solo', '$B000; the address advances by itself')],
               [T('leggere lo stato', 'read the status'), T('leggere $B001 (azzera F e la richiesta di interruzione)', 'read $B001 (clears F and the interrupt request)')],
               ]
    add(TBL(vdp_ops, [0.38, 0.62]))
    regs = [[T('REG.', 'REG.'), T('BIT', 'BITS'), T('VALORE BIOS', 'BIOS VALUE'), T('SIGNIFICATO', 'MEANING')],
            ['R0', 'bit 1 M3, bit 0 EXTVID', '$00', T('modo (M3 = Graphics II)', 'mode (M3 = Graphics II)')],
            ['R1', T('7 16K, 6 BLANK, 5 IE, 4 M1, 3 M2, 1 SIZE, 0 MAG', '7 16K, 6 BLANK, 5 IE, 4 M1, 3 M2, 1 SIZE, 0 MAG'), '$D0',
             T('16K, schermo acceso, modo testo, interruzione spenta', '16K, display on, text mode, interrupt off')],
            ['R2', T('indirizzo tabella dei nomi / $400', 'name table address / $400'), '$02', T('nomi a $0800', 'names at $0800')],
            ['R3', T('tabella dei colori / $40', 'colour table / $40'), '$00', T('non usata nel modo testo', 'not used in text mode')],
            ['R4', T('tabella dei caratteri / $800', 'pattern table / $800'), '$00', T('caratteri a $0000', 'patterns at $0000')],
            ['R5', T('attributi sprite / $80', 'sprite attributes / $80'), '$20', T('$1000 (sprite non usati)', '$1000 (no sprites in text mode)')],
            ['R6', T('disegni sprite / $800', 'sprite patterns / $800'), '$00', '$0000'],
            ['R7', T('colore testo (4 alti), sfondo (4 bassi)', 'text colour (high 4), backdrop (low 4)'), '$F5',
             T('bianco su azzurro', 'white on light blue')],
            ]
    add(TBL(regs, [0.07, 0.38, 0.14, 0.41], center_cols=(0, 2)))
    add(P(T(
        "Stato ($B001 in lettura): bit 7 <b>F</b> (fine quadro, 60 Hz), bit 6 <b>5S</b> (quinto sprite su una "
        "riga), bit 5 <b>C</b> (collisione tra sprite), bit 0-4 numero del quinto sprite. Il BIOS lascia "
        "l'interruzione spenta; un gioco la accende con il bit 5 di R1 e riceve una NMI per quadro.",
        "Status ($B001 read): bit 7 <b>F</b> (end of frame, 60 Hz), bit 6 <b>5S</b> (fifth sprite on a line), "
        "bit 5 <b>C</b> (sprite collision), bits 0-4 number of the fifth sprite. The BIOS leaves the interrupt "
        "off; a game turns it on with bit 5 of R1 and gets one NMI per frame.")))
    add(H3(T('VRAM nel modo testo del BIOS', 'VRAM in the BIOS text mode')))
    vram = [[T('INDIRIZZO VRAM', 'VRAM ADDRESS'), T('CONTENUTO', 'CONTENTS')],
            ['$0000-$07FF', T('tabella dei caratteri: 256 caratteri da 8 byte (6x8 pixel visibili). Gli applicativi usano 128-255 per il testo in negativo',
                              'pattern table: 256 characters of 8 bytes (6x8 visible pixels). The applications use 128-255 for inverse text')],
            ['$0800-$0BBF', T('tabella dei nomi: 40 colonne x 24 righe = 960 byte; il carattere della riga r, colonna c è a $0800 + r*40 + c',
                              'name table: 40 columns x 24 rows = 960 bytes; the character of row r, column c is at $0800 + r*40 + c')],
            ['$0BC0-$3FFF', T('libera (lo Z-Machine di Zork la usa come cache)', 'free (the Zork Z-Machine uses it as a cache)')],
            ]
    add(TBL(vram, [0.22, 0.78]))
    pal = [[T('N.', 'NO.'), T('COLORE', 'COLOUR'), T('N.', 'NO.'), T('COLORE', 'COLOUR'), T('N.', 'NO.'), T('COLORE', 'COLOUR'), T('N.', 'NO.'), T('COLORE', 'COLOUR')]]
    names = T('trasparente,nero,verde medio,verde chiaro,blu scuro,azzurro,rosso scuro,ciano,rosso medio,rosso chiaro,giallo scuro,giallo chiaro,verde scuro,magenta,grigio,bianco',
              'transparent,black,medium green,light green,dark blue,light blue,dark red,cyan,medium red,light red,dark yellow,light yellow,dark green,magenta,grey,white').split(',')
    for r in range(4):
        row = []
        for c in range(4):
            k = c * 4 + r
            row += [str(k), names[k]]
        pal.append(row)
    add(H3(T('I 16 colori', 'The 16 colours')))
    add(TBL(pal, [0.06, 0.19] * 4, center_cols=(0, 2, 4, 6)))
    add(P(T(
        "I giochi usano il modo <b>Graphics II</b> (256x192, due colori per ogni riga di 8 pixel) e gli sprite; "
        "Missile Command e Lunar Lander usano lo schermo come una bitmap intera.",
        "The games use <b>Graphics II</b> mode (256x192, two colours for every 8-pixel row) and sprites; Missile "
        "Command and Lunar Lander use the screen as a full bitmap.")))

    # ---------------- ACIA
    add(H2(T('Seriale: W65C51 ACIA', 'Serial: W65C51 ACIA')))
    acia = [[T('INDIRIZZO', 'ADDRESS'), T('REGISTRO', 'REGISTER'), T('NOTE', 'NOTES')],
            ['$C000', T('dati', 'data'), T('scrittura: byte da trasmettere; lettura: byte ricevuto', 'write: byte to send; read: byte received')],
            ['$C001', T('stato', 'status'), T('bit 3 = byte ricevuto, bit 4 = trasmettitore vuoto, bit 0-2 errori, bit 7 IRQ',
                                               'bit 3 = byte received, bit 4 = transmitter empty, bits 0-2 errors, bit 7 IRQ')],
            ['$C002', T('comando', 'command'), T('BIOS: $8B = nessuna parità, nessuna eco, interruzioni spente, DTR attivo',
                                                  'BIOS: $8B = no parity, no echo, interrupts off, DTR on')],
            ['$C003', T('controllo', 'control'), T('BIOS: $1F = 19200 baud, 8 bit, 1 bit di stop', 'BIOS: $1F = 19200 baud, 8 bits, 1 stop bit')],
            ]
    add(TBL(acia, [0.13, 0.15, 0.72]))
    add(P(T(
        "Il quarzo è da 1,8432 MHz. Il bit 4 di stato della W65C51 non è affidabile: il BIOS, dopo ogni byte "
        "trasmesso, aspetta con un ciclo di ritardo fisso invece di leggerlo. Tutto quello che il BIOS scrive "
        "sullo schermo (menu, WozMon, BASIC) esce anche dalla seriale, e i tasti ricevuti dalla seriale valgono "
        "come quelli della tastiera.",
        "The crystal is 1.8432 MHz. Status bit 4 of the W65C51 is not reliable: after every byte sent the BIOS "
        "waits with a fixed delay loop instead of reading it. Everything the BIOS writes on the screen (menu, "
        "WozMon, BASIC) also goes out of the serial port, and the keys received from the serial port count as "
        "keyboard keys.")))

    # ---------------- VIA generic
    add(H2(T('Le tre VIA W65C22', 'The three W65C22 VIAs')))
    add(P(T(
        "Tastiera, joystick e scheda SD hanno ciascuno una W65C22. I 16 registri sono uguali per tutte e tre; "
        "l'indirizzo è base + numero del registro.",
        "Keyboard, joysticks and SD card have one W65C22 each. The 16 registers are the same for the three of "
        "them; the address is base + register number.")))
    via = [[T('REG.', 'REG.'), T('NOME', 'NAME'), T('TASTIERA', 'KEYBOARD'), 'JOYSTICK', 'SD', T('FUNZIONE', 'FUNCTION')]]
    vn = [('0', 'ORB/IRB', T('porta B', 'port B')), ('1', 'ORA/IRA', T('porta A (con handshake)', 'port A (with handshake)')),
          ('2', 'DDRB', T('direzione porta B (1 = uscita)', 'port B direction (1 = output)')),
          ('3', 'DDRA', T('direzione porta A', 'port A direction')), ('4', 'T1C-L', 'timer 1'), ('5', 'T1C-H', 'timer 1'),
          ('6', 'T1L-L', T('latch timer 1', 'timer 1 latch')), ('7', 'T1L-H', T('latch timer 1', 'timer 1 latch')),
          ('8', 'T2C-L', 'timer 2'), ('9', 'T2C-H', 'timer 2'), ('A', 'SR', T('registro a scorrimento', 'shift register')),
          ('B', 'ACR', T('controllo ausiliario', 'auxiliary control')), ('C', 'PCR', T('controllo periferiche (CA1, CA2, CB1, CB2)', 'peripheral control (CA1, CA2, CB1, CB2)')),
          ('D', 'IFR', T('flag di interruzione', 'interrupt flags')), ('E', 'IER', T('abilitazione interruzioni', 'interrupt enable')),
          ('F', 'ORA', T('porta A senza handshake', 'port A, no handshake'))]
    for r, name, fn in vn:
        k = int(r, 16)
        via.append(['$' + r, name, f'$D18{r}', f'$D58{r}', f'$DD8{r}', fn])
    add(TBL(via, [0.07, 0.13, 0.13, 0.13, 0.12, 0.42], center_cols=(0, 2, 3, 4), font=7.4))

    add(H3(T('Tastiera DIN5 ($D180)', 'DIN5 keyboard ($D180)')))
    add(P(T(
        "La tastiera si collega al connettore <b>DIN a 5 poli</b> (tastiere AT; una tastiera PS/2 va bene con un "
        "adattatore passivo). Due 74HCT595 raccolgono i bit seriali della tastiera: ogni codice di scansione completo arriva "
        "sulla porta A (<b>$D181</b>) e la linea <b>CA1</b> segnala che è pronto (bit 1 di IFR, <b>$D18D</b>). "
        "Il BIOS legge la tastiera per polling, senza interruzioni, la decodifica e mette i caratteri in un "
        "buffer circolare di 128 byte a <b>$0380-$03FF</b>. Il VIA tiene solo l'ultimo byte: se un programma non "
        "legge per molto tempo, i tasti si perdono.",
        "The keyboard plugs into the <b>5-pin DIN</b> connector (AT keyboards; a PS/2 keyboard works through a "
        "passive adapter). Two 74HCT595 collect the serial bits of the keyboard: every complete scancode arrives on port A "
        "(<b>$D181</b>) and the <b>CA1</b> line says it is ready (bit 1 of IFR, <b>$D18D</b>). The BIOS reads "
        "the keyboard by polling, without interrupts, decodes it and puts the characters into a 128-byte ring "
        "buffer at <b>$0380-$03FF</b>. The VIA keeps only the last byte: if a program does not read for a long "
        "time, keys are lost.")))

    add(H3(T('Joystick ($D580)', 'Joysticks ($D580)')))
    joy = [[T('BIT', 'BIT'), T('SEGNALE', 'SIGNAL'), T('VALORE', 'VALUE')],
           ['0', T('su', 'up'), T('0 = premuto', '0 = pressed')], ['1', T('giù', 'down'), T('0 = premuto', '0 = pressed')],
           ['2', T('sinistra', 'left'), T('0 = premuto', '0 = pressed')], ['3', T('destra', 'right'), T('0 = premuto', '0 = pressed')],
           ['4', T('pulsante 1', 'button 1'), T('0 = premuto', '0 = pressed')], ['5', T('pulsante 2', 'button 2'), T('0 = premuto', '0 = pressed')],
           ['6-7', T('non collegati', 'not connected'), '-']]
    add(P(T(
        "Il giocatore 1 è sulla porta A, <b>$D581</b>; il giocatore 2 sulla porta B, <b>$D580</b>. Le porte "
        "restano in ingresso (DDR = 0) e hanno resistenze di pull-up: un bit a 0 vuol dire premuto.",
        "Player 1 is on port A, <b>$D581</b>; player 2 on port B, <b>$D580</b>. The ports stay as inputs "
        "(DDR = 0) and have pull-up resistors: a bit at 0 means pressed.")))
    add(TBL(joy, [0.12, 0.40, 0.48], center_cols=(0,)))

    add(H3(T('Piedinatura dei connettori DB9 dei joystick', 'Pinout of the DB9 joystick connectors')))
    add(P(T(
        "I due connettori DB9 seguono lo standard Sega Master System: un joystick o un pad Master System "
        "(o un joystick Atari a un pulsante) si collega senza adattatori. Ogni contatto chiude verso massa; "
        "le resistenze di pull-up da 4,7 kOhm sono sulla scheda (R83-R88 per JOY1, R89-R822 per JOY2). "
        "Il +5 V non è portato al connettore.",
        "The two DB9 connectors follow the Sega Master System standard: a Master System joystick or pad "
        "(or a one-button Atari joystick) plugs in without adapters. Every contact closes to ground; the "
        "4.7 kOhm pull-up resistors are on the board (R83-R88 for JOY1, R89-R822 for JOY2). +5 V is not "
        "brought to the connector.")))
    db9 = [[T('PIN', 'PIN'), T('SEGNALE', 'SIGNAL'), T('JOY1 (GIOC. 1)', 'JOY1 (PLAYER 1)'),
            T('JOY2 (GIOC. 2)', 'JOY2 (PLAYER 2)'), T('PIN SCHEMA', 'SCHEMATIC PIN')],
           ['1', T('su', 'up'), '$D581 bit 0 (PA0)', '$D580 bit 0 (PB0)', '5'],
           ['2', T('giù', 'down'), '$D581 bit 1 (PA1)', '$D580 bit 1 (PB1)', '4'],
           ['3', T('sinistra', 'left'), '$D581 bit 2 (PA2)', '$D580 bit 2 (PB2)', '3'],
           ['4', T('destra', 'right'), '$D581 bit 3 (PA3)', '$D580 bit 3 (PB3)', '2'],
           ['5', T('(+5 V) non collegato', '(+5 V) not connected'), '-', '-', '1'],
           ['6', T('pulsante 1 (TL)', 'button 1 (TL)'), '$D581 bit 4 (PA4)', '$D580 bit 4 (PB4)', '9'],
           ['7', T('(TH) non collegato', '(TH) not connected'), '-', '-', '8'],
           ['8', T('massa', 'ground'), 'GND', 'GND', '7'],
           ['9', T('pulsante 2 (TR)', 'button 2 (TR)'), '$D581 bit 5 (PA5)', '$D580 bit 5 (PB5)', '6']]
    add(TBL(db9, [0.08, 0.28, 0.24, 0.24, 0.16], center_cols=(0, 4), font=7.6))
    add(NOTE(T(
        "Il simbolo del connettore nello schema elettrico numera i piedini in ordine speculare (lato saldature): "
        "l'ultima colonna dà il numero che compare nello schema.",
        "The connector symbol in the schematic numbers the pins in mirror order (solder side): the last column "
        "gives the number shown in the schematic.")))

    add(H3(T('Scheda SD ($DD80)', 'SD card ($DD80)')))
    add(P(T(
        "La SD lavora in modo SPI, generato dal software sulla porta A (<b>$DD81</b>, direzione in "
        "<b>$DD83</b>): <b>PA1</b> MISO (dalla scheda), <b>PA2</b> MOSI, <b>PA3</b> SCK, <b>PA4</b> CS. "
        "Le altre linee della VIA sono libere sul pettine di espansione. Il BIOS KEYB/SD riconosce SDSC v1, "
        "SDSC v2 e SDHC/SDXC, legge e scrive settori da 512 byte. È lenta come la scheda vera: circa 6 secondi "
        "per caricare un programma di 23 Kbyte.",
        "The SD works in SPI mode, generated in software on port A (<b>$DD81</b>, direction in <b>$DD83</b>): "
        "<b>PA1</b> MISO (from the card), <b>PA2</b> MOSI, <b>PA3</b> SCK, <b>PA4</b> CS. The other VIA lines are "
        "free on the expansion header. The KEYB/SD BIOS knows SDSC v1, SDSC v2 and SDHC/SDXC cards, and reads and "
        "writes 512-byte sectors. It is as slow as the real card: about 6 seconds to load a 23 Kbyte program.")))

    # ---------------- AY
    add(H2(T('Audio: 2 x AY-3-8910', 'Audio: 2 x AY-3-8910')))
    add(P(T(
        "Ogni AY-3-8910 ha tre voci a onda quadra (A, B, C), un generatore di rumore e un inviluppo; le tre "
        "voci di ogni chip sono mescolate su un'uscita RCA. Il clock è quello della CPU, 1 MHz. Per scrivere "
        "un registro: numero del registro nell'indirizzo <i>latch</i>, poi il valore nell'indirizzo <i>dati</i>. "
        "A0 sceglie latch (0) o dati (1), A2 il chip destro (0) o sinistro (1).",
        "Each AY-3-8910 has three square-wave voices (A, B, C), a noise generator and an envelope; the three "
        "voices of each chip are mixed on one RCA output. The clock is the CPU clock, 1 MHz. To write a register: "
        "the register number to the <i>latch</i> address, then the value to the <i>data</i> address. A0 selects "
        "latch (0) or data (1), A2 the right (0) or left (1) chip.")))
    ay = [[T('CANALE', 'CHANNEL'), 'LATCH', T('DATI', 'DATA'), T('DECIMALE', 'DECIMAL')],
          [T('destro', 'right'), '$D380', '$D381', '54144 / 54145'],
          [T('sinistro', 'left'), '$D384', '$D385', '54148 / 54149']]
    add(TBL(ay, [0.25, 0.25, 0.25, 0.25], center_cols=(1, 2, 3)))
    ayr = [[T('REG.', 'REG.'), T('FUNZIONE', 'FUNCTION'), T('REG.', 'REG.'), T('FUNZIONE', 'FUNCTION')],
           ['R0 / R1', T('periodo voce A: fine (8 bit) / grosso (4 bit)', 'voice A period: fine (8 bits) / coarse (4 bits)'),
            'R8', T('volume A (0-15; bit 4 = usa l\'inviluppo)', 'volume A (0-15; bit 4 = use the envelope)')],
           ['R2 / R3', T('periodo voce B', 'voice B period'), 'R9', T('volume B', 'volume B')],
           ['R4 / R5', T('periodo voce C', 'voice C period'), 'R10', T('volume C', 'volume C')],
           ['R6', T('periodo del rumore (5 bit)', 'noise period (5 bits)'), 'R11 / R12', T('periodo dell\'inviluppo (16 bit)', 'envelope period (16 bits)')],
           ['R7', T('mixer: bit 0-2 tono A-C spento, bit 3-5 rumore A-C spento (1 = spento)', 'mixer: bits 0-2 tone A-C off, bits 3-5 noise A-C off (1 = off)'),
            'R13', T('forma dell\'inviluppo', 'envelope shape')],
           ['', '', 'R14 / R15', T('porte I/O (non usate)', 'I/O ports (not used)')]]
    add(TBL(ayr, [0.11, 0.39, 0.12, 0.38], center_cols=(0, 2)))
    add(P(T(
        "Frequenza di una nota: <b>f = 1.000.000 / (16 x periodo)</b>. Per esempio il La a 440 Hz ha "
        "periodo 142 ($08E).",
        "Frequency of a note: <b>f = 1,000,000 / (16 x period)</b>. For example A at 440 Hz has period 142 ($08E).")))

    add(H2(T('Pettine di espansione', 'Expansion header')))
    add(P(T(
        "I pettini portano fuori il bus degli indirizzi, il bus dei dati, il clock PHI0 e le linee libere della "
        "VIA della scheda SD (porta A tranne PA1-PA4, porta B, CA/CB). La piedinatura esatta è nello schema "
        "(sezione III).",
        "The headers bring out the address bus, the data bus, the PHI0 clock and the free lines of the SD card "
        "VIA (port A except PA1-PA4, port B, CA/CB). The exact pinout is in the schematic (section III).")))

    # ================================================================ VI. MEMORY USE
    add(H1('VI', T('Uso della memoria', 'Memory usage')))
    add(P(T(
        "Questa sezione serve a chi scrive programmi: dice quali parti della RAM usano il BIOS, WozMon e il "
        "BASIC, e quali restano libere.",
        "This section is for those who write programs: it tells which parts of the RAM the BIOS, WozMon and "
        "BASIC use, and which stay free.")))
    add(H2(T('La RAM in dettaglio', 'The RAM in detail')))
    ram = [[T('INDIRIZZI', 'ADDRESSES'), T('USATA DA', 'USED BY'), T('CONTENUTO', 'CONTENTS')],
           ['$0000-$002F', 'BASIC', T('variabili del BASIC in pagina zero (anche $3A-$43, $50-$FF)', 'BASIC zero-page variables (also $3A-$43, $50-$FF)')],
           ['$0010-$005F', 'BASIC', T('INPUTBUFFER: la riga battuta', 'INPUTBUFFER: the line being typed')],
           ['$0024-$002B', 'WozMon', 'XAML, XAMH, STL, STH, L, H, YSAV, MODE'],
           ['$0030-$0039', T('BIOS video', 'BIOS video'), T('cursore (riga $32, colonna $33) e calcoli del driver di testo', 'cursor (row $32, column $33) and text driver work bytes')],
           ['$0040-$0043', T('BIOS menu', 'BIOS menu'), T('puntatori del menu', 'menu pointers')],
           ['$0044-$004E', 'BIOS SD', T('driver SD: comando, puntatore, settore, tentativi, slot', 'SD driver: command, pointer, sector, retries, slot')],
           ['$0100-$01FF', 'CPU', T('stack', 'stack')],
           ['$0200-$027F', 'WozMon', T('buffer della riga di comando', 'command line buffer')],
           ['$0300-$0305', 'BIOS SD', T('comando SD (6 byte)', 'SD command (6 bytes)')],
           ['$0306-$0308', T('BIOS tastiera', 'BIOS keyboard'), T('puntatori di scrittura e lettura del buffer, stato (Shift, Ctrl, Alt, Caps)', 'buffer write and read pointers, state (Shift, Ctrl, Alt, Caps)')],
           ['$0309', T('BIOS tastiera', 'BIOS keyboard'), T('modo: bit 7 = esteso', 'mode: bit 7 = extended')],
           ['$030A-$030F', 'BIOS SD', T('tipo di scheda, risposta R3/R7, contatore', 'card type, R3/R7 response, counter')],
           ['$0310-$0315', 'BIOS SD', T('lunghezza, indirizzo di carico, indirizzo di avvio del programma', 'length, load address, start address of the program')],
           ['$0316-$0319', 'BIOS SD', T('<b>SD_LBA</b>: numero del settore, 32 bit little endian', '<b>SD_LBA</b>: sector number, 32 bits little endian')],
           ['$031A-$033A', 'BIOS SD', T('tipo e nome per la riga seriale (libera dopo il caricamento)', 'type and name for the serial line (free after loading)')],
           ['$0380-$03FF', T('BIOS tastiera', 'BIOS keyboard'), T('buffer dei tasti, 128 byte', 'key buffer, 128 bytes')],
           ['$0400-$7FFF', 'BASIC', T('programma, variabili e stringhe (31743 byte liberi)', 'program, variables and strings (31743 bytes free)')],
           ['$0FA0', T('programma', 'program'), T('trampolino IRQ (JSR dal BIOS)', 'IRQ trampoline (JSR from the BIOS)')],
           ['$0FD0', T('programma', 'program'), T('trampolino NMI (JSR dal BIOS a ogni quadro)', 'NMI trampoline (JSR from the BIOS every frame)')],
           ['$1000-$7FFF', T('programma', 'program'), T('programmi della SD (al massimo 28 Kbyte, carico da $0F00)', 'SD programs (at most 28 Kbyte, loaded from $0F00)')],
           ['$3000-$7FFF', T('applicativi', 'applications'), T('dati di WRITE (gap buffer); area libera di MON e ASM', 'WRITE data (gap buffer); free area of MON and ASM')],
           ]
    add(TBL(ram, [0.17, 0.17, 0.66], font=7.4))
    add(NOTE(T(
        "<b>Durante il menu SD</b> il BIOS usa anche $1000-$11FF (settore della directory), $1200-$1208 "
        "(stato del menu), $1300-$14FE (slot e flag dei sottomenu) e $2000-$3FDF (nomi dei sottomenu). Tutto "
        "torna libero quando il programma è caricato.",
        "<b>During the SD menu</b> the BIOS also uses $1000-$11FF (directory sector), $1200-$1208 (menu state), "
        "$1300-$14FE (submenu slots and flags) and $2000-$3FDF (submenu names). All of it is free again once "
        "the program is loaded.")))

    add(H2(T('La ROM', 'The ROM')))
    rom = [[T('INDIRIZZI', 'ADDRESSES'), T('DIM.', 'SIZE'), T('CONTENUTO', 'CONTENTS')],
           ['$8000-$AFFF', '12K', T('Microsoft BASIC 1977 e i driver del BIOS (video, tastiera, seriale, SD)', 'Microsoft BASIC 1977 and the BIOS drivers (video, keyboard, serial, SD)')],
           ['$B000-$DFFF', '12K', T('non visibile: finestra di I/O', 'not visible: I/O window')],
           ['$E000-$FCFF', '7424', T('menu di avvio, menu SD, tastiera estesa', 'boot menu, SD menu, extended keyboard')],
           ['$FD00-$FDFF', '256', T('tabella dei salti (interfaccia stabile)', 'jump table (stable interface)')],
           ['$FE00-$FFF9', '506', 'WozMon'],
           ['$FFFA-$FFFF', '6', T('vettori NMI, RESET, IRQ', 'NMI, RESET, IRQ vectors')]]
    add(TBL(rom, [0.2, 0.1, 0.7]))

    add(H2(T('La tabella dei salti ($FD00)', 'The jump table ($FD00)')))
    add(P(T(
        "I programmi chiamano il BIOS <b>solo</b> attraverso questa tabella: ogni voce è un <b>JMP</b> alla "
        "routine vera, che può spostarsi a ogni nuova versione del BIOS. Gli indirizzi della tabella invece "
        "non cambiano mai; le voci nuove si aggiungono solo in fondo.",
        "Programs call the BIOS <b>only</b> through this table: every entry is a <b>JMP</b> to the real routine, "
        "which can move with every new BIOS version. The table addresses never change; new entries are only "
        "added at the end.")))
    jt = [[T('INDIRIZZO', 'ADDRESS'), T('NOME', 'NAME'), T('INGRESSO / USCITA', 'INPUT / OUTPUT')],
          ['$FD00', 'JT_CHROUT', T('A = carattere da stampare (schermo e seriale)', 'A = character to print (screen and serial)')],
          ['$FD03', 'JT_CHRIN_NOECHO', T('C=1 e A = tasto se premuto; C=0 se nessuno. Prima la seriale, poi la tastiera', 'C=1 and A = key if pressed; C=0 if none. Serial first, then keyboard')],
          ['$FD06', 'JT_RESET_TERM', T('reset ANSI del terminale seriale', 'ANSI reset of the serial terminal')],
          ['$FD09', 'JT_INIT_CRT', T('modo testo, VRAM e caratteri del BIOS; cursore in alto', 'text mode, VRAM and BIOS font; cursor at the top')],
          ['$FD0C', 'JT_LOAD_RUN_SLOT', T('A = slot SD: carica ed esegue (con JMP: non ritorna; errore = menu)', 'A = SD slot: loads and runs (with JMP: never returns; error = menu)')],
          ['$FD0F', 'JT_SHOW_MENU', T('torna al menu del BIOS (con JMP)', 'back to the BIOS menu (with JMP)')],
          ['$FD12', 'JT_INIT_SDCARD', T('A = slot SD: carica e ritorna; C=0 ok, C=1 errore', 'A = SD slot: loads and returns; C=0 ok, C=1 error')],
          ['$FD15', 'JT_FLUSH_KB', T('svuota il buffer della tastiera (circa 0,5 s; conserva A, X, Y)', 'empties the keyboard buffer (about 0.5 s; keeps A, X, Y)')],
          ['$FD18', 'JT_SD_READ_SECTOR', T('legge il settore SD_LBA nel buffer X/Y (lo/hi, 512 byte); C=0 ok', 'reads sector SD_LBA into the buffer X/Y (lo/hi, 512 bytes); C=0 ok')],
          ['$FD1B', 'JT_SD_WRITE_SECTOR', T('scrive il buffer X/Y nel settore SD_LBA; C=0 ok', 'writes the buffer X/Y to sector SD_LBA; C=0 ok')],
          ['$FD1E', 'JT_SD_INIT', T('(re)inizializza la SD: C=0 e A = tipo (1 SDSC v1, 2 SDSC v2, 3 SDHC); C=1 nessuna scheda', '(re)initializes the SD: C=0 and A = type (1 SDSC v1, 2 SDSC v2, 3 SDHC); C=1 no card')],
          ['$FD21', 'JT_KB_SET_MODE', T('A=0 tastiera classica, A≠0 tastiera estesa', 'A=0 classic keyboard, A≠0 extended keyboard')]]
    add(TBL(jt, [0.12, 0.27, 0.61], font=7.4))
    add(P(T(
        "Le voci da $FD18 in poi esistono solo nel BIOS KEYB/SD. Un programma che vuole funzionare anche con "
        "il BIOS precedente controlla che all'indirizzo ci sia <b>$4C</b> (JMP) prima di chiamarlo.",
        "The entries from $FD18 on exist only in the KEYB/SD BIOS. A program that must also work with the "
        "previous BIOS checks that the address holds <b>$4C</b> (JMP) before calling it.")))
    add(CODE(T("""
; stampa "CIAO" con il BIOS (assemblatore 65C02)
        .ORG $3000
        LDX #0
LOOP    LDA MSG,X
        BEQ FINE
        JSR $FD00          ; JT_CHROUT
        INX
        BNE LOOP
FINE    RTS
MSG     .BYTE "CIAO",13,10,0
""", """
; prints "HELLO" through the BIOS (65C02 assembler)
        .ORG $3000
        LDX #0
LOOP    LDA MSG,X
        BEQ DONE
        JSR $FD00          ; JT_CHROUT
        INX
        BNE LOOP
DONE    RTS
MSG     .BYTE "HELLO",13,10,0
""")))

    # ================================================================ VII. BIOS
    add(H1('VII', T('Il BIOS e il menu', 'The BIOS and its menu')))
    add(P(T(
        "Il firmware nella EEPROM è il <b>BIOS 16.11.26 KEYB/SD R2</b>. All'accensione, e dopo ogni RESET, "
        "prepara video, tastiera, seriale e audio e mostra il menu principale, sullo schermo e sul terminale "
        "seriale insieme.",
        "The firmware in the EEPROM is <b>BIOS 16.11.26 KEYB/SD R2</b>. At power-on, and after every RESET, it "
        "sets up video, keyboard, serial port and audio and shows the main menu, on the screen and on the serial "
        "terminal at the same time.")))
    add(IMGROW([(SCREENS / 'menu_main.png', T('Il menu principale.', 'The main menu.')),
                (SCREENS / 'menu_info.png', T('System Information (tasto 4).', 'System Information (key 4).'))], 78))
    menu = [[T('TASTO', 'KEY'), T('VOCE', 'ENTRY'), T('COSA FA', 'WHAT IT DOES')],
            ['1', 'WOZ MONITOR APPLE I', T('avvia WozMon a $FE00 (sezione VIII)', 'starts WozMon at $FE00 (section VIII)')],
            ['2', 'MICROSOFT BASIC 1977', T('avvia il BASIC a $8000 (sezione IX)', 'starts BASIC at $8000 (section IX)')],
            ['3', 'SDCARD PROGRAMS MENU', T('legge la scheda SD e mostra i programmi', 'reads the SD card and shows the programs')],
            ['4', 'MiniVIC SYSTEM INFORMATION', T('CPU, memoria, indirizzi delle schede, versione; un tasto torna al menu', 'CPU, memory, board addresses, version; a key goes back to the menu')]]
    add(TBL(menu, [0.1, 0.36, 0.54], center_cols=(0,)))

    add(H2(T('Il menu dei programmi SD', 'The SD programs menu')))
    add(P(T(
        "Il tasto <b>3</b> legge la directory della scheda (READING SD DIRECTORY...) e chiede che tipo di "
        "programmi mostrare. Senza scheda, o con una scheda non preparata da make_sd.py, dopo circa 5 secondi "
        "compare <b>NO VALID SD DIRECTORY FOUND</b>; un tasto torna al menu.",
        "Key <b>3</b> reads the card directory (READING SD DIRECTORY...) and asks which kind of programs to "
        "show. With no card, or with a card not made by make_sd.py, after about 5 seconds <b>NO VALID SD "
        "DIRECTORY FOUND</b> appears; a key goes back to the menu.")))
    add(IMGROW([(SCREENS / 'menu_sd.png', T('La scelta del sottomenu.', 'Choosing the submenu.')),
                (SCREENS / 'menu_games.png', T('1. GAMES, pagina 1 di 6.', '1. GAMES, page 1 of 6.'))], 78))
    sub = [[T('TASTO', 'KEY'), T('SOTTOMENU', 'SUBMENU'), T('MOSTRA', 'SHOWS')],
           ['1', 'GAMES', T('i giochi (tipo GAME)', 'the games (type GAME)')],
           ['2', 'APPS', T('gli applicativi e gli strumenti (tipi APP e TOOL)', 'the applications and tools (types APP and TOOL)')],
           ['3', 'SOUNDS', T('i brani musicali (tipo SOUND)', 'the songs (type SOUND)')],
           ['4', 'ALL PROGRAMS', T('tutte le pagine della SD così come sono, anche i programmi senza tipo', 'all the SD pages as they are, also the programs without a type')],
           ['ESC', 'MAIN MENU', T('torna al menu principale', 'back to the main menu')]]
    add(TBL(sub, [0.1, 0.22, 0.68], center_cols=(0,)))
    add(P(T("Dentro un elenco:", "Inside a list:")))
    add(B([
        T("<b>1</b>...<b>9</b> sceglie il programma della pagina;", "<b>1</b>...<b>9</b> picks the program of the page;"),
        T("<b>A</b> pagina precedente, <b>D</b> pagina successiva (9 programmi per pagina);",
          "<b>A</b> previous page, <b>D</b> next page (9 programs per page);"),
        T("<b>ESC</b> torna alla scelta del sottomenu;", "<b>ESC</b> goes back to the submenu choice;"),
        T("<b>N&gt;</b> davanti al nome: il programma parte da solo dopo il caricamento; <b>N.</b>: viene solo caricato.",
          "<b>N&gt;</b> before the name: the program starts by itself after loading; <b>N.</b>: it is only loaded."),
    ]))
    add(P(T(
        "Durante il caricamento compare <b>LOADING FROM SD, PLEASE WAIT...</b>. Un programma solo caricato mostra "
        "<b>SD PROGRAM LOADED AT $xxxx</b> e <b>TYPE xxxx R AND ENTER ON WOZMON</b>: si avvia da WozMon con "
        "l'indirizzo seguito da R. Se la scheda o i dati del programma non sono validi compare <b>SD LOAD ERROR</b>. "
        "Un sottomenu vuoto dice <b>NO PROGRAMS OF THIS KIND ON THE SD</b> (scheda fatta prima dei tipi: usate 4. ALL).",
        "While loading, <b>LOADING FROM SD, PLEASE WAIT...</b> appears. A program that is only loaded shows "
        "<b>SD PROGRAM LOADED AT $xxxx</b> and <b>TYPE xxxx R AND ENTER ON WOZMON</b>: start it from WozMon with "
        "the address followed by R. If the card or the program data are not valid, <b>SD LOAD ERROR</b> appears. "
        "An empty submenu says <b>NO PROGRAMS OF THIS KIND ON THE SD</b> (card made before the types: use 4. ALL).")))
    add(P(T(
        "Quando un programma parte, il BIOS manda <b>solo sulla seriale</b> una riga con il tipo e il nome, "
        "per esempio <b>[GAME] ASTEROIDS</b>, <b>[APP] WRITE</b>, <b>[TOOL] MON</b>, <b>[SOUND] KOROBEINIKI</b>. "
        "Lo schermo non cambia.",
        "When a program starts, the BIOS sends <b>on the serial port only</b> a line with its type and name, for "
        "example <b>[GAME] ASTEROIDS</b>, <b>[APP] WRITE</b>, <b>[TOOL] MON</b>, <b>[SOUND] KOROBEINIKI</b>. The "
        "screen does not change.")))
    add(IMGROW([(SCREENS / 'menu_apps.png', '2. APPS'), (SCREENS / 'menu_sounds.png', '3. SOUNDS')], 78))

    add(H2(T('La tastiera', 'The keyboard')))
    add(P(T(
        "La tastiera DIN5 deve avere il layout <b>US</b>. Il BIOS ha due modi. Il <b>modo classico</b> è quello "
        "del menu, di WozMon e del BASIC: lettere, cifre e simboli con lo Shift, Invio, Backspace, Tab, Esc; "
        "le frecce danno le cifre del tastierino (i giochi le usano così). Il <b>modo esteso</b> lo accendono "
        "gli applicativi con JT_KB_SET_MODE; il ritorno al menu rimette il modo classico.",
        "The DIN5 keyboard must have the <b>US</b> layout. The BIOS has two modes. <b>Classic mode</b> is the one "
        "of the menu, WozMon and BASIC: letters, digits and symbols with Shift, Enter, Backspace, Tab, Esc; the "
        "arrows give the keypad digits (games use them this way). <b>Extended mode</b> is turned on by the "
        "applications with JT_KB_SET_MODE; going back to the menu sets classic mode again.")))
    kx = [[T('TASTO', 'KEY'), T('CODICE (MODO ESTESO)', 'CODE (EXTENDED MODE)'), T('TASTO', 'KEY'), T('CODICE', 'CODE')],
          ['↑ ↓ ← →', '$80 $81 $82 $83', 'F1 ... F12', '$90 ... $9B'],
          ['Home End', '$84 $85', T('Ctrl+lettera', 'Ctrl+letter'), '$01 ... $1A'],
          ['PgUp PgDn', '$86 $87', T('Alt+lettera', 'Alt+letter'), '$E1 ... $FA'],
          ['Ins Delete', '$88 $89', T('Invio / Backspace', 'Enter / Backspace'), '$0D / $08'],
          [T('Caps Lock', 'Caps Lock'), T('inverte maiuscole e minuscole delle lettere', 'swaps upper and lower case of letters'), 'Tab / Esc', '$09 / $1B']]
    add(TBL(kx, [0.18, 0.32, 0.24, 0.26]))
    add(P(T(
        "Ctrl e Alt di destra funzionano come quelli di sinistra. Il LED di Caps Lock resta spento: la scheda "
        "non trasmette verso la tastiera. Il tastierino dà sempre le cifre.",
        "Right Ctrl and Alt work like the left ones. The Caps Lock LED stays off: the board does not send to "
        "the keyboard. The keypad always gives digits.")))

    add(H2(T('Il terminale seriale', 'The serial terminal')))
    add(P(T(
        "Con un cavo seriale e un programma terminale (PuTTY, Tera Term, minicom) impostato a <b>19200 baud, 8 bit, "
        "nessuna parità, 1 bit di stop</b>, senza controllo di flusso, il PC diventa una seconda console: "
        "vede tutto quello che il BIOS, WozMon e il BASIC scrivono, e i tasti battuti sul PC arrivano come quelli "
        "della tastiera. Il tasto DEL ($7F) del terminale vale come Backspace. Nel BASIC, <b>Ctrl+C</b> dal "
        "terminale interrompe il programma. I giochi e gli applicativi non usano la seriale, tranne TERM.",
        "With a serial cable and a terminal program (PuTTY, Tera Term, minicom) set to <b>19200 baud, 8 bits, no "
        "parity, 1 stop bit</b>, no flow control, the PC becomes a second console: it sees everything the BIOS, "
        "WozMon and BASIC write, and the keys typed on the PC arrive like keyboard keys. The DEL key ($7F) of the "
        "terminal works as Backspace. In BASIC, <b>Ctrl+C</b> from the terminal stops the program. Games and "
        "applications do not use the serial port, except TERM.")))

    # ================================================================ VIII. WOZMON
    add(H1('VIII', T('Il monitor WozMon', 'The WozMon monitor')))
    add(P(T(
        "WozMon è il monitor scritto da Steve Wozniak per l'Apple-1 (1976), qui a $FE00. Con WozMon si guarda "
        "e si cambia la memoria in esadecimale e si avviano programmi in linguaggio macchina. Si avvia con il "
        "tasto <b>1</b> del menu; compare la barra rovesciata <b>\\</b>, il suo prompt. Si esce con RESET.",
        "WozMon is the monitor Steve Wozniak wrote for the Apple-1 (1976), here at $FE00. With WozMon you look "
        "at and change the memory in hexadecimal and start machine language programs. It starts with key "
        "<b>1</b> of the menu; the backslash <b>\\</b>, its prompt, appears. RESET leaves it.")))
    add(P(T(
        "Ogni comando è una riga che finisce con <b>Invio</b>. Gli indirizzi e i dati sono in esadecimale "
        "(cifre 0-9 e A-F, fino a 4 cifre; gli zeri iniziali si possono omettere). <b>Backspace</b> cancella "
        "l'ultimo carattere, <b>Esc</b> annulla la riga (compare una nuova \\).",
        "Every command is a line ending with <b>Enter</b>. Addresses and data are hexadecimal (digits 0-9 and "
        "A-F, up to 4 digits; leading zeros can be left out). <b>Backspace</b> erases the last character, "
        "<b>Esc</b> cancels the line (a new \\ appears).")))
    wz = [[T('COMANDO', 'COMMAND'), T('ESEMPIO', 'EXAMPLE'), T('COSA FA', 'WHAT IT DOES')],
          [T('indirizzo', 'address'), 'E000', T('mostra il byte a $E000', 'shows the byte at $E000')],
          [T('più indirizzi', 'several addresses'), '4 FF 1000', T('mostra i byte di ogni indirizzo', 'shows the byte of every address')],
          [T('blocco', 'block'), 'E000.E01F', T('mostra i byte da $E000 a $E01F, 8 per riga', 'shows the bytes from $E000 to $E01F, 8 per line')],
          [T('continua', 'continue'), '.E03F', T('continua il blocco dall\'ultimo indirizzo mostrato', 'continues the block from the last address shown')],
          [T('scrivi', 'store'), '3000: A9 41 20', T('scrive i byte da $3000 in poi', 'writes the bytes from $3000 on')],
          [T('scrivi ancora', 'store more'), ': 00 FD', T('continua a scrivere dopo l\'ultimo byte', 'goes on writing after the last byte')],
          [T('esegui', 'run'), '3000R', T('salta a $3000 (JMP)', 'jumps to $3000 (JMP)')],
          [T('combinati', 'combined'), '3000: A9 41 3000R', T('scrive e poi esegue', 'stores and then runs')]]
    add(TBL(wz, [0.2, 0.25, 0.55]))
    add(H3(T('Un esempio', 'An example')))
    add(P(T(
        "Si leggono i vettori della CPU, poi si scrive un programma di 8 byte a $3000 che stampa la lettera A "
        "con JT_CHROUT e torna a WozMon (JMP $FE10, la routine che legge una nuova riga), lo si rilegge e lo "
        "si esegue. Dopo <b>3000R</b> WozMon mostra il primo byte ($A9) e il programma stampa <b>A</b>.",
        "We read the CPU vectors, then write an 8-byte program at $3000 that prints the letter A with JT_CHROUT "
        "and goes back to WozMon (JMP $FE10, the routine that reads a new line), read it back and run it. After "
        "<b>3000R</b> WozMon shows the first byte ($A9) and the program prints <b>A</b>.")))
    add(CODE("""\\
FFFA.FFFF
FFFA: B0 A7 08 E2 01 AA
3000: A9 41 20 00 FD 4C 10 FE
3000: 00
3000.3007
3000: A9 41 20 00 FD 4C 10 FE

3000R
3000: A9A"""))
    add(IMG_(SCREENS / 'wozmon.png', 95, T('La stessa sessione sullo schermo del miniVIC.', 'The same session on the miniVIC screen.')))
    add(NOTE(T(
        "Le aree libere per i programmi sono $1000-$7FFF (la pagina $0300 è del BIOS, $0200 è il buffer di "
        "WozMon). Un programma che finisce con RTS dopo un comando R non torna a WozMon: usate JMP $FE10, "
        "oppure RESET.",
        "The free areas for programs are $1000-$7FFF (page $0300 belongs to the BIOS, $0200 is the WozMon "
        "buffer). A program ending with RTS after an R command does not go back to WozMon: use JMP $FE10, or "
        "RESET.")))

    # ================================================================ IX. BASIC
    add(H1('IX', 'Microsoft BASIC'))
    add(P(T(
        "Il BASIC è il Microsoft BASIC per 6502 del 1977 (dal progetto msbasic di Michael Steil, configurazione "
        "2A, numeri a 9 cifre), con l'ingresso e l'uscita del BIOS del miniVIC. Si avvia con il tasto <b>2</b> "
        "del menu. Prima chiede:",
        "BASIC is Microsoft BASIC for the 6502 of 1977 (from Michael Steil's msbasic project, configuration 2A, "
        "9-digit numbers), with the input and output of the miniVIC BIOS. It starts with key <b>2</b> of the "
        "menu. First it asks:")))
    add(B([
        T("<b>MEMORY SIZE?</b> Invio usa tutta la RAM; un numero limita la memoria del BASIC (per lasciare spazio a routine in linguaggio macchina).",
          "<b>MEMORY SIZE?</b> Enter uses all the RAM; a number limits the BASIC memory (to leave room for machine language routines)."),
        T("<b>TERMINAL WIDTH?</b> Invio lascia 40 colonne.", "<b>TERMINAL WIDTH?</b> Enter keeps 40 columns."),
    ]))
    add(P(T("Poi scrive <b>31743 BYTES FREE</b>, la riga del copyright e <b>OK</b>.",
            "Then it writes <b>31743 BYTES FREE</b>, the copyright line and <b>OK</b>.")))
    add(IMG_(SCREENS / 'basic.png', 95, T('Avvio del BASIC e un piccolo programma.', 'BASIC start-up and a small program.')))
    add(H2(T('Scrivere i programmi', 'Writing programs')))
    add(B([
        T("Una riga che inizia con un numero (0-63999) entra nel programma; senza numero viene eseguita subito.",
          "A line starting with a number (0-63999) goes into the program; without a number it runs at once."),
        T("<b>Backspace</b> cancella l'ultimo carattere; i vecchi tasti del BASIC funzionano ancora: <b>_</b> cancella un carattere, <b>@</b> annulla la riga.",
          "<b>Backspace</b> erases the last character; the old BASIC keys still work: <b>_</b> erases a character, <b>@</b> cancels the line."),
        T("<b>?</b> è un'abbreviazione di PRINT.", "<b>?</b> is short for PRINT."),
        T("Per correggere una riga si riscrive per intero; un numero da solo la cancella.",
          "To fix a line, type it again in full; a number alone deletes it."),
        T("Ctrl+C da un terminale seriale interrompe un programma (BREAK); CONT lo riprende.",
          "Ctrl+C from a serial terminal stops a program (BREAK); CONT resumes it."),
    ]))
    add(NOTE(T(
        "<b>Limiti noti.</b> LOAD e SAVE esistono ma non fanno nulla: il miniVIC non salva i programmi BASIC. "
        "Le righe più lunghe di circa 32 caratteri si rovinano dal 33° in poi: scrivete righe brevi. "
        "USR non è disponibile.",
        "<b>Known limits.</b> LOAD and SAVE exist but do nothing: the miniVIC does not save BASIC programs. Lines "
        "longer than about 32 characters get spoiled from the 33rd on: keep the lines short. USR is not "
        "available.")))
    add(H2(T('Parole chiave', 'Keywords')))
    kw = [[T('TIPO', 'KIND'), T('PAROLE', 'WORDS')],
          [T('istruzioni', 'statements'), 'END FOR NEXT DATA INPUT DIM READ LET GOTO RUN IF RESTORE GOSUB RETURN REM STOP ON WAIT DEF POKE PRINT CONT LIST CLEAR GET NEW (LOAD SAVE)'],
          [T('parti di istruzione', 'statement parts'), 'TAB( TO FN SPC( THEN NOT STEP GO'],
          [T('operatori', 'operators'), '+ - * / ^ AND OR &gt; = &lt;'],
          [T('funzioni numeriche', 'numeric functions'), 'SGN INT ABS FRE POS SQR RND LOG EXP COS SIN TAN ATN PEEK'],
          [T('funzioni di stringa', 'string functions'), 'LEN STR$ VAL ASC CHR$ LEFT$ RIGHT$ MID$']]
    add(TBL(kw, [0.22, 0.78]))
    add(P(T(
        "Le variabili hanno nomi di due caratteri significativi; <b>A$</b> è una stringa, <b>A%</b> un intero. "
        "GET legge un tasto senza aspettare. Messaggi di errore principali: ?SYNTAX ERROR, ?NEXT WITHOUT FOR, "
        "?RETURN WITHOUT GOSUB, ?OUT OF DATA, ?ILLEGAL QUANTITY, ?OVERFLOW, ?OUT OF MEMORY, ?UNDEF'D STATEMENT, "
        "?BAD SUBSCRIPT, ?REDIM'D ARRAY, ?DIVISION BY ZERO, ?TYPE MISMATCH, ?STRING TOO LONG, ?CAN'T CONTINUE.",
        "Variables have names with two significant characters; <b>A$</b> is a string, <b>A%</b> an integer. GET "
        "reads a key without waiting. Main error messages: ?SYNTAX ERROR, ?NEXT WITHOUT FOR, ?RETURN WITHOUT "
        "GOSUB, ?OUT OF DATA, ?ILLEGAL QUANTITY, ?OVERFLOW, ?OUT OF MEMORY, ?UNDEF'D STATEMENT, ?BAD SUBSCRIPT, "
        "?REDIM'D ARRAY, ?DIVISION BY ZERO, ?TYPE MISMATCH, ?STRING TOO LONG, ?CAN'T CONTINUE.")))
    add(H2(T('PEEK e POKE sui dispositivi', 'PEEK and POKE on the devices')))
    add(P(T("Leggere il joystick 1 (ogni bit a 0 è una direzione o un pulsante premuto):",
            "Reading joystick 1 (every bit at 0 is a pressed direction or button):")))
    add(CODE("""10 J=PEEK(54657)
20 IF (J AND 16)=0 THEN PRINT "FIRE"
30 IF (J AND 1)=0 THEN PRINT "UP"
40 GOTO 10"""))
    add(P(T("Suonare un La (440 Hz) sulla voce A del chip destro, poi spegnerlo:",
            "Playing an A (440 Hz) on voice A of the right chip, then stopping it:")))
    add(CODE(T("""10 L=54144:D=54145
20 POKE L,0:POKE D,142:REM PERIODO FINE
30 POKE L,1:POKE D,0:REM PERIODO GROSSO
40 POKE L,7:POKE D,62:REM SOLO TONO A
50 POKE L,8:POKE D,15:REM VOLUME A
60 FOR I=1 TO 1000:NEXT
70 POKE L,8:POKE D,0""", """10 L=54144:D=54145
20 POKE L,0:POKE D,142:REM FINE PERIOD
30 POKE L,1:POKE D,0:REM COARSE PERIOD
40 POKE L,7:POKE D,62:REM TONE A ONLY
50 POKE L,8:POKE D,15:REM VOLUME A
60 FOR I=1 TO 1000:NEXT
70 POKE L,8:POKE D,0""")))
    add(P(T("Cambiare i colori dello schermo (registro 7 del VDP: testo nero su bianco):",
            "Changing the screen colours (VDP register 7: black text on white):")))
    add(CODE("POKE 45057,31:POKE 45057,135"))

    # ================================================================ X. APPLICATIONS
    add(H1('X', T('Gli applicativi', 'The applications')))
    add(P(T(
        "I <b>miniVIC Apps</b> sono programmi da ufficio in assembly 65C02, nello spirito di quelli del VIC-20 "
        "(1980-1983). Stanno nel sottomenu <b>APPS</b> della SD e richiedono il BIOS KEYB/SD (tastiera estesa e "
        "scrittura sulla SD), tranne JUKEBOX.",
        "The <b>miniVIC Apps</b> are office programs in 65C02 assembly, in the spirit of those of the VIC-20 "
        "years (1980-1983). They are in the <b>APPS</b> submenu of the SD and need the KEYB/SD BIOS (extended "
        "keyboard and SD writing), except JUKEBOX.")))
    apps = [[T('PROGRAMMA', 'PROGRAM'), T('TIPO', 'TYPE'), T('COS\'È', 'WHAT IT IS')],
            ['WRITE', 'APP', T('elaboratore di testi nello stile di WordStar', 'text editor in the WordStar style')],
            ['CALC', 'APP', T('foglio elettronico nello stile di VisiCalc', 'spreadsheet in the VisiCalc style')],
            ['FILE', 'APP', T('schedario nello stile di PFS:File', 'card file in the PFS:File style')],
            ['DESK', 'APP', T('calcolatrice con rotolo, calendario, orologio con sveglia', 'adding machine, calendar, clock with alarm')],
            ['TERM', 'APP', T('terminale seriale nello stile di VicTerm', 'serial terminal in the VicTerm style')],
            ['JUKEBOX', 'APP', T('lettore musicale con il joystick', 'music player, with the joystick')],
            ['MON', 'TOOL', T('monitor in linguaggio macchina nello stile di Supermon', 'machine language monitor in the Supermon style')],
            ['DISK', 'TOOL', T('gestione della scheda SD: programmi e documenti', 'SD card manager: programs and documents')],
            ['ASM', 'TOOL', T('assemblatore 65C02 a due passate', 'two-pass 65C02 assembler')]]
    add(TBL(apps, [0.18, 0.12, 0.70], center_cols=(1,)))
    add(H2(T('Convenzioni comuni', 'Common conventions')))
    add(B([
        T("<b>^</b> vuol dire <b>Ctrl</b>. <b>^KS</b> è un comando di due tasti: Ctrl+K, poi S.",
          "<b>^</b> means <b>Ctrl</b>. <b>^KS</b> is a two-key command: Ctrl+K, then S."),
        T("Ogni comando con una freccia o un tasto funzione ha anche una scorciatoia Ctrl+lettera, per le tastiere compatte.",
          "Every command with an arrow or a function key also has a Ctrl+letter shortcut, for compact keyboards."),
        T("<b>F1</b> (o <b>^J</b>) mostra l'aiuto.", "<b>F1</b> (or <b>^J</b>) shows the help."),
        T("<b>F10</b>, <b>^KQ</b> o <b>Q</b> torna al menu del BIOS, chiedendo prima se c'è qualcosa da salvare.",
          "<b>F10</b>, <b>^KQ</b> or <b>Q</b> goes back to the BIOS menu, asking first if something is not saved."),
    ]))
    add(H3(T('I documenti sulla SD', 'Documents on the SD card')))
    add(P(T(
        "I documenti stanno dopo l'area dei programmi, dal settore 16384: un indice di 15 documenti, ognuno "
        "con un nome di 12 caratteri, un tipo e 40 settori (20 Kbyte). Aggiornare il menu della SD non li tocca.",
        "Documents live after the program area, from sector 16384: an index of 15 documents, each with a "
        "12-character name, a type and 40 sectors (20 Kbyte). Updating the SD menu never touches them.")))
    docs = [[T('TIPO', 'TYPE'), T('CREATO DA', 'MADE BY'), T('APERTO DA', 'OPENED BY')],
            ['TEXT', T('WRITE, TERM (cattura)', 'WRITE, TERM (capture)'), T('WRITE, ASM (sorgente), TERM (invio)', 'WRITE, ASM (source), TERM (send)')],
            ['SHEET', T('CALC (testo leggibile)', 'CALC (readable text)'), 'CALC, WRITE'],
            ['FILE', 'FILE', 'FILE'], ['CODE', 'MON, ASM', 'MON']]
    add(TBL(docs, [0.16, 0.36, 0.48]))

    # WRITE
    add(H2('WRITE'))
    add(P(T(
        "Un elaboratore di testi nello stile di <i>WordStar</i> (1978): il \"diamante\" di Ctrl muove il "
        "cursore, ^K e ^Q iniziano i comandi di due tasti, le parole vanno a capo da sole a 40 colonne, i "
        "blocchi si vedono in negativo. Un documento contiene fino a 20.480 caratteri. La riga 0 è la barra di "
        "stato (nome, * se modificato, riga, colonna, INS/OVR, prefisso in attesa, byte liberi); la riga 23 "
        "mostra messaggi e domande.",
        "A word processor in the style of <i>WordStar</i> (1978): the Ctrl \"diamond\" moves the cursor, ^K and ^Q "
        "start the two-key commands, words wrap at 40 columns by themselves, blocks show in inverse. A document "
        "holds up to 20,480 characters. Row 0 is the status bar (name, * if changed, line, column, INS/OVR, the "
        "prefix waiting for its letter, free bytes); row 23 shows messages and questions.")))
    add(IMGROW([(APPSHOT / 'write_testsd.png', T('Una lettera.', 'A letter.')),
                (APPSHOT / 'write_block.png', T('Un blocco marcato.', 'A marked block.'))], 72))
    wr = [[T('FUNZIONE', 'FUNCTION'), 'WORDSTAR', T('TASTI', 'KEYS')],
          [T('cursore su / giù / sinistra / destra', 'cursor up / down / left / right'), '^E ^X ^S ^D', T('frecce', 'arrows')],
          [T('parola a sinistra / destra', 'word left / right'), '^A ^F', ''],
          [T('inizio / fine riga', 'start / end of line'), '^QS ^QD', 'Home End'],
          [T('pagina su / giù', 'page up / down'), '^R ^C', 'PgUp PgDn'],
          [T('inizio / fine del testo', 'start / end of text'), '^QR ^QC', ''],
          [T('cancella carattere / a sinistra', 'delete character / left'), '^G / ^H', 'Del / Backspace'],
          [T('cancella parola / riga / fino a fine riga', 'delete word / line / to end of line'), '^T / ^Y / ^QY', ''],
          [T('spezza la riga', 'split the line'), '^N', ''],
          [T('inserimento / sovrascrittura', 'insert / overwrite'), '^V', 'Ins'],
          [T('blocco: inizio, fine, nascondi', 'block begin, end, hide'), '^KB ^KK ^KH', 'F6 F7'],
          [T('blocco: copia, sposta, cancella', 'block copy, move, delete'), '^KC ^KV ^KY', 'F8 F9'],
          [T('vai a inizio / fine blocco', 'go to block begin / end'), '^QB ^QK', ''],
          [T('cerca, cerca ancora', 'find, find again'), '^QF, ^L', 'F4, F5'],
          [T('sostituisci tutto', 'replace all'), '^QA', ''],
          [T('salva, salva con nome', 'save, save as'), '^KS, ^KA', 'F2'],
          [T('apri, nuovo', 'open, new'), '^KO, ^KN', 'F3'],
          [T('salva ed esci, esci', 'save and exit, quit'), '^KX (^KD), ^KQ', T('F10 = esci', 'F10 = quit')],
          [T('aiuto', 'help'), '^J', 'F1']]
    add(TBL(wr, [0.48, 0.27, 0.25], font=7.4))

    # CALC
    add(H2('CALC'))
    add(P(T(
        "Un foglio elettronico nello stile di <i>VisiCalc</i> (1979): 26 x 99 celle, 4 colonne di 9 caratteri "
        "sullo schermo (o più con /W). Una voce che inizia con una lettera o con \" è un'etichetta; le altre "
        "sono valori o formule. I numeri sono a virgola fissa con 2 decimali, da -21.474.836,47 a "
        "21.474.836,47; una divisione per zero o un traboccamento mostrano ERROR. Il foglio si ricalcola dopo "
        "ogni modifica.",
        "A spreadsheet in the style of <i>VisiCalc</i> (1979): 26 x 99 cells, 4 columns of 9 characters on the "
        "screen (or more with /W). An entry that starts with a letter or \" is a label; the others are values or "
        "formulas. Numbers are fixed point with 2 decimals, from -21,474,836.47 to 21,474,836.47; a division by "
        "zero or an overflow shows ERROR. The sheet is recalculated after every change.")))
    add(B([
        T("operatori + - * / con precedenza, parentesi e meno unario;", "operators + - * / with precedence, parentheses and unary minus;"),
        T("celle A1...Z99; $ blocca colonna o riga nella copia ($A$1); una formula che inizia con una cella si scrive con +: <b>+A1*2</b>;",
          "cells A1...Z99; $ keeps the column or row fixed when copying ($A$1); a formula starting with a cell is written with +: <b>+A1*2</b>;"),
        T("@SUM @AVG @MIN @MAX @COUNT su intervalli (A1:C3 o A1...C3) e liste (@SUM(A1,B1,5)); anche @ABS(x) e @INT(x).",
          "@SUM @AVG @MIN @MAX @COUNT on ranges (A1:C3 or A1...C3) and lists (@SUM(A1,B1,5)); also @ABS(x) and @INT(x)."),
    ]))
    add(IMGROW([(APPSHOT / 'calc_testsd.png', T('Un bilancio familiare.', 'A home budget.')),
                (APPSHOT / 'calc_formulas.png', T('Le formule.', 'Formulas.'))], 72))
    ca = [[T('TASTO', 'KEY'), T('FUNZIONE', 'FUNCTION'), T('TASTO', 'KEY'), T('FUNZIONE', 'FUNCTION')],
          [T('frecce, ^E ^X ^S ^D', 'arrows, ^E ^X ^S ^D'), T('muove tra le celle', 'move between cells'), '/B', T('svuota la cella', 'blank the cell')],
          ['Tab', T('cella a destra', 'cell to the right'), '/C', T('cancella il foglio', 'clear the sheet')],
          [T('Invio', 'Enter'), T('cella sotto', 'cell below'), '/R', T('replica: DA una cella o intervallo, A un intervallo', 'replicate: FROM a cell or range, TO a range')],
          ['PgUp PgDn', T('20 righe', '20 rows'), '/W', T('larghezza colonna, 4-18', 'column width, 4-18')],
          ['Home', T('va ad A1', 'go to A1'), '/S /L', T('salva, carica', 'save, load')],
          ['F2', T('modifica la cella', 'edit the cell'), '/Q', T('esci', 'quit')],
          ['Del', T('cancella la cella', 'clear the cell'), '&gt;', T('vai a una cella', 'go to a cell')],
          ['F1', T('aiuto', 'help'), '!', T('ricalcola', 'recalculate')]]
    add(TBL(ca, [0.2, 0.25, 0.1, 0.45], font=7.4))
    add(P(T("Il foglio si salva come testo, una cella per riga (<b>A1 100</b>, <b>B1 +A1*2</b>, <b>D1 \"Totale</b>): WRITE può aprirlo.",
            "A sheet is saved as plain text, one cell per line (<b>A1 100</b>, <b>B1 +A1*2</b>, <b>D1 \"Total</b>): WRITE can open it.")))

    # FILE
    add(H2('FILE'))
    add(P(T(
        "Uno schedario nello stile di <i>PFS:File</i> (1980): un modulo ha fino a 8 campi, ognuno con nome e "
        "larghezza da 1 a 28 caratteri; si vede una scheda alla volta, e le schede si cercano, si ordinano e si "
        "elencano. Parte con un modulo di rubrica (NAME, ADDRESS, CITY, PHONE, EMAIL, BIRTHDAY, NOTES) che "
        "contiene 131 schede; con moduli più piccoli fino a 250.",
        "A card file in the style of <i>PFS:File</i> (1980): a form has up to 8 fields, each with a name and a "
        "width from 1 to 28 characters; one card is shown at a time, and cards can be found, sorted and listed. "
        "It starts with an address book form (NAME, ADDRESS, CITY, PHONE, EMAIL, BIRTHDAY, NOTES) that holds "
        "131 cards; with smaller forms up to 250.")))
    add(IMGROW([(APPSHOT / 'file_card.png', T('Una scheda.', 'A card.')),
                (APPSHOT / 'file_list.png', T('L\'elenco.', 'List view.'))], 72))
    fi = [[T('TASTO', 'KEY'), T('FUNZIONE', 'FUNCTION')],
          [T('↑ ↓ (^E ^X), Tab, Invio', '↑ ↓ (^E ^X), Tab, Enter'), T('campo precedente / successivo', 'previous / next field')],
          ['← → (^S ^D), Home End (^A ^F)', T('cursore nel campo', 'cursor in the field')],
          [T('caratteri', 'characters'), T('scrivono sopra', 'type over')],
          ['Backspace, Del (^G)', T('cancella; il resto del campo si sposta', 'delete; the rest of the field moves')],
          ['PgUp PgDn (^R ^C)', T('scheda precedente / successiva', 'previous / next card')],
          ['^T / ^Z', T('prima / ultima scheda', 'first / last card')],
          ['F3 (^N)', T('nuova scheda dopo quella mostrata', 'new card after the one shown')],
          ['F8 (^Y)', T('cancella la scheda (chiede prima)', 'delete the card (asks first)')],
          ['F2', T('elenco: una scheda per riga; Invio la apre', 'list: one card per line; Enter opens it')],
          ['F4, F5 (^L)', T('cerca un testo in tutti i campi, cerca ancora', 'find a text in every field, find again')],
          ['F6', T('ordina per il campo del cursore', 'sort by the field of the cursor')],
          ['^KS ^KA ^KO', T('salva, salva con nome, apri', 'save, save as, open')],
          ['^KN', T('disegna un nuovo modulo (Invio su un nome vuoto termina)', 'design a new form (Enter on an empty name ends it)')],
          ['^KX, ^KQ (F10)', T('salva ed esci, esci', 'save and exit, quit')],
          ['^J, F1', T('aiuto', 'help')]]
    add(TBL(fi, [0.35, 0.65], font=7.4))

    # DESK
    add(H2('DESK'))
    add(P(T(
        "Gli accessori da scrivania in un programma con tre pagine: <b>F2</b> calcolatrice, <b>F3</b> calendario, "
        "<b>F4</b> orologio; <b>Tab</b> passa alla pagina seguente, <b>F1</b> aiuto, <b>Q</b> o <b>F10</b> torna al menu.",
        "The desk accessories in one program with three pages: <b>F2</b> calculator, <b>F3</b> calendar, <b>F4</b> "
        "clock; <b>Tab</b> goes to the next page, <b>F1</b> help, <b>Q</b> or <b>F10</b> back to the menu.")))
    add(IMGROW([(APPSHOT / 'desk_calculator.png', T('Calcolatrice.', 'Adding machine.')),
                (APPSHOT / 'desk_calendar.png', T('Calendario.', 'Calendar.')),
                (APPSHOT / 'desk_clock.png', T('Orologio.', 'Clock.'))], 50))
    add(B([
        T("<b>Calcolatrice</b> con rotolo di carta: ogni numero va sul rotolo con la sua operazione, il totale è segnato con *. "
          "Cifre e <b>.</b> (11 caratteri), <b>+ - * /</b>, <b>=</b> o Invio (= di nuovo ripete l'ultima operazione), "
          "<b>Esc</b> azzera tutto (dopo un errore è l'unico tasto che funziona), Del/Backspace, <b>S</b> cambia segno, "
          "<b>M N R K</b> = M+ M- MR MC.",
          "<b>Adding machine</b> with a paper tape: every number goes on the tape with its operation, the total is marked with *. "
          "Digits and <b>.</b> (11 characters), <b>+ - * /</b>, <b>=</b> or Enter (= again repeats the last operation), "
          "<b>Esc</b> clears all (after an error it is the only key that works), Del/Backspace, <b>S</b> changes sign, "
          "<b>M N R K</b> = M+ M- MR MC."),
        T("<b>Calendario</b>: un mese, settimane da lunedì, oggi in negativo; ← → cambiano il mese, ↑ ↓ l'anno, Home torna a oggi; ogni anno gregoriano dal 1583.",
          "<b>Calendar</b>: one month, weeks from Monday, today in inverse; ← → change the month, ↑ ↓ the year, Home goes back to today; any Gregorian year from 1583."),
        T("<b>Orologio</b>: cifre grandi, data con il giorno della settimana, sveglia. <b>S</b> imposta data e ora (2026 10 30, 23 59 50), "
          "<b>A</b> la sveglia (07 30), <b>O</b> la spegne; la sveglia lampeggia *** ALARM *** su ogni pagina. "
          "Non c'è un orologio hardware: il tempo è contato con il segnale di fine quadro del TMS9918A e va avanti solo mentre DESK è aperto.",
          "<b>Clock</b>: big digits, the date with the day of the week, the alarm. <b>S</b> sets date and time (2026 10 30, 23 59 50), "
          "<b>A</b> the alarm (07 30), <b>O</b> turns it off; the alarm flashes *** ALARM *** on every page. "
          "There is no hardware clock: time is counted with the end-of-frame flag of the TMS9918A and runs only while DESK is open."),
    ]))

    # TERM
    add(H2('TERM'))
    add(P(T(
        "Il miniVIC diventa un terminale sulla porta seriale, nello stile di <i>VicTerm</i>. Riconosce CR, LF, "
        "BS, TAB, FF e le sequenze ANSI ESC[nJ, ESC[H, ESC[K, ESC[nA/B/C/D; lo schermo scorre in fondo. La "
        "ricezione va a interruzioni in un anello di 256 byte; la cattura tiene fino a 20 Kbyte e si salva "
        "come documento di testo.",
        "The miniVIC becomes a terminal on the serial port, in the style of <i>VicTerm</i>. It understands CR, LF, "
        "BS, TAB, FF and the ANSI sequences ESC[nJ, ESC[H, ESC[K, ESC[nA/B/C/D; the screen scrolls at the bottom. "
        "Reception works by interrupt into a 256-byte ring; the capture holds up to 20 Kbyte and is saved as a "
        "text document.")))
    te = [[T('TASTO', 'KEY'), T('FUNZIONE', 'FUNCTION'), T('TASTO', 'KEY'), T('FUNZIONE', 'FUNCTION')],
          [T('caratteri, Ctrl+lettera', 'characters, Ctrl+letter'), T('inviati come sono', 'sent as they are'), 'F3', T('Invio manda CR LF / CR', 'Enter sends CR LF / CR')],
          [T('Invio', 'Enter'), 'CR (o CR LF)' if L == 'it' else 'CR (or CR LF)', 'F4', T('cattura sì / no', 'capture on / off')],
          [T('frecce', 'arrows'), 'ESC[A ESC[B ESC[C ESC[D', 'F5', T('salva la cattura', 'save the capture')],
          ['Del / Backspace', '$7F / $08', 'F6', T('invia un documento (Esc ferma)', 'send a document (Esc stops)')],
          ['F1', T('aiuto', 'help'), 'F7', T('velocità: 300-19200 baud', 'speed: 300-19200 baud')],
          ['F2', T('eco locale sì / no', 'local echo on / off'), 'F10', T('menu del BIOS (seriale di nuovo a 19200 8N1)', 'BIOS menu (serial back to 19200 8N1)')]]
    add(TBL(te, [0.2, 0.28, 0.1, 0.42], font=7.4))

    # MON
    add(H2('MON'))
    add(P(T(
        "Un monitor nello stile di <i>Supermon</i> e <i>VICMON</i>, in una console che scorre, con comandi di una "
        "lettera e numeri esadecimali. Assembla e disassembla tutto il set del W65C02S; <b>$3000-$7FFF</b> è "
        "libero per i vostri programmi. <b>Esc</b> ferma un elenco lungo.",
        "A monitor in the style of <i>Supermon</i> and <i>VICMON</i>, in a scrolling console, with one-letter "
        "commands and hex numbers. It assembles and disassembles the whole W65C02S set; <b>$3000-$7FFF</b> is "
        "free for your programs. <b>Esc</b> stops a long listing.")))
    add(IMGROW([(APPSHOT / 'mon_memory.png', T('Comandi di memoria.', 'Memory commands.')),
                (APPSHOT / 'mon_disasm.png', T('Assemblatore e disassemblatore.', 'Assembler and disassembler.'))], 72))
    mo = [[T('COMANDO', 'COMMAND'), T('FUNZIONE', 'FUNCTION')],
          ['M [a [b]]', T('dump della memoria, 8 byte per riga con il testo; senza indirizzi continua', 'memory dump, 8 bytes per line with the text; without addresses it goes on')],
          [': a bb bb ...', T('scrive i byte da a (una riga di M si può correggere e reinviare)', 'writes bytes from a (a line of M can be edited and entered again)')],
          ['D [a [b]]', T('disassembla 20 istruzioni, o fino a b', 'disassembles 20 instructions, or up to b')],
          ['A a istr.' if L == 'it' else 'A a instr.', T('assembla una riga, poi propone l\'indirizzo seguente; una riga vuota termina', 'assembles one line, then offers the next address; an empty line ends')],
          ['G a', T('chiama a con JSR; al ritorno mostra A= X= Y= P=', 'calls a with JSR; on RTS shows A= X= Y= P=')],
          ['R', T('i registri dell\'ultimo G', 'the registers of the last G')],
          ['F a b v', T('riempie a..b con v', 'fills a..b with v')],
          ['T a b c', T('copia a..b in c, anche sovrapposti', 'copies a..b to c, overlapping too')],
          ['H a b bb ...', T('cerca fino a 16 byte in a..b', 'hunts up to 16 bytes in a..b')],
          [T('S nome a b', 'S name a b'), T('salva a..b sulla SD come documento CODE', 'saves a..b to the SD as a CODE document')],
          [T('L nome [a]', 'L name [a]'), T('lo carica al suo indirizzo, o ad a', 'loads it at its address, or at a')],
          ['X', T('torna al menu del BIOS', 'back to the BIOS menu')], ['?', T('aiuto', 'help')]]
    add(TBL(mo, [0.22, 0.78], font=7.4))

    # DISK
    add(H2('DISK'))
    add(P(T(
        "Un piccolo DOS: mostra il tipo di scheda (SDSC V1, SDSC V2, SDHC), avvia qualunque programma del menu "
        "SD e gestisce i documenti.",
        "A small DOS: it shows the card type (SDSC V1, SDSC V2, SDHC), runs any program of the SD menu and "
        "manages the documents.")))
    add(IMGROW([(APPSHOT / 'disk_programs.png', T('Programmi.', 'Programs.')),
                (APPSHOT / 'disk_documents.png', T('Documenti.', 'Documents.'))], 72))
    di = [[T('TASTO', 'KEY'), T('FUNZIONE', 'FUNCTION')],
          ['F2 / F3, Tab', T('programmi / documenti', 'programs / documents')],
          [T('frecce (^E ^X), PgUp PgDn', 'arrows (^E ^X), PgUp PgDn'), T('muove nell\'elenco', 'move in the list')],
          [T('Invio su un programma', 'Enter on a program'), T('lo esegue (chiede prima)', 'runs it (asks first)')],
          [T('V, Invio su un documento', 'V, Enter on a document'), T('lo mostra, una schermata alla volta: testo, o esadecimale per CODE', 'views it, one screen at a time: as text, or in hex for CODE')],
          ['R', T('rinomina', 'rename')], ['C', T('copia in uno slot libero con un nome nuovo', 'copy to a free slot with a new name')],
          ['Del', T('cancella (chiede prima)', 'delete (asks first)')],
          ['F', T('formatta: svuota l\'indice dei documenti (chiede prima)', 'format: empty the document index (asks first)')],
          ['Q, F10', T('torna al menu del BIOS', 'back to the BIOS menu')]]
    add(TBL(di, [0.35, 0.65], font=7.4))

    # ASM
    add(H2('ASM'))
    add(P(T(
        "Un assemblatore a due passate nello stile di <i>Assembler 64</i>: assembla un sorgente scritto con WRITE "
        "leggendolo due volte dalla SD, senza caricarlo in RAM, e salva il codice come documento CODE per MON.",
        "A two-pass assembler in the style of <i>Assembler 64</i>: it assembles a source written with WRITE, "
        "reading it twice from the SD without loading it into RAM, and saves the code as a CODE document for MON.")))
    add(B([
        T("Scrivete il sorgente con <b>WRITE</b> e salvatelo (^KS).", "Write the source with <b>WRITE</b> and save it (^KS)."),
        T("Avviate <b>ASM</b> e scegliete il sorgente con le frecce e Invio: ASM mostra gli errori (LINE n: messaggio) oppure OK: $inizio-$fine n BYTES.",
          "Start <b>ASM</b> and choose the source with the arrows and Enter: ASM shows the errors (LINE n: message), or OK: $start-$end n BYTES."),
        T("<b>S</b> salva il codice, <b>A</b> assembla un altro testo, <b>Q</b> torna al menu.",
          "<b>S</b> saves the code, <b>A</b> assembles another text, <b>Q</b> goes back to the menu."),
        T("In <b>MON</b>: L nome carica il codice, G indirizzo lo esegue.", "In <b>MON</b>: L name loads the code, G address runs it."),
    ]))
    asmt = [[T('ELEMENTO', 'ITEM'), T('SINTASSI', 'SYNTAX')],
            [T('riga', 'line'), T('[ETICHETTA[:]] [ISTRUZIONE operando | .DIRETTIVA] [; commento], oppure NOME = espressione',
                                  '[LABEL[:]] [INSTRUCTION operand | .DIRECTIVE] [; comment], or NAME = expression')],
            [T('simboli', 'symbols'), T('lettere, cifre, _; 8 caratteri significativi, fino a 340 simboli', 'letters, digits, _; 8 significant characters, up to 340 symbols')],
            [T('direttive', 'directives'), T('.ORG (predefinito $3000), .BYTE / .TEXT, .WORD, .RES n', '.ORG (default $3000), .BYTE / .TEXT, .WORD, .RES n')],
            [T('espressioni', 'expressions'), T("$esa, %binario, decimale, 'c', *, simboli, + -, meno unario, &lt; byte basso, &gt; byte alto",
                                                "$hex, %binary, decimal, 'c', *, symbols, + -, unary minus, &lt; low byte, &gt; high byte")],
            [T('errori', 'errors'), 'SYNTAX, UNDEFINED SYMBOL, DEFINED TWICE, ADDRESSING MODE, BRANCH TOO FAR, VALUE OVER $FF, OUT OF THE 16 KB AREA, TOO MANY SYMBOLS']]
    add(TBL(asmt, [0.2, 0.8], font=7.4))

    # JUKEBOX
    add(H2('JUKEBOX'))
    add(P(T(
        "Il lettore dei brani di miniVIC Music, in stereo sui due AY-3-8910 (sei voci). Usa il <b>joystick</b>, "
        "non la tastiera né la SD, quindi funziona con qualunque BIOS.",
        "The player of the miniVIC Music songs, in stereo on the two AY-3-8910 (six voices). It uses the "
        "<b>joystick</b>, not the keyboard or the SD card, so it runs with any BIOS.")))
    add(IMGROW([(APPSHOT / 'jukebox_list.png', T('L\'elenco.', 'The list.')),
                (APPSHOT / 'jukebox_play.png', T('Un brano.', 'A song.'))], 72))
    jb = [['JOYSTICK', T('ELENCO', 'LIST'), T('IN RIPRODUZIONE', 'PLAYING')],
          [T('su / giù', 'up / down'), T('sceglie un brano', 'choose a song'), ''],
          [T('fuoco', 'fire'), T('suona; su RANDOM PLAY: tutti i brani una volta in ordine casuale; su EXIT: menu del BIOS',
                                 'play it; on RANDOM PLAY: every song once in random order; on EXIT: BIOS menu'), T('torna all\'elenco', 'back to the list')],
          [T('destra', 'right'), '', T('brano seguente', 'next song')], [T('sinistra', 'left'), '', T('lo suona di nuovo', 'play it again')]]
    add(TBL(jb, [0.18, 0.52, 0.30]))

    # ================================================================ XI. GAMES & MUSIC
    add(H1('XI', T('Giochi e musica', 'Games and music')))
    add(P(T(
        "La collezione <b>miniVIC Games</b> è nel sottomenu <b>GAMES</b> della SD. Sono giochi in assembly 65C02 "
        "con musica stereo: alcuni sono omaggi non commerciali ai classici da sala giochi, gli altri sono "
        "originali. Si giocano con i joystick (giocatore 1 sulla porta JOY 1); i due giocatori giocano a turno "
        "o insieme, come indicato.",
        "The <b>miniVIC Games</b> collection is in the <b>GAMES</b> submenu of the SD. They are games in 65C02 "
        "assembly with stereo music: some are non-commercial tributes to the arcade classics, the others are "
        "originals. They are played with the joysticks (player 1 on the JOY 1 port); the two players play in "
        "turn or together, as shown.")))
    add(H2(T('Record sulla scheda SD', 'Records on the SD card')))
    add(B([
        T("Ogni gioco tiene i suoi <b>8 punteggi migliori</b>, firmati con <b>3 iniziali</b>: dopo la partita, chi entra in classifica firma "
          "(SU / GIÙ cambiano la lettera, SINISTRA / DESTRA si spostano, un pulsante conferma; dopo 30 secondi le iniziali si confermano da sole).",
          "Every game keeps its <b>8 best scores</b>, signed with <b>3 initials</b>: after the game, a player who enters the table signs it "
          "(UP / DOWN change the letter, LEFT / RIGHT move, a button goes on; after 30 seconds the initials are confirmed by themselves)."),
        T("La schermata del titolo mostra la classifica ogni pochi secondi; il punteggio migliore è l'HI del gioco.",
          "The title screen shows the table every few seconds; the best score is the HI of the game."),
        T("Nei giochi uno contro uno (Tank vs Tank, 1 vs 1 Basketball, Warlords, The Warriors) la classifica conta le vittorie di fila contro il computer.",
          "In the one-against-one games (Tank vs Tank, 1 vs 1 Basketball, Warlords, The Warriors) the table counts the wins in a row against the computer."),
        T("I record si scrivono con il BIOS KEYB/SD in un'area dopo i primi 16 Mbyte della scheda, che gli strumenti della SD non sovrascrivono mai; con il BIOS precedente restano in RAM fino allo spegnimento.",
          "Records are written with the KEYB/SD BIOS in an area after the first 16 Mbyte of the card, which the SD tools never overwrite; with the older BIOS they stay in RAM until power-off."),
    ]))
    add(H2(T('Zork I, II, III', 'Zork I, II, III')))
    add(P(T(
        "Le tre avventure testuali Infocom girano, con i file originali (Z-machine versione 3, licenza MIT), sul "
        "<b>miniVIC Z-Machine</b>, un interprete scritto per il miniVIC. La storia viene letta dalla SD (solo "
        "nella SD completa). Ogni storia ha una versione da <b>tastiera</b> (si battono i comandi; Backspace / "
        "Esc correggono, SU richiama l'ultimo comando) e una da <b>joystick</b> (la frase si compone scegliendo le "
        "parole da elenchi: SU / GIÙ l'elenco, SINISTRA / DESTRA la parola, pulsante 1 la aggiunge, pulsante 2 "
        "invia). <b>SAVE</b> e <b>RESTORE</b> tengono tre partite salvate per storia sulla SD.",
        "The three Infocom text adventures run, with the original story files (Z-machine version 3, MIT "
        "licence), on the <b>miniVIC Z-Machine</b>, an interpreter written for the miniVIC. The story is read "
        "from the SD (full SD only). Every story has a <b>keyboard</b> version (type the commands; Backspace / "
        "Esc correct, UP brings back the last command) and a <b>joystick</b> version (the sentence is made of "
        "words chosen from lists: UP / DOWN the list, LEFT / RIGHT the word, button 1 adds it, button 2 sends). "
        "<b>SAVE</b> and <b>RESTORE</b> keep three saved games per story on the SD.")))

    add(H2(T('Elenco dei giochi', 'List of games')))
    G = T('omaggio', 'tribute')
    O = T('originale', 'original')
    games = [
        ('Tank vs Tank', '1-2', O, T('carri armati, sfida', 'tank duel')),
        ('1 vs 1 Basketball', '1-2', O, T('basket uno contro uno', 'one-on-one basketball')),
        ('Centipede', '1', G + ' (Atari)', T('sparatutto', 'shooter')),
        ('Missile Command', '1-2', G + ' (Atari)', T('difesa delle città', 'city defence')),
        ('Lunar Lander', '1', G + ' (Atari)', T('allunaggio', 'moon landing')),
        ('The Warriors', '1-2', O, T('picchiaduro', 'fighting game')),
        ('Breakout', '1-2', G + ' (Atari 1976)', T('mattoncini', 'brick breaker')),
        ('Asteroids', '1-2', G + ' (Atari 1979)', T('sparatutto spaziale', 'space shooter')),
        ('Space Invaders', '1-2', G + ' (Taito 1978)', T('sparatutto', 'shooter')),
        ('Warlords', '1-2', G + ' (Atari 1980)', T('castelli e palla di fuoco', 'castles and fireball')),
        ('Defender', '1', G + ' (Williams 1981)', T('sparatutto a scorrimento', 'scrolling shooter')),
        ('Radar Scope', '1-2', G + ' (Nintendo 1980)', T('sparatutto in prospettiva', 'perspective shooter')),
        ('Space Firebird', '1-2', G + ' (Nintendo 1980)', T('sparatutto', 'shooter')),
        ('Moon Cresta', '1-2', G + ' (Nichibutsu 1980)', T('sparatutto con aggancio', 'shooter with docking')),
        ('Stargate', '1-2', G + ' (Williams 1981)', T('sparatutto a scorrimento', 'scrolling shooter')),
        ('Gravitar', '1-2', G + ' (Atari 1982)', T('navicella e gravità', 'ship and gravity')),
        ('Quantum', '1-2', G + ' (Atari 1982)', T('cattura delle particelle', 'particle trapping')),
        ('Joust', '1-2', G + ' (Williams 1982)', T('giostra volante', 'flying joust')),
        ('Exerion', '1-2', G + ' (Jaleco 1983)', T('sparatutto pseudo-3D', 'pseudo-3D shooter')),
        ('Bubbles', '1-2', G + ' (Williams 1982)', T('pulizia del lavello', 'sink cleaning')),
        ('Times Tables', '1-2', O, T('le tabelline (testi in italiano)', 'times tables (Italian texts)')),
        ('Robert', '1-2', O, T('salti isometrici sui cubi', 'isometric cube hopping')),
        ('Cloud Raider', '1-2', O, T('sparatutto isometrico', 'isometric shooter')),
        ('Crystal Gardens', '1-2', O, T('labirinto isometrico', 'isometric maze')),
        ('Special Forces', '1-2', O, T('azione a scorrimento', 'side-scrolling action')),
        ('Core Runner', '1-2', O, T('volo e piattaforme', 'space run and platforms')),
        ('Deep Space Miner', '1-2', O, T('miniera spaziale', 'space mining shooter')),
        ('Dune Ranger', '1-2', O, T('rover nel deserto', 'desert rover')),
        ('Sky Tug', '1-2', O, T('sparatutto verticale', 'vertical shooter')),
        ('Super Carlo', '1-2', O, T('piattaforme a schermo fisso', 'single-screen platform')),
        ('Ghost &amp; Ghust', '1-2', O, T('piattaforme a schermo fisso', 'single-screen platform')),
        ('Wormer', '1-2', O, T('labirinto, il bruco cresce', 'maze, growing caterpillar')),
        ('Sky Squirrel', '1-2', O, T('salti e planate', 'jump and glide platform')),
        ('Room', '1', O, T('labirinto in prima persona', 'first-person maze shooter')),
        ('Zork I / II / III', '1', 'Infocom', T('avventure testuali (tastiera o joystick)', 'text adventures (keyboard or joystick)')),
        ('Robo Vac', '1-2', O, T('inseguimento nel labirinto', 'maze chase')),
        ('Little 6502 Guy', '1', O, T('vita simulata', 'life-sim toy')),
        ('Hedge Hop', '1-2', O, T('attraversamento', 'crossing game')),
        ('Mole Hole', '1-2', O, T('scavo', 'digging game')),
        ('Lighthouse Keeper', '1-2', O, T('arrampicata', 'climbing game')),
        ('Paint Duel', '1-2', O, T('duello di scie', 'trail duel')),
        ('Lix', '1-2', O, T('conquista del territorio', 'territory game')),
        ('Cheese Chase', '1-2', O, T('scavo e piattaforme', 'digging puzzle platform')),
        ('Haunted Keep', '1-2', O, T('sparatutto nel labirinto', 'maze shooter')),
        ('Pastry Panic', '1-2', O, T('piattaforme', 'platform game')),
        ('Brick Drop', '1-2', O, T('blocchi che cadono', 'falling blocks')),
        ('Turbo Horizon', '1-2', O, T('corse pseudo-3D', 'pseudo-3D racing')),
    ]
    rows = [[T('GIOCO', 'GAME'), T('GIOC.', 'PLAY.'), T('TIPO', 'KIND'), T('GENERE', 'GENRE')]] + [list(g) for g in games]
    add(TBL(rows, [0.28, 0.09, 0.28, 0.35], center_cols=(1,), font=7.4))

    # title screens grid
    add(H2(T('Le schermate dei titoli', 'The title screens'), toc=False))
    shots = sorted(GAMESHOT.glob('*_title.png'))
    from layout import Table, TableStyle, Image as RLImage, picture
    cells, row = [], []
    for f in shots:
        w = 38 * mm
        im = RLImage(str(picture(f)), width=w, height=w * 0.75)
        cap = Paragraph(f.stem.replace('_title', '').replace('_', ' ').upper(), S['caption'])
        row.append([im, cap])
        if len(row) == 4:
            cells.append(row); row = []
    if row:
        cells.append(row + [''] * (4 - len(row)))
    t = Table(cells, colWidths=[BODY_W / 4] * 4)
    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    add([t])

    add(H2(T('Musica', 'Music')))
    add(P(T(
        "Il sottomenu <b>SOUNDS</b> contiene i brani: ognuno è un piccolo programma che suona il brano in "
        "continuazione e ne mostra il titolo; il fuoco del joystick torna al menu. JUKEBOX (sottomenu APPS) li "
        "suona tutti.",
        "The <b>SOUNDS</b> submenu holds the songs: each one is a small program that plays the song again and "
        "again and shows its title; joystick fire goes back to the menu. JUKEBOX (APPS submenu) plays all of them.")))
    songs = [[T('BRANO', 'SONG'), T('AUTORE', 'COMPOSER'), T('DURATA', 'LENGTH')],
             ['In the Hall of the Mountain King', 'Edvard Grieg, 1875', '75 s'], ['Korobeiniki', T('canto popolare russo', 'Russian folk song'), '66 s'],
             ['The Entertainer', 'Scott Joplin, 1902', '39 s'], ['Toccata and Fugue in D Minor', T('J. S. Bach, 1704 circa', 'J. S. Bach, about 1704'), '43 s'],
             ['Arcade Start', O, '5 s'], ['Star Patrol', O, '56 s'], ['Neon Drive', O, '81 s'],
             ['Level Clear and Game Over', O, '11 s'], ['Flight of the Bumblebee', 'N. Rimsky-Korsakov, 1900', '32 s'],
             ['Rondo alla Turca', 'W. A. Mozart, 1783', '49 s'], ['Can-Can (Galop Infernal)', 'Jacques Offenbach, 1858', '37 s'],
             ['William Tell Overture, finale', 'Gioachino Rossini, 1829', '33 s'], ['Für Elise', 'L. van Beethoven, 1810', '44 s'],
             ['Maze Chase', O, '49 s'], ['Dungeon Boss', O, '45 s'], ['High Score', O, '43 s']]
    add(TBL(songs, [0.5, 0.36, 0.14], center_cols=(2,), font=7.4))
    add(P(T("Sulla SD ci sono anche Imperial March, The Final Countdown e Super Mario Bros.",
            "The SD also holds Imperial March, The Final Countdown and Super Mario Bros.")))

    # ================================================================ XII. SD CARD
    add(H1('XII', T('La scheda SD', 'The SD card')))
    add(P(T(
        "La SD non ha un filesystem: è un'immagine \"grezza\" che si prepara sul PC con <b>bo6502-SDbuilder</b> "
        "(https://github.com/Boogs77/bo6502-SDbuilder) e si scrive sulla scheda con un programma come Win32 Disk "
        "Imager o dd. Il BIOS legge i programmi dai settori, senza nomi di file.",
        "The SD has no filesystem: it is a raw image prepared on the PC with <b>bo6502-SDbuilder</b> "
        "(https://github.com/Boogs77/bo6502-SDbuilder) and written to the card with a program such as Win32 Disk "
        "Imager or dd. The BIOS reads the programs from the sectors, with no file names.")))
    add(H2(T('Preparare la scheda', 'Preparing the card')))
    sdm = [[T('MODO', 'MODE'), T('CONTENUTO', 'CONTENTS'), T('FILE', 'FILE'), 'BIOS'],
           ['games', T('giochi e brani', 'games and songs'), 'sd.img', T('qualunque', 'any')],
           ['full', T('giochi, applicativi, brani, documenti di esempio, storie di Zork', 'games, applications, songs, sample documents, Zork stories'), 'sd_full.img (16 MB)', 'KEYB/SD']]
    add(TBL(sdm, [0.12, 0.48, 0.22, 0.18]))
    add(CODE("""python update_sd.py --mode full --dry-run   # list the full SD
python update_sd.py --mode full             # -> sd_full.img (16 MB)"""))
    add(P(T(
        "Scrivete l'immagine intera sulla scheda (con dd o Win32 Disk Imager), così ci sono anche i documenti. "
        "Una scheda di qualunque capacità va bene; l'area dei record, dopo i 16 Mbyte, non viene mai "
        "sovrascritta.",
        "Write the whole image to the card (with dd or Win32 Disk Imager), so that the documents are there too. "
        "A card of any capacity is fine; the record area, after 16 Mbyte, is never overwritten.")))
    add(H2(T('Organizzazione della scheda', 'Card layout')))
    lay = [[T('SETTORI', 'SECTORS'), T('BYTE', 'BYTES'), T('CONTENUTO', 'CONTENTS')],
           ['0 - 16383', '$00000000', T('255 blocchi di programma da 32 Kbyte (64 settori)', '255 program blocks of 32 Kbyte (64 sectors)')],
           ['16384 - 16983', '$00800000', T('indice "DOCS" e 15 documenti da 40 settori', '"DOCS" index and 15 documents of 40 sectors')],
           ['20480 - ...', '$00A00000', T('indice "ZSTO" e storie dello Z-Machine (256 settori l\'una)', '"ZSTO" index and Z-Machine stories (256 sectors each)')],
           ['32768 - 36863', '$01000000', T('area di salvataggio: 256 zone da 16 settori (record, partite)', 'save area: 256 zones of 16 sectors (records, saved games)')]]
    add(TBL(lay, [0.2, 0.17, 0.63]))
    add(H3(T('Un blocco di programma', 'A program block')))
    blk = [[T('POSIZIONE NEL BLOCCO', 'OFFSET IN THE BLOCK'), T('CONTENUTO', 'CONTENTS')],
           [T('+$0000 (settore 0)', '+$0000 (sector 0)'), T('pagina P della directory, nel blocco P (solo nei primi blocchi)', 'directory page P, in block P (only in the first blocks)')],
           [T('+$0200 (settore 1)', '+$0200 (sector 1)'), T('riga di informazioni ASCII (slot, file, carico, lunghezza, avvio, CRC32)', 'ASCII info line (slot, file, load, length, entry, CRC32)')],
           ['+$1000 - +$7FFF', T('i byte del programma (al massimo $7000 = 28 Kbyte)', 'the program bytes (at most $7000 = 28 Kbyte)')]]
    add(TBL(blk, [0.3, 0.7]))
    add(P(T("Il programma N (da 1) sta all'indirizzo (N-1) x $8000, cioè dal settore (N-1) x 64; i dati dal settore (N-1) x 64 + 8.",
            "Program N (from 1) is at address (N-1) x $8000, that is from sector (N-1) x 64; its data from sector (N-1) x 64 + 8.")))
    add(H3(T('Il settore della directory (versione 3)', 'The directory sector (version 3)')))
    dr = [[T('OFFSET', 'OFFSET'), T('BYTE', 'SIZE'), T('CAMPO', 'FIELD')],
          ['0', '4', T('firma "BOGS"', 'magic "BOGS"')], ['4', '1', T('versione (3)', 'version (3)')],
          ['5', '1', T('programmi in questa pagina (1-9)', 'programs on this page (1-9)')],
          ['6', '9', T('flag di ogni voce (bit 0 = esegui dopo il caricamento)', 'flags of each entry (bit 0 = run after loading)')],
          ['15', '1', T('numero totale dei programmi', 'total number of programs')],
          ['16 + i*8', '8', T('carico (lo,hi), lunghezza (lo,hi), avvio (lo,hi), tipo, lunghezza del nome seriale', 'load (lo,hi), length (lo,hi), entry (lo,hi), type, serial name length')],
          ['96 + i*32', '32', T('nome ASCII (al massimo 31 caratteri + $00)', 'ASCII name (at most 31 characters + $00)')]]
    add(TBL(dr, [0.15, 0.1, 0.75], center_cols=(1,)))
    add(P(T("Tipo: 0 nessuno, 1 GAME, 2 APP, 3 TOOL, 4 SOUND.", "Type: 0 none, 1 GAME, 2 APP, 3 TOOL, 4 SOUND.")))
    add(H3(T('Area di salvataggio', 'Save area')))
    add(P(T(
        "La zona z (0-255) occupa i settori 32768 + z x 16 ... +15. I giochi hanno zone fisse da 1 a 127, gli "
        "applicativi da 128 a 255. I settori 0 e 1 di una zona tengono i record in due copie alternate (firma "
        "\"MVSV\", versione, zona, tabelle, righe, contatore delle scritture, nome del gioco, righe con punteggio "
        "BCD e 3 iniziali, somma di controllo a +510); i settori 2-15 sono liberi per il gioco (partite salvate). "
        "Lo strumento <b>saves.py</b> e l'emulatore esportano e importano l'area come file .json.",
        "Zone z (0-255) takes sectors 32768 + z x 16 ... +15. Games have fixed zones from 1 to 127, "
        "applications from 128 to 255. Sectors 0 and 1 of a zone hold the records in two alternating copies "
        "(magic \"MVSV\", version, zone, tables, rows, write counter, game name, rows with BCD score and 3 "
        "initials, checksum at +510); sectors 2-15 are free for the game (saved games). The <b>saves.py</b> tool "
        "and the emulator export and import the area as a .json file.")))

    # ================================================================ APPENDIX
    add(H1('A', T('Appendice', 'Appendix')))
    add(H2(T('L\'emulatore nel browser', 'The browser emulator')))
    add(P(T(
        "<b>BO6502 · miniVIC Emulator</b> (https://boogs77.github.io/BO6502-miniVIC-emulator/) fa girare il BIOS "
        "vero, i giochi, gli applicativi e la SD completa in un browser, con tastiera e joystick virtuali, "
        "pannelli per la seriale, l'audio e il debug. È il modo più semplice per provare il miniVIC senza la scheda.",
        "<b>BO6502 · miniVIC Emulator</b> (https://boogs77.github.io/BO6502-miniVIC-emulator/) runs the real "
        "BIOS, the games, the applications and the full SD in a browser, with a virtual keyboard and joysticks "
        "and panels for the serial port, the audio and debugging. It is the easiest way to try the miniVIC "
        "without the board.")))
    add(H2(T('Versioni del firmware', 'Firmware versions')))
    fw = [[T('VERSIONE', 'VERSION'), T('NOVITÀ', 'CHANGES')],
          ['30.09.26', T('menu SD con più pagine, trampolino NMI a $0FD0', 'SD menu with several pages, NMI trampoline at $0FD0')],
          ['24.10.26', T('menu SD: i tasti A/D non cambiano più pagina due volte', 'SD menu: the A/D keys no longer change page twice')],
          ['27.10.26 KEYB/SD', T('tastiera estesa, lettura e scrittura su SDSC v1/v2 e SDHC, tabella dei salti $FD18-$FD21', 'extended keyboard, read and write on SDSC v1/v2 and SDHC, jump table $FD18-$FD21')],
          ['03.11.26 KEYB/SD', T('sottomenu GAMES, APPS, SOUNDS, ALL', 'GAMES, APPS, SOUNDS, ALL submenus')],
          ['16.11.26 KEYB/SD', T('un solo Invio all\'avvio del BASIC; buffer della tastiera a $0380', 'one Enter at the BASIC start-up; keyboard buffer at $0380')],
          ['16.11.26 KEYB/SD R2', T('Backspace nel BASIC, tabelle della tastiera classica corrette, indirizzi giusti in System Information', 'Backspace in BASIC, classic keyboard tables fixed, right addresses in System Information')]]
    add(TBL(fw, [0.28, 0.72]))
    add(H2(T('Collegamenti', 'Links')))
    add(TBL([[T('PROGETTO', 'PROJECT'), 'URL'],
             [T('Hardware miniVIC', 'miniVIC hardware'), 'https://github.com/Boogs77/miniVIC_65c02'],
             ['BIOS', 'https://github.com/Boogs77/miniVIC_bios'],
             [T('Giochi', 'Games'), 'https://github.com/Boogs77/miniVIC_games'],
             [T('Applicativi', 'Applications'), 'https://github.com/Boogs77/miniVIC_apps'],
             [T('Musica', 'Music'), 'https://github.com/Boogs77/miniVIC_music'],
             ['SD builder', 'https://github.com/Boogs77/bo6502-SDbuilder'],
             [T('Emulatore', 'Emulator'), 'https://github.com/Boogs77/BO6502-miniVIC-emulator'],
             ['BO6502', 'https://github.com/Boogs77/BO6502_65C02-based_modular_computer'],
             ['Microsoft BASIC (msbasic)', 'https://github.com/mist64/msbasic']], [0.32, 0.68]))
    add(SPACE(10))
    add([Paragraph(T('<i>Creato da Boogs77 - 2026</i>', '<i>Created by Boogs77 - 2026</i>'), S['caption'])])
    return st
