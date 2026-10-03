# -*- coding: utf-8 -*-
"""
Telegram channel. Started by src/server.py when TELEGRAM_BOT_TOKEN is set.

.env:
  TELEGRAM_BOT_TOKEN=123:abc                 from @BotFather
  TELEGRAM_IDENTITY_MAP=111:leader,222:w_erioni,333:w_leart,444:w_arta
      chat_id -> "leader" or a worker id from company.json. Identity comes from this map, never from text.
      Unknown chats that send /start get their chat_id back (to fill in the map).

Leader chat: messages go to the AI Team Leader; plans arrive with a [✅ MIRATO] button.
Worker chats: detailed tasks arrive with [✅ ACCEPT] [❌ S'MUNDEM].
"""
from __future__ import annotations

import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests

from .. import runtime as R
from .. import state as S

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
API = f"https://api.telegram.org/bot{TOKEN}"
POOL = ThreadPoolExecutor(max_workers=4)


def _imap() -> dict[str, str]:
    out = {}
    for pair in filter(None, (p.strip() for p in os.getenv("TELEGRAM_IDENTITY_MAP", "").split(","))):
        chat, _, who = pair.partition(":")
        out[chat.strip()] = who.strip()
    return out


def tg(method: str, **params) -> dict:
    try:
        r = requests.post(f"{API}/{method}", json=params, timeout=40)
        data = r.json()
    except Exception as e:  # noqa: BLE001
        print(f"  ! telegram {method}: {e}")
        return {"ok": False}
    if not data.get("ok"):
        print(f"  ! telegram {method}: {data}")
    return data


class Notifier:
    def __init__(self) -> None:
        self.imap = _imap()
        self.by_who = {who: chat for chat, who in self.imap.items()}
        self.leader_history: list = []

    def send_task(self, worker_id: str, job_id: str, task_id: str, text: str) -> bool:
        chat = self.by_who.get(worker_id)
        if not chat:
            return False
        kb = {"inline_keyboard": [[{"text": "✅ ACCEPT", "callback_data": f"a:{job_id}:{task_id}"},
                                   {"text": "❌ S'MUNDEM", "callback_data": f"d:{job_id}:{task_id}"}]]}
        return bool(tg("sendMessage", chat_id=chat, text=text, reply_markup=kb).get("ok"))

    def send_checkin(self, worker_id: str, job_id: str, task_id: str, text: str) -> bool:
        chat = self.by_who.get(worker_id)
        if not chat:
            return False
        kb = {"inline_keyboard": [[{"text": "👍 PO, JAM GATI", "callback_data": f"c:{job_id}:{task_id}"},
                                   {"text": "⚠️ KAM PROBLEM", "callback_data": f"p:{job_id}:{task_id}"}]]}
        return bool(tg("sendMessage", chat_id=chat, text=text, reply_markup=kb).get("ok"))

    def send_progress(self, worker_id: str, job_id: str, task_id: str, role: str) -> bool:
        chat = self.by_who.get(worker_id)
        if not chat:
            return False
        kb = {"inline_keyboard": [[{"text": "🚗 E NISA", "callback_data": f"s:{job_id}:{task_id}"},
                                   {"text": "✅ PËRFUNDOVA", "callback_data": f"f:{job_id}:{task_id}"}]]}
        return bool(tg("sendMessage", chat_id=chat, text=f"Gjatë punës '{role}': shtyp kur e nis dhe kur e përfundon.",
                       reply_markup=kb).get("ok"))

    def send_leader(self, text: str) -> None:
        chat = self.by_who.get("leader")
        if chat:
            tg("sendMessage", chat_id=chat, text=text)

    def ask_approval(self, job_id: str, summary: str) -> None:
        chat = self.by_who.get("leader")
        if chat:
            kb = {"inline_keyboard": [[{"text": "✅ MIRATO", "callback_data": f"ok:{job_id}"}]]}
            tg("sendMessage", chat_id=chat, text=f"📋 Plani {job_id}\n{summary}", reply_markup=kb)


def _on_message(n: Notifier, msg: dict) -> None:
    chat = str(msg["chat"]["id"])
    text = (msg.get("text") or "").strip()
    who = n.imap.get(chat)
    if text.startswith("/start") or not who:
        tg("sendMessage", chat_id=chat, text=f"Përshëndetje! chat_id: {chat}\n" +
           (f"Je lidhur si: {who}" if who else "Ky chat ende s'është i lidhur me ekipin."))
        first = (msg.get("from") or {}).get("first_name", "")
        print(f"   /start from chat_id {chat} ({who or 'unmapped'}) {first}", flush=True)
        with open(S.EVENTS_FILE.parent / "telegram_starts.txt", "a", encoding="utf-8") as f:
            f.write(f"{chat} | {first} | {who or 'unmapped'}\n")
        return
    if who == "leader":
        from ..agent.loop import run
        tg("sendChatAction", chat_id=chat, action="typing")
        res = run(text, history=n.leader_history[-12:])
        n.leader_history = res.get("history") or n.leader_history
        tg("sendMessage", chat_id=chat, text=res["reply_text"])
    else:
        tg("sendMessage", chat_id=chat, text="Faleminderit. Për detyrat përdor butonat ACCEPT / S'MUNDEM. Për çdo gjë tjetër, shkruaji liderit.")


def _on_callback(n: Notifier, cq: dict) -> None:
    tg("answerCallbackQuery", callback_query_id=cq["id"])  # answer first, always
    chat = str(cq["message"]["chat"]["id"])
    who = n.imap.get(chat)
    parts = (cq.get("data") or "").split(":")
    mid = cq["message"]["message_id"]
    original = cq["message"].get("text", "")
    if parts[0] == "ok" and who == "leader":
        res = R.approve(parts[1], by="Telegram")
        tg("editMessageText", chat_id=chat, message_id=mid,
           text=original + ("\n\n✅ U miratua — detyrat u dërguan." if "error" not in res else f"\n\n⚠️ {res['error']}"))
        return
    if parts[0] in ("s", "f") and len(parts) == 3 and who and who != "leader":
        res = R.progress(parts[1], parts[2], who, "start" if parts[0] == "s" else "done")
        tg("sendMessage", chat_id=chat, text=("ℹ️ Kjo detyrë s'është më aktive." if res.get("stale") else
                                             f"Regjistruar: {'nisja' if parts[0] == 's' else 'përfundimi'} në {res['at'][:5]}."))
        return
    if parts[0] in ("c", "p") and len(parts) == 3 and who and who != "leader":
        res = R.checkin_answer(parts[1], parts[2], who, ok=parts[0] == "c")
        if res.get("stale"):
            stamp = "\n\nℹ️ Kjo detyrë s'është më aktive."
        elif parts[0] == "c":
            stamp = "\n\n👍 Faleminderit, suksese!"
        else:
            stamp = "\n\n⚠️ U njoftua lideri. Detyra i kalon dikujt tjetër."
        tg("editMessageText", chat_id=chat, message_id=mid, text=original + stamp)
        return
    if parts[0] in ("a", "d") and len(parts) == 3 and who and who != "leader":
        res = R.respond(parts[1], parts[2], who, accept=parts[0] == "a")
        if res.get("stale"):
            stamp = "\n\nℹ️ Kjo detyrë s'është më aktive."
        elif res.get("status") == "accepted":
            stamp = "\n\n✅ E pranove. Faleminderit!"
        else:
            stamp = "\n\n❌ U regjistrua. Detyra i kalon dikujt tjetër."
        tg("editMessageText", chat_id=chat, message_id=mid, text=original + stamp)


def _loop(n: Notifier) -> None:
    offset = None
    while True:
        try:
            upd = tg("getUpdates", offset=offset, timeout=25, allowed_updates=["message", "callback_query"])
            for u in upd.get("result", []):
                offset = u["update_id"] + 1
                if "callback_query" in u:
                    POOL.submit(_on_callback, n, u["callback_query"])
                elif u.get("message", {}).get("text"):
                    POOL.submit(_on_message, n, u["message"])
        except Exception as e:  # noqa: BLE001
            print(f"  ! telegram loop: {e}")
            time.sleep(3)


def start() -> bool:
    if not TOKEN:
        print("Telegram: off (no TELEGRAM_BOT_TOKEN). Use the UI panel for approve / accept.")
        return False
    me = tg("getMe")
    if not me.get("ok"):
        print("Telegram: token rejected.")
        return False
    n = Notifier()
    R.notifier = n
    threading.Thread(target=_loop, args=(n,), daemon=True).start()
    print(f"Telegram: @{me['result']['username']} live · mapped chats: {len(n.imap)}")
    S.log("system", f"Telegram @{me['result']['username']} është lidhur ({len(n.imap)} chat-e).")
    return True
