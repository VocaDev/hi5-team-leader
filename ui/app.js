const VIEW_URL = 'sample_view.json';

// ===== GENTI: lidh këto 4 funksione me serverin (UI-ja vetëm i thërret) =====
async function sendMessage(text) { console.log('sendMessage', text); }
async function approve() { console.log('approve'); }
async function answer(taskId, action) { console.log('answer', taskId, action); } // action: "accept" | "decline"
async function reset() { console.log('reset'); }
// =============================================================================

const $ = id => document.getElementById(id);
const STATUS = {planned: 'Planifikuar', sent: 'Dërguar', accepted: '✅ Pranuar', declined: '❌ Refuzuar'};
const JOB = {draft: 'Draft', awaiting_approval: 'Pret miratimin', sent: 'Dërguar', confirmed: '✅ Konfirmuar'};
let last = '';

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined) e.textContent = text;
  return e;
}

function render(v) {
  const job = v.job || {};
  $('jobTitle').textContent = job.title ? `${job.title} · ${job.zone || ''} · ${job.start || ''}` : 'Plani';
  const jp = $('jobPill');
  jp.textContent = job.status ? (JOB[job.status] || job.status) : 'S\'ka punë';
  $('approveBtn').disabled = job.status !== 'awaiting_approval';

  $('busy').hidden = !v.busy;
  $('summary').textContent = job.summary || '';
  $('existing').replaceChildren(...((v.existing_jobs || []).map(e => el('div', 'ex', `${e.title || e.id} · ${e.zone || ''} · ${e.from || ''}–${e.to || ''}` + (e.workers ? ' · ' + (Array.isArray(e.workers) ? e.workers : Object.keys(e.workers)).join(', ') : '')))));
  const sent = (v.tasks || []).filter(t => t.status === 'sent');
  $('phones').replaceChildren(...(sent.length ? sent.map(t => {
    const r = el('div', 'ph'); r.append(el('span', '', `${t.worker}: ${t.role}`));
    [['accept', 'ACCEPT', 'btn btn-go btn-sm'], ['decline', "S'MUNDEM", 'btn btn-sm']].forEach(([a, l, cls]) => {
      const b = el('button', cls, l);
      b.onclick = async () => { b.disabled = true; try { await answer(t.id, a); } catch (e) { $('msgNote').textContent = 'Dështoi.'; } poll(); };
      r.append(b);
    });
    return r;
  }) : [el('div', 'empty', 'S\'ka detyra në pritje.')]));

  const bl = $('blocked'), blocked = v.blocked || [];
  bl.hidden = !blocked.length;
  bl.replaceChildren(...blocked.map(b => el('div', '', '⛔ BLLOKUAR: ' + b.text)));

  // plani: sipas personit, pastaj sipas orës
  const tasks = (v.tasks || []).slice().sort((a, b) => (a.from || '').localeCompare(b.from || ''));
  const byWorker = {};
  tasks.forEach(t => (byWorker[t.worker] = byWorker[t.worker] || []).push(t));
  const plan = $('plan');
  if (!tasks.length) plan.replaceChildren(el('div', 'empty', 'Ende s\'ka plan. Shkruaje punën më lart.'));
  else plan.replaceChildren(...Object.entries(byWorker).map(([name, list]) => {
    const p = el('div', 'person');
    p.append(el('h3', '', name));
    list.forEach(t => {
      const row = el('div', 'task st-' + t.status);
      row.append(el('div', 'time', `${t.from}–${t.to}`));
      const mid = el('div');
      mid.append(el('div', '', t.role));
      if (t.bring && t.bring.length) mid.append(el('div', 'bring', 'Merr: ' + t.bring.join(', ')));
      if (t.note) mid.append(el('div', 'bring', t.note));
      row.append(mid, el('span', 'badge b-' + t.status, STATUS[t.status] || t.status));
      p.append(row);
    });
    return p;
  }));

  // punëtorët: statusi vjen nga detyrat e tyre
  $('workers').replaceChildren(...(v.workers || []).map(w => {
    const mine = tasks.filter(t => t.worker === w.name).map(t => t.status);
    let st = mine.includes('declined') ? 'declined' : mine.length && mine.every(s => s === 'accepted') ? 'accepted'
      : mine.includes('sent') ? 'sent' : 'planned';
    const label = mine.length ? STATUS[st] : (w.status === 'busy' ? 'i zënë' : 'i lirë');
    const d = el('div', 'worker');
    d.append(el('b', '', w.name), el('span', 'badge b-' + (mine.length ? st : 'planned'), label));
    return d;
  }));

  const feed = $('feed'), atBottom = feed.scrollTop + feed.clientHeight >= feed.scrollHeight - 20;
  feed.replaceChildren(...(v.feed || []).map(f => {
    const d = el('div', 'fi ' + f.type);
    d.append(el('span', 't', f.t), el('span', '', f.text));
    return d;
  }));
  if (atBottom) feed.scrollTop = feed.scrollHeight;
}

function setConn(ok) {
  const c = $('conn');
  c.textContent = ok ? 'live' : 'pa lidhje';
  c.className = 'pill ' + (ok ? 'pill-on' : 'pill-off');
}

async function poll() {
  try {
    const r = await fetch(VIEW_URL, {cache: 'no-store'});
    if (!r.ok) throw new Error(r.status);
    const text = await r.text();
    if (text !== last) { last = text; render(JSON.parse(text)); }
    setConn(true);
  } catch (e) { setConn(false); }
}

$('sendBtn').onclick = async () => {
  const text = $('msg').value.trim();
  if (!text) return;
  $('sendBtn').disabled = true; $('msgNote').textContent = '';
  try { await sendMessage(text); $('msg').value = ''; $('msgNote').textContent = 'Dërguar: "' + text + '" → shiko feed-in djathtas.'; }
  catch (e) { $('msgNote').textContent = 'Dështoi (backend-i s\'është gati?)'; }
  $('sendBtn').disabled = false;
};

$('resetBtn').onclick = async () => {
  try { await reset(); $('msgNote').textContent = 'U rivendos.'; } catch (e) { $('msgNote').textContent = 'Reset dështoi.'; }
  poll();
};

$('approveBtn').onclick = async () => {
  $('approveBtn').disabled = true;
  try { await approve(); } catch (e) { $('msgNote').textContent = 'Miratimi dështoi.'; }
  poll();
};

poll(); setInterval(poll, 1000);