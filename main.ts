// news-image-20261121 entry (Node 22, standard library only, no network).
//
// The finished infographic is entry.png beside this file. It was drawn in
// this session by gen_image.py (Python PIL, no AI image generator, no
// copyrighted images) from the verified research in RESEARCH.md: seven
// world-news stories of Saturday 21 November 2026, each checked against at
// least two independent reports. This program copies it to the output
// directory and verifies the copy, so two runs write byte-identical output.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
const source = join(root, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

if (!existsSync(source)) {
  throw new Error(`missing entry image: ${source}`);
}
const bytes = readFileSync(source);

// PNG signature: 89 50 4E 47 0D 0A 1A 0A.
const signature = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
for (let i = 0; i < signature.length; i++) {
  if (bytes[i] !== signature[i]) {
    throw new Error('entry.png is not a PNG file');
  }
}

// IHDR width and height are big-endian uint32 at offsets 16 and 20.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}
if (bytes.length > 1024 * 1024) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// Verify the copy is byte-identical to the source image.
const digest = (path: string): string =>
  createHash('sha256').update(readFileSync(path)).digest('hex');
if (digest(source) !== digest(target)) {
  throw new Error('output differs from entry.png');
}
console.log(
  `wrote ${target} (${width}x${height}, ${bytes.length} bytes, ` +
    `sha256 ${digest(target).slice(0, 16)}...)`,
);
