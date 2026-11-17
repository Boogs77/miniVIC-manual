// shots.ts - takes the BIOS screenshots used in the manual, on the bo6502-emulator core
// with the miniVIC BIOS KEYB/SD and the full SD of bo6502-SDbuilder.
import { readFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { buildMachine, defaultConfig } from 'EMU/src/machines/profiles';
import { SdCardBoard, KeyboardBoard } from 'EMU/src/boards/Boards';
import { screenText, runFrames, writePng } from 'EMU/tests/helpers';
import { TMS_PALETTE, SCREEN_W, SCREEN_H } from 'EMU/src/devices/TMS9918A';

declare const __OUT__: string;
declare const __ROM__: string;
declare const __SD__: string;

export default async function () {
  mkdirSync(__OUT__, { recursive: true });
  const m: any = buildMachine(defaultConfig('minivic'));
  m.loadRom(new Uint8Array(readFileSync(__ROM__)));
  (m.board<SdCardBoard>('sdcard')! as any).card.insert(new Uint8Array(readFileSync(__SD__)));
  m.powerOn();
  const kb = () => m.board<KeyboardBoard>('keyboard')!.keyboard;
  const key = (code: string, mods: string[] = []) => {
    for (const x of mods) kb().keyDown(x);
    kb().keyDown(code); runFrames(m, 3); kb().keyUp(code); runFrames(m, 3);
    for (const x of mods) kb().keyUp(x);
    runFrames(m, 4);
  };
  const SH: Record<string, string> = { ':': 'Semicolon', '"': 'Quote', '?': 'Slash', '$': 'Digit4', '(': 'Digit9', ')': 'Digit0', '*': 'Digit8', '+': 'Equal', '<': 'Comma', '>': 'Period' };
  const PL: Record<string, string> = { ' ': 'Space', '.': 'Period', ',': 'Comma', ';': 'Semicolon', '-': 'Minus', '/': 'Slash', '=': 'Equal', '\n': 'Enter' };
  const type = (s: string) => {
    for (const ch of s) {
      if (/[a-z]/.test(ch)) key('Key' + ch.toUpperCase());
      else if (/[A-Z]/.test(ch)) key('Key' + ch, ['ShiftLeft']);
      else if (/[0-9]/.test(ch)) key('Digit' + ch);
      else if (PL[ch]) key(PL[ch]);
      else if (SH[ch]) key(SH[ch], ['ShiftLeft']);
    }
  };
  const shot = (name: string) => {
    runFrames(m, 3);
    const vdp = m.vdu!.vdp;
    const f = writePng(name, SCREEN_W * 2, SCREEN_H * 2, (x, y) => TMS_PALETTE[vdp.frame[(y >> 1) * SCREEN_W + (x >> 1)]]);
    const dst = join(__OUT__, name + '.png');
    require('node:fs').copyFileSync(f, dst);
    console.log('shot', name, '\n' + screenText(m));
  };
  const waitFor = (txt: string, max = 2000) => {
    for (let f = 0; f < max; f += 10) { if (screenText(m).includes(txt)) return; runFrames(m, 10); }
    console.log('TIMEOUT waiting for', txt, '\n' + screenText(m));
  };

  runFrames(m, 120);
  shot('menu_main');

  key('Digit4'); waitFor('Press any key'); runFrames(m, 30); shot('menu_info');
  key('Space'); runFrames(m, 60);

  key('Digit3'); waitFor('SD PROGRAMS MENU'); runFrames(m, 20); shot('menu_sd');
  key('Digit1'); waitFor('SD GAMES'); waitFor('Select >'); runFrames(m, 30); shot('menu_games');
  key('Escape'); waitFor('SD PROGRAMS MENU'); runFrames(m, 20);
  key('Digit2'); waitFor('SD APPS'); waitFor('Select >'); runFrames(m, 30); shot('menu_apps');
  key('Escape'); waitFor('SD PROGRAMS MENU'); runFrames(m, 20);
  key('Digit3'); waitFor('SD SOUNDS'); waitFor('Select >'); runFrames(m, 30); shot('menu_sounds');
  key('Escape'); waitFor('SD PROGRAMS MENU'); runFrames(m, 20);
  key('Digit4'); waitFor('SD ALL PROGRAMS'); waitFor('Select >'); runFrames(m, 30); shot('menu_all');
  key('Escape'); runFrames(m, 30); key('Escape'); runFrames(m, 60);

  // WozMon
  m.powerOn(); runFrames(m, 120);
  key('Digit1'); runFrames(m, 60);
  type('FFFA.FFFF\n'); runFrames(m, 20);
  type('3000: A9 41 20 00 FD 4C 10 FE\n'); runFrames(m, 20);
  type('3000.3007\n'); runFrames(m, 20);
  type('3000R\n'); runFrames(m, 30);
  shot('wozmon');

  // BASIC (fresh machine: WozMon has no exit)
  m.powerOn(); runFrames(m, 120);
  key('Digit2'); runFrames(m, 120);
  key('Enter'); runFrames(m, 200);
  key('Enter'); runFrames(m, 120);
  type('10 FOR I=1 TO 5\n20 PRINT I,I*I\n30 NEXT\nRUN\n'); runFrames(m, 120);
  shot('basic');
}
