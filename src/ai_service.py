import warnings

from ai_config import get_provider_name
from ai_mock_provider import MockAIProvider
from ai_provider import AIProvider

# Step 3: from ai_openai_provider import OpenAIProvider


def _create_provider(provider_name: str) -> AIProvider:
    """設定された Provider 名に応じて AIProvider 実装を返します。"""
    if provider_name == "mock":
        return MockAIProvider()

    if provider_name == "openai":
        # Step 3 で return OpenAIProvider() に差し替え
        warnings.warn(
            (
                "AI_PROVIDER=openai ですが OpenAI Provider は未実装のため、"
                "暫定的に Mock を使用します。"
            ),
            UserWarning,
            stacklevel=2,
        )
        return MockAIProvider()

    return MockAIProvider()


class AIService:
    """AI解析処理を呼び出すサービス層です。"""

    def __init__(self):
        """設定に応じて使うAI Providerを準備します。"""
        self._provider_name = get_provider_name()
        self.provider = _create_provider(self._provider_name)

    def _build_fallback_result(self) -> dict:
        return {
            "source": self._provider_name,
            "status": "warning",
            "severity": "medium",
            "issues": [
                "AI解析を実行できませんでした。しばらくしてから再度お試しください。"
            ],
            "recommendation": "請求書の抽出結果は表示されています。内容は原本と照合してご確認ください。",
        }

    def analyze(self, data: dict) -> dict:
        """
        Lv3で解析されたデータを受け取り、
        設定されたAI Providerで解析します。

        Args:
            data (dict): Lv3で解析された請求書データ

        Returns:
            dict: AI Providerが返した解析結果
        """
        try:
            return self.provider.analyze(data)
        except Exception:
            return self._build_fallback_result()
