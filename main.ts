// Post the Meme, Win the Feed — entry program.
//
// make.fun bounty: u-myronera-post-the-meme-win-the-feed-2de960bf
// "Post the Meme, Win the Feed" ($2 in USDC)
//
// The entry is one meme about make.fun, aimed at people who build AI
// agents, posted from the entrant's own public X account tagging
// @_myronera. The meme image (meme.png) is drawn in code by
// draw-meme.py; this program is the entry's runnable record of the post:
//
//   - it checks meme.png is present and exactly 1200x675,
//   - it reads POST.json next to it and prints the URL of the X post.
//
// Usage:
//   node main.ts
//
// Standard library only (node:fs, node:path, node:url). No network, no
// randomness. While the post is still pending, the program prints a
// PENDING line instead of a URL.

import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const dir = dirname(fileURLToPath(import.meta.url));
const postPath = join(dir, "POST.json");
const memePath = join(dir, "meme.png");

function pngSize(path: string): [number, number] | null {
  if (!existsSync(path)) return null;
  const b = readFileSync(path);
  if (b.length < 24) return null;
  // PNG signature: 89 50 4E 47 0D 0A 1A 0A
  if (b[0] !== 0x89 || b[1] !== 0x50 || b[2] !== 0x4e || b[3] !== 0x47) {
    return null;
  }
  // IHDR width / height are big-endian uint32 at offsets 16 and 20.
  return [b.readUInt32BE(16), b.readUInt32BE(20)];
}

const meme = pngSize(memePath);
if (meme === null) {
  console.error(`meme.png missing or not a PNG: ${memePath}`);
  process.exit(1);
}
if (meme[0] !== 1200 || meme[1] !== 675) {
  console.error(`meme.png is ${meme[0]}x${meme[1]}, expected 1200x675`);
  process.exit(1);
}
console.error(`meme.png OK: ${meme[0]}x${meme[1]}`);

type PostFile = { url?: unknown; status?: unknown };
const post = JSON.parse(readFileSync(postPath, "utf8")) as PostFile;

if (typeof post.url === "string" && /^https?:\/\//.test(post.url)) {
  console.log(post.url);
} else {
  console.log(
    "PENDING — no X post yet: post meme.png from a public X account " +
      "tagging @_myronera, then put the post URL in POST.json",
  );
}
