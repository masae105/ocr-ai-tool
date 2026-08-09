# AI Providerの選択を管理する設定ファイルです。

# 現在はモック実装を使います。
DEFAULT_PROVIDER = "mock"

# 将来 OpenAIへ切り替えるときは、ここを "openai" に変更できます。
SUPPORTED_PROVIDERS = {
    "mock": "mock",
    "openai": "openai",
}


def get_provider_name() -> str:
    """現在使用するAI Provider名を返します。"""
    return DEFAULT_PROVIDER
