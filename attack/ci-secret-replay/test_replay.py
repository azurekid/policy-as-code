import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import mock_cloud
import replay


class ScrapeTests(unittest.TestCase):
    def test_full_chain_against_loopback_services(self):
        with mock_cloud.start_mock_services() as (base, received):
            events = replay.replay(token_url=base, sink_url=base)
        scraped = events[:-1]
        self.assertEqual([e["source"] for e in scraped], [
            "env-file:service-principal.env",
            "cred-file:azure-credentials.json",
            "toJSON(secrets):WF_SECRETS",
        ])
        self.assertTrue(all(e["use"]["authenticated"] for e in scraped))
        self.assertTrue(all(e["use"]["mode"] == "loopback" for e in scraped))
        self.assertTrue(all(e["exfil"]["delivered"] for e in scraped))
        self.assertEqual(events[-1]["event"], "metadata-only")
        self.assertFalse(events[-1]["authenticated"])
        # Secrets never appear in emitted events.
        self.assertNotIn(replay.FAKE_SECRET, json.dumps(events))
        self.assertTrue(all(e["secret"] == "[REDACTED]" for e in scraped))
        # Loopback sink saw three gzip exfil deliveries carrying the campaign token.
        self.assertEqual(len(received), 3)
        self.assertTrue(all(r["encoding"] == "gzip" for r in received))
        self.assertTrue(all(r["ctoken"] == replay.WF_CTOKEN for r in received))

    def test_scrape_secrets_dump_extracts_azure_and_lists_other_names(self):
        dump = replay.scrape_secrets_dump(replay.read_fixture("secrets-dump.json"))
        self.assertEqual(dump["azure"], replay.EXPECTED)
        self.assertEqual(dump["other_secret_names"], ["GITHUB_TOKEN", "NPM_TOKEN"])

    def test_scrape_secrets_dump_rejects_non_flat_object(self):
        for text in ('["AZURE_CLIENT_ID"]', '{"AZURE_CREDENTIALS": {"a": 1}}'):
            with self.assertRaises(ValueError):
                replay.scrape_secrets_dump(text)

    def test_refuses_real_looking_or_incomplete_credentials(self):
        for credentials in (
            {**replay.EXPECTED, "clientSecret": "different-test-value"},
            {"clientId": replay.EXPECTED["clientId"]},
        ):
            with self.subTest(credentials=list(credentials)):
                with self.assertRaisesRegex(ValueError, "non-synthetic"):
                    replay.use_credentials(credentials)

    def test_simulation_mode_when_no_endpoint(self):
        result = replay.use_credentials(replay.EXPECTED)
        self.assertEqual(result["mode"], "simulation")
        self.assertTrue(result["authenticated"])

    def test_use_and_exfil_refuse_non_loopback_destinations(self):
        with self.assertRaisesRegex(ValueError, "non-loopback"):
            replay.use_credentials(replay.EXPECTED, token_url="http://10.0.0.1:8080")
        with self.assertRaisesRegex(ValueError, "non-loopback"):
            replay.exfiltrate({"azure": replay.EXPECTED}, sink_url="http://10.0.0.1:8080")

    def test_env_rejects_duplicate_and_unrecognized_fields(self):
        for text in (
            "AZURE_CLIENT_ID=x\nAZURE_CLIENT_ID=y",
            "UNRELATED_SECRET=x",
            "not-an-assignment",
        ):
            with self.assertRaises(ValueError):
                replay.parse_env(text)

    def test_refuses_symlink_and_oversized_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root / "outside"
            outside.write_text("not a fixture")
            fixtures = root / "fixtures"
            fixtures.mkdir()
            file = fixtures / "azure-credentials.json"
            file.symlink_to(outside)
            with patch.object(replay, "FIXTURES", fixtures):
                with self.assertRaises(ValueError):
                    replay.read_fixture(file.name)
                file.unlink()
                file.write_text("x" * 16385)
                with self.assertRaises(ValueError):
                    replay.read_fixture(file.name)
            file.unlink()
            fixtures.rmdir()
            fixtures.symlink_to(root, target_is_directory=True)
            with patch.object(replay, "FIXTURES", fixtures):
                with self.assertRaises(ValueError):
                    replay.read_fixture("outside")


if __name__ == "__main__":
    unittest.main()
