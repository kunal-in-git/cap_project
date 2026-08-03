import logging
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fetch_contributors import RateLimitError, RepoNotFoundError, fetch_all, fetch_top_contributors


class FakeResponse:
    def __init__(self, status_code, json_data=None, headers=None):
        self.status_code = status_code
        self._json_data = json_data or []
        self.headers = headers or {}

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")


class FakeSession:
    """Returns one scripted response per .get() call, in order."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = 0

    def get(self, *args, **kwargs):
        self.calls += 1
        return self._responses.pop(0)


@pytest.fixture
def logger():
    log = logging.getLogger("test-pipeline")
    log.addHandler(logging.NullHandler())
    return log


def test_fetch_top_contributors_not_found_raises():
    session = FakeSession([FakeResponse(404)])

    with pytest.raises(RepoNotFoundError):
        fetch_top_contributors("owner/missing", session=session)


def test_fetch_top_contributors_rate_limited_raises():
    session = FakeSession(
        [FakeResponse(403, headers={"X-RateLimit-Remaining": "0"})]
    )

    with pytest.raises(RateLimitError):
        fetch_top_contributors("owner/repo", session=session)


def test_fetch_top_contributors_returns_top_n_sorted_by_contributions():
    session = FakeSession(
        [
            FakeResponse(
                200,
                json_data=[
                    {"login": "low", "contributions": 2},
                    {"login": "high", "contributions": 10},
                    {"login": "mid", "contributions": 5},
                ],
            )
        ]
    )

    result = fetch_top_contributors("owner/repo", top_n=2, session=session)

    assert result == [
        {"login": "high", "contributions": 10},
        {"login": "mid", "contributions": 5},
    ]


def test_fetch_all_stops_calling_api_after_rate_limit(logger, monkeypatch):
    # repo1 succeeds, repo2 hits the rate limit, repo3 should be
    # skipped WITHOUT making a 3rd network call.
    responses = [
        FakeResponse(200, json_data=[{"login": "a", "contributions": 1}]),
        FakeResponse(403, headers={"X-RateLimit-Remaining": "0"}),
    ]
    fake_session = FakeSession(responses)
    monkeypatch.setattr(
        "fetch_contributors.requests.Session", lambda: fake_session
    )

    results = fetch_all(["owner/repo1", "owner/repo2", "owner/repo3"], logger)

    assert results[0]["error"] is None
    assert results[0]["contributors"] == [{"login": "a", "contributions": 1}]
    assert "rate limit" in results[1]["error"].lower()
    assert results[2]["error"] == "Skipped: rate limit exceeded"
    assert fake_session.calls == 2  # never called a 3rd time


def test_fetch_all_records_not_found_without_stopping(logger, monkeypatch):
    responses = [
        FakeResponse(404),
        FakeResponse(200, json_data=[{"login": "b", "contributions": 3}]),
    ]
    fake_session = FakeSession(responses)
    monkeypatch.setattr(
        "fetch_contributors.requests.Session", lambda: fake_session
    )

    results = fetch_all(["owner/missing", "owner/repo2"], logger)

    assert "not found" in results[0]["error"].lower()
    assert results[1]["error"] is None
    assert results[1]["contributors"] == [{"login": "b", "contributions": 3}]
