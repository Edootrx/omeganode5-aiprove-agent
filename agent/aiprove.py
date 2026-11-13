#!/usr/bin/env python3
"""AIProve agent client — REST only, per https://aiprove.fun/skill.md

Identity = dedicated EVM keypair in wallet.key (mode 600, never printed).
Auth = EIP-191 challenge -> sign -> Bearer session token.
Referral attribution = POST /api/me/referral/claim {code} once after first
auth (mirrors the browser client in assets/js/api.js lines 228-233).
No on-chain transactions, no funds: open-beta entries are free and the
escrow contracts are not deployed yet (skill.md endpoint reference).
"""
import json, os, sys, time
import requests
from eth_account import Account
from eth_account.messages import encode_defunct

BASE = os.environ.get("API_BASE_URL", "https://aiprove.fun")
HERE = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = os.path.join(HERE, "wallet.key")
STATE_FILE = os.path.join(HERE, "state.json")
HANDLE = "OmegaNode5"  # server-assigned profile handle (verified via /api/me)
REF_CODE = "7760fc34"  # referral link the user gave: aiprove.fun/r/7760fc34

def load_wallet():
    if not os.path.exists(KEY_FILE):
        acct = Account.create()
        with open(KEY_FILE, "w") as f:
            f.write(acct.key.hex())
        os.chmod(KEY_FILE, 0o600)
    with open(KEY_FILE) as f:
        return Account.from_key(f.read().strip())

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}

def save_state(s):
    with open(STATE_FILE, "w") as f:
        json.dump(s, f, indent=1)
    os.chmod(STATE_FILE, 0o600)

class Client:
    def __init__(self):
        self.acct = load_wallet()
        self.state = load_state()
        self.token = None

    def auth(self, force=False):
        now_ms = int(time.time() * 1000)
        if (not force and self.state.get("token")
                and self.state.get("token_addr") == self.acct.address.lower()
                and self.state.get("expiresAt", 0) > now_ms + 60_000):
            self.token = self.state["token"]
            return self.token
        r = requests.get(f"{BASE}/api/auth/challenge",
                         params={"address": self.acct.address}, timeout=90)
        r.raise_for_status()
        challenge = r.json()["challenge"]
        sig = self.acct.sign_message(encode_defunct(text=challenge)).signature.hex()
        if not sig.startswith("0x"):
            sig = "0x" + sig
        r = requests.post(f"{BASE}/api/auth/verify",
                          json={"address": self.acct.address, "signature": sig},
                          timeout=90)
        r.raise_for_status()
        body = r.json()
        self.token = body["token"]
        self.state.update({"token": self.token,
                           "token_addr": self.acct.address.lower(),
                           "expiresAt": body.get("expiresAt", 0),
                           "address": self.acct.address})
        save_state(self.state)
        return self.token

    def _h(self):
        return {"Authorization": f"Bearer {self.token}", "content-type": "application/json"}

    def get(self, path, auth=False, **kw):
        r = requests.get(f"{BASE}{path}", headers=self._h() if auth else {}, timeout=90, **kw)
        return r

    def post(self, path, body):
        return requests.post(f"{BASE}{path}", headers=self._h(), json=body, timeout=90)

    def claim_referral(self, code=REF_CODE):
        if self.state.get("referral_claimed") == code:
            return {"skipped": "already claimed in state"}
        r = self.post("/api/me/referral/claim", {"code": code})
        out = {"status": r.status_code, "body": r.text[:500]}
        if r.ok:
            self.state["referral_claimed"] = code
            save_state(self.state)
        return out

    def me(self):
        r = self.get("/api/me", auth=True)
        r.raise_for_status()
        return r.json()

    def my_submissions(self):
        r = self.get("/api/me/submissions", auth=True)
        r.raise_for_status()
        return r.json()

    def bounties(self, status="open"):
        r = requests.get(f"{BASE}/api/bounties", params={"status": status}, timeout=90)
        r.raise_for_status()
        return r.json()["bounties"]

    def enter(self, slug):
        r = self.post(f"/api/bounties/{slug}/enter", {"handle": HANDLE})
        return r.status_code, r.text[:300]

    def submit_prediction(self, slug, prediction):
        r = self.post(f"/api/bounties/{slug}/submit",
                      {"prediction": prediction, "handle": HANDLE})
        return r.status_code, r.text[:500]

    def submit_link(self, slug, link, note=""):
        r = self.post(f"/api/bounties/{slug}/submit",
                      {"link": link, "note": note, "handle": HANDLE})
        return r.status_code, r.text[:500]

if __name__ == "__main__":
    c = Client()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "address":
        print(c.acct.address)
    elif cmd == "auth":
        c.auth()
        print(json.dumps(c.me(), indent=1)[:2000])
    elif cmd == "bounties":
        for b in c.bounties():
            print(b["slug"], "|", b["submitKind"] if "submitKind" in b else b.get("lane"), "|", b["amt"], b["unit"], "| closes", b["closes"])
    else:
        c.auth()
        print(json.dumps(c.me(), indent=1)[:3000])
