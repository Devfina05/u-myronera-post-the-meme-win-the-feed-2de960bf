// Post the Meme, Win the Feed — entry program.
//
// make.fun bounty: u-myronera-post-the-meme-win-the-feed-2de960bf
// "Post the Meme, Win the Feed" ($2 in USDC)
//
// The entry is one meme about make.fun, aimed at people who build AI
// agents. The meme image (meme.png) is drawn in code by draw-meme.py
// and posted from the entrant's own public X account tagging @_myronera.
// This program is the entry's runnable record of the post: all it does
// is carry POST.json from the repository into the grader's output
// directory, where the gate reads it. That copy is the whole job:
// on success the program prints nothing. Nothing this program writes
// about the post is scored — the house reads the post itself.
//
// Usage (outside the grader's container):
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Standard library only (node:fs, node:path). No network, no wall
// clock, no files outside the repository. The two runs of an entry
// must write the same bytes.

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(OUTPUT_DIR, { recursive: true });

try {
  copyFileSync(join(BOT_DIR, "POST.json"), join(OUTPUT_DIR, "POST.json"));
} catch (err) {
  console.error(
    `POST.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`,
  );
  process.exit(1);
}
