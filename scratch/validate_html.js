const fs = require('fs');
const html = fs.readFileSync('bigpy_all_in_one.html', 'utf-8');

// Only validate the body content after the closing </style> tags in the <head>-ish preamble.
// We'll scan the whole file but ignore <style>...</style> and <script>...</script> contents.
const voidTags = new Set(['br','img','meta','link','input','hr','col','area','base','source','track','wbr']);

let i = 0;
const stack = [];
const lines = html.split('\n');
let lineNo = 1;
let charIdx = 0;

// Build line index for offsets
const lineStarts = [0];
for (let k=0;k<html.length;k++){ if(html[k]==='\n') lineStarts.push(k+1); }
function lineOf(pos){
  let lo=0, hi=lineStarts.length-1;
  while(lo<hi){ const mid=(lo+hi+1)>>1; if(lineStarts[mid]<=pos) lo=mid; else hi=mid-1; }
  return lo+1;
}

const tagRe = /<(\/?)([a-zA-Z][a-zA-Z0-9]*)((?:\s+[^<>]*?)?)(\/?)>/g;
let m;
let inStyle = false, inScript = false;
let firstMismatch = null;
let mismatchCount = 0;

while((m = tagRe.exec(html)) !== null){
  const [full, closing, tagRaw, attrs, selfClose] = m;
  const tag = tagRaw.toLowerCase();
  const pos = m.index;

  if (tag === 'style'){ inStyle = !closing; if(closing) inStyle=false; continue; }
  if (tag === 'script'){ inScript = !closing; if(closing) inScript=false; continue; }
  if (inStyle || inScript) continue;
  if (voidTags.has(tag)) continue;
  if (tag === 'title' || tag === 'meta' || tag === 'link' || tag === 'base') continue;

  if (!closing){
    if (selfClose === '/') continue; // self-closed like <br/>
    stack.push({tag, pos});
  } else {
    // find matching from top
    let found = -1;
    for(let s=stack.length-1; s>=0; s--){
      if(stack[s].tag === tag){ found = s; break; }
    }
    if (found === -1){
      mismatchCount++;
      if(!firstMismatch) firstMismatch = {type:'unmatched-close', tag, line: lineOf(pos)};
      console.log(`[line ${lineOf(pos)}] UNMATCHED CLOSE </${tag}> — no open <${tag}> on stack`);
    } else {
      if (found !== stack.length-1){
        mismatchCount++;
        if(!firstMismatch) firstMismatch = {type:'skip-close', tag, line: lineOf(pos)};
        const skipped = stack.slice(found+1).map(x=>x.tag+'@'+lineOf(x.pos)).join(', ');
        console.log(`[line ${lineOf(pos)}] CLOSE </${tag}> closes out of order; still-open above it: ${skipped}`);
      }
      stack.length = found;
    }
  }
}

console.log('---');
console.log('Remaining open (never closed) at EOF:', stack.map(x=>x.tag+'@line'+lineOf(x.pos)).join(', ') || '(none)');
console.log('Total mismatch events:', mismatchCount);
