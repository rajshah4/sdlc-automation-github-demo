"""Provider-neutral event shapes for the SDLC automation demo."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class RepositoryRef:
    name: str
    id: str | None = None
    full_name: str | None = None
    clone_url: str | None = None
    web_url: str | None = None


@dataclass
class PullRequestRef:
    id: str | int
    number: str | int | None = None
    title: str | None = None
    source_branch: str | None = None
    target_branch: str | None = None
    url: str | None = None


@dataclass
class IssueRef:
    id: str | int
    number: str | int | None = None
    title: str | None = None
    url: str | None = None
    labels: list[str] = field(default_factory=list)


@dataclass
class CommentRef:
    body: str
    id: str | int | None = None
    author: str | None = None
    url: str | None = None


@dataclass
class TriggerRef:
    name: str
    arguments: str = ""
    raw: str | None = None


@dataclass
class NormalizedEvent:
    provider: str
    event_type: str
    repository: RepositoryRef
    trigger: TriggerRef
    organization: str | None = None
    project: str | None = None
    issue: IssueRef | None = None
    pull_request: PullRequestRef | None = None
    comment: CommentRef | None = None
    raw_event: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
