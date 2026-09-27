// Usage: node tools/extract.js <board.html> <out.json>
// Pulls the `var T = ...; var CHATS = [...]` block out of the Papan Sekolah board and writes it as JSON.
const fs = require('fs');
const [, , src, out] = process.argv;
if (!src || !out) { console.error('usage: node tools/extract.js <board.html> <out.json>'); process.exit(1); }
const html = fs.readFileSync(src, 'utf8');
const a = html.indexOf('var T = '), b = html.indexOf('var MS=');
if (a < 0 || b < 0) { console.error('CHATS block not found'); process.exit(1); }
const vm = require('vm'); const ctx = {};
vm.runInNewContext(html.slice(a, b) + '\n;this.__T=T;this.__C=CHATS;', ctx);
fs.writeFileSync(out, JSON.stringify({ T: ctx.__T, chats: ctx.__C, builtAt: new Date().toISOString() }));
console.log('wrote', out, ctx.__C.length, 'groups');
