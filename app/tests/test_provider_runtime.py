from providers.common.runtime_context import get_provider_runtime


def test_github_runtime_uses_github_secret_namespace() -> None:
    runtime = get_provider_runtime("github")

    assert runtime.login_provider == "github"
    assert runtime.openhands.api_key_env == "OPENHANDS_API_KEY_GITHUB"
    assert runtime.openhands.secret_namespace == "github"
    assert runtime.chain_transport == "pull_request_labels"
    assert runtime.automation_id_env["qa"] == "GITHUB_OPENHANDS_QA_AUTOMATION_ID"
