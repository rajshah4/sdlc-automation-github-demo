"""Provider runtime configuration for OpenHands automation identities."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


MANIFEST_PATH = Path(__file__).resolve().parents[1] / "runtime-manifest.json"


@dataclass(frozen=True)
class OpenHandsRuntime:
    host_env: str
    api_key_env: str
    secret_namespace: str
    automation_namespace: str


@dataclass(frozen=True)
class ProviderRuntime:
    provider: str
    login_provider: str
    display_name: str
    openhands: OpenHandsRuntime
    provider_credentials: dict[str, str]
    chain_transport: str
    automation_id_env: dict[str, str]
    fallback_transport: str | None = None

    @property
    def required_env_names(self) -> set[str]:
        names = {
            self.openhands.host_env,
            self.openhands.api_key_env,
            self.provider_credentials["primary_token_env"],
        }
        return names | set(self.automation_id_env.values())


def load_runtime_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def get_provider_runtime(provider: str, path: Path = MANIFEST_PATH) -> ProviderRuntime:
    manifest = load_runtime_manifest(path)
    config = manifest["providers"][provider]
    openhands = OpenHandsRuntime(**config["openhands"])

    return ProviderRuntime(
        provider=provider,
        login_provider=config["login_provider"],
        display_name=config["display_name"],
        openhands=openhands,
        provider_credentials=dict(config["provider_credentials"]),
        chain_transport=config["chain_transport"],
        fallback_transport=config.get("fallback_transport"),
        automation_id_env=dict(config["automation_id_env"]),
    )
