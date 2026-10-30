import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


TRACKER_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TRACKER_ROOT))

import track_and_notify


class MinimumStarFilterTests(unittest.TestCase):
    def test_includes_repositories_at_or_above_minimum(self):
        self.assertTrue(track_and_notify.passes_minimum_star_filter("owner/repo", 50, 50))
        self.assertTrue(track_and_notify.passes_minimum_star_filter("owner/repo", 51, 50))

    def test_excludes_new_repositories_below_minimum(self):
        self.assertFalse(track_and_notify.passes_minimum_star_filter("owner/repo", 49, 50))

    def test_explicit_and_previously_tracked_repositories_bypass_minimum(self):
        exempt = {"owner/pinned", "owner/previously-tracked"}
        self.assertTrue(track_and_notify.passes_minimum_star_filter("owner/pinned", 1, 50, exempt))
        self.assertTrue(track_and_notify.passes_minimum_star_filter("owner/previously-tracked", 1, 50, exempt))

    def test_loads_minimum_stars_and_preserves_legacy_watchlist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            seed_path = Path(temp_dir) / "watchlist_seed.json"
            seed_path.write_text(json.dumps({
                "always_track": ["owner/pinned"],
                "topics_of_interest": ["python"],
                "minimum_stars": 75,
            }))
            with patch.object(track_and_notify, "WATCHLIST_SEED", str(seed_path)):
                self.assertEqual(
                    track_and_notify.load_watchlist_seed(),
                    ({"owner/pinned"}, ["python"], 75),
                )

            seed_path.write_text(json.dumps(["owner/legacy"]))
            with patch.object(track_and_notify, "WATCHLIST_SEED", str(seed_path)):
                self.assertEqual(
                    track_and_notify.load_watchlist_seed(),
                    ({"owner/legacy"}, [], 0),
                )

    def test_invalid_minimum_stars_logs_issue_and_disables_filter(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            seed_path = Path(temp_dir) / "watchlist_seed.json"
            seed_path.write_text(json.dumps({"minimum_stars": -1}))
            with (
                patch.object(track_and_notify, "WATCHLIST_SEED", str(seed_path)),
                patch.object(track_and_notify, "RUN_ERRORS", []),
            ):
                self.assertEqual(track_and_notify.load_watchlist_seed(), (set(), [], 0))
                self.assertEqual(len(track_and_notify.RUN_ERRORS), 1)

    def test_llm_reason_skips_external_call_without_api_key(self):
        with (
            patch.dict(track_and_notify.os.environ, {"GROQ_API_KEY_FOR_AUTO_EMAIL": ""}),
            patch.object(track_and_notify.requests, "post") as post,
        ):
            result = track_and_notify.llm_reason(
                {"owner/repo": {"velocity": 10, "phase": "Breakout"}},
                {},
                {},
            )

        self.assertEqual(result, {})
        post.assert_not_called()

    def test_send_email_requires_both_configuration_values(self):
        with (
            patch.dict(
                track_and_notify.os.environ,
                {"RESEND_API_KEY": "", "MY_EMAIL": ""},
            ),
            self.assertRaises(RuntimeError),
        ):
            track_and_notify.send_email("<p>test</p>")

    def test_snapshot_skips_only_below_minimum_non_exempt_repositories(self):
        stats = {
            "owner/below": {"stars": 49, "description": "below"},
            "owner/at": {"stars": 50, "description": "at threshold"},
            "owner/pinned": {"stars": 1, "description": "pinned"},
            "owner/previously-tracked": {"stars": 1, "description": "tracked"},
        }
        for value in stats.values():
            value.update({
                "forks": 0,
                "open_issues": 0,
                "created_at": "2025-01-01T00:00:00Z",
                "pushed_at": "2025-01-01T00:00:00Z",
            })

        with tempfile.TemporaryDirectory() as temp_dir:
            snapshots_path = str(Path(temp_dir) / "snapshots.csv")
            with (
                patch.object(track_and_notify, "SNAPSHOTS_CSV", snapshots_path),
                patch.object(track_and_notify, "get_repo_stats", side_effect=lambda name: stats[name]),
                patch.object(track_and_notify, "get_top_contributors", return_value=[]),
                patch.object(track_and_notify.time, "sleep"),
            ):
                track_and_notify.snapshot_all(
                    [
                        "owner/below",
                        "owner/at",
                        "owner/pinned",
                        "owner/previously-tracked",
                    ],
                    minimum_stars=50,
                    exempt_repos={"owner/pinned", "owner/previously-tracked"},
                )
                history = track_and_notify.load_history()

        self.assertEqual(
            set(history),
            {"owner/at", "owner/pinned", "owner/previously-tracked"},
        )


if __name__ == "__main__":
    unittest.main()
