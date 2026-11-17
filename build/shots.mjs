// Bundles shots.ts against the emulator sources and runs it: node build/shots.mjs
import { createRequire } from 'node:module';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
const here = dirname(fileURLToPath(import.meta.url)).split('\\').join('/');
const root = join(here, '..', '..').split('\\').join('/');
const EMU = root + '/bo6502-emulator';
const { build } = createRequire(EMU + '/package.json')('esbuild');
const out = here + '/shots.out.mjs';
await build({
  entryPoints: [here + '/shots.ts'], outfile: out, bundle: true, platform: 'node', format: 'esm',
  logLevel: 'error', alias: { EMU },
  banner: { js: "import { createRequire as __cr } from 'node:module'; const require = __cr(import.meta.url);" },
  define: {
    __OUT__: JSON.stringify(here + '/img/screens'),
    __ROM__: JSON.stringify(root + '/miniVIC BIOS/bin/boogs.bin'),
    __SD__: JSON.stringify(root + '/bo6502-SDbuilder/sd_full.img'),
  },
});
const mod = await import(pathToFileURL(out).href);
await mod.default();
