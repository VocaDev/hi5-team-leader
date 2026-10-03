// Served by the backend (python -m src.server -> http://localhost:8000) = same origin.
// Opened as a file -> sample_view.json (read-only preview).
const LIVE = location.protocol.startsWith('http') && !location.pathname.endsWith('sample.html');
const API = LIVE ? '' : 'http://localhost:8000';
const VIEW_URL = LIVE ? '/api/view' : 'sample_view.json';
let VIEW = {};

async function post(path, body) {
  const r = await fetch(API + path, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body || {})});
  const data = await r.json().catch(() => ({}));
  if (!r.ok || data.error) throw new Error(data.error || r.status);
  return data;
}
const jobId = () => (VIEW.job || {}).id;
async function sendMessage(text) { return post('/api/message', {text}); }
async function approve() { return post('/api/approve', {job_id: jobId()}); }
async function answer(taskId, action) { return post('/api/callback', {job_id: jobId(), task_id: taskId, action}); }
async function reset() { return post('/api/reset'); }
async function checkin() { return post('/api/checkin', {job_id: jobId()}); }
async function checkinAnswer(taskId, ok) { return post('/api/checkin_answer', {job_id: jobId(), task_id: taskId, ok}); }
async function progress(taskId, kind) { return post('/api/progress', {job_id: jobId(), task_id: taskId, kind}); }
async function setIndustry(name) { return post('/api/industry', {name}); }

const $ = id => document.getElementById(id);
const STATUS = {planned: 'Planifikuar', sent: 'Dërguar', accepted: '✅ Pranuar', declined: '❌ Refuzuar'};
const JOB = {draft: 'Draft', awaiting_approval: 'Pret miratimin', sent: 'Dërguar', confirmed: '✅ Konfirmuar', done: '🏁 Përfunduar'};
const CHK = {asked: '⏰ check-in', ok: '👍 gati', problem: '⚠️ problem'};
let last = '';

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined) e.textContent = text;
  return e;
}

function phoneBtn(label, cls, fn) {
  const b = el('button', 'btn btn-sm ' + cls, label);
  b.onclick = async () => { b.disabled = true; try { await fn(); } catch (e) { $('msgNote').textContent = 'Dështoi: ' + e.message; } poll(); };
  return b;
}

function render(v) {
  VIEW = v;
  const job = v.job || {};
  $('checkinBtn').disabled = job.status !== 'confirmed';
  $('company').textContent = v.company || '';
  ['events', 'it_services'].forEach(n => $('ind_' + n).classList.toggle('btn-go', v.industry === n));
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
  }) : []).concat((v.tasks || []).filter(t => t.status === 'accepted').map(t => {
    const r = el('div', 'ph'); r.append(el('span', '', `${t.worker}: ${t.role}`));
    if (t.checkin === 'asked') {
      r.append(phoneBtn('👍 GATI', 'btn-go', () => checkinAnswer(t.id, true)), phoneBtn('⚠️ PROBLEM', '', () => checkinAnswer(t.id, false)));
    } else if (!t.done_at) {
      r.append(phoneBtn(t.started_at ? '✅ PËRFUNDOVA' : '🚗 E NISA', '', () => progress(t.id, t.started_at ? 'done' : 'start')));
    } else r.append(el('span', 'badge b-accepted', '✅ ' + t.done_at.slice(0, 5)));
    return r;
  })));
  if (!$('phones').children.length) $('phones').append(el('div', 'empty', 'S\'ka detyra në pritje.'));

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
      if (t.checkin) mid.append(el('div', 'bring', CHK[t.checkin] || t.checkin));
      if (t.started_at) mid.append(el('div', 'bring', '🚗 nisi ' + t.started_at.slice(0, 5) + (t.done_at ? ' · ✅ ' + t.done_at.slice(0, 5) : '')));
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
  catch (e) { $('msgNote').textContent = 'Dështoi: ' + e.message; }
  $('sendBtn').disabled = false;
};

$('resetBtn').onclick = async () => {
  try { await reset(); $('msgNote').textContent = 'U rivendos.'; } catch (e) { $('msgNote').textContent = 'Reset dështoi.'; }
  poll();
};

$('checkinBtn').onclick = async () => {
  try { await checkin(); } catch (e) { $('msgNote').textContent = 'Check-in dështoi.'; }
  poll();
};
['events', 'it_services'].forEach(n => $('ind_' + n).onclick = async () => {
  try { await setIndustry(n); last = ''; $('msgNote').textContent = n === 'events' ? 'Evente (pa PM)' : 'IT (me PM)'; } catch (e) { $('msgNote').textContent = 'Ndërrimi dështoi.'; }
  poll();
});

$('approveBtn').onclick = async () => {
  $('approveBtn').disabled = true;
  try { await approve(); } catch (e) { $('msgNote').textContent = 'Miratimi dështoi.'; }
  poll();
};

poll(); setInterval(poll, 1000);