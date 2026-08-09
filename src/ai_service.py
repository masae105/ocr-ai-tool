from ai_config import get_provider_name
from ai_mock_provider import MockAIProvider


class AIService:
    """AI解析処理を呼び出すサービス層です。"""

    def __init__(self):
        """設定に応じて使うAI Providerを準備します。"""
        provider_name = get_provider_name()

        if provider_name == "mock":
            self.provider = MockAIProvider()
        else:
            # 将来 OpenAI を追加するための分岐です。
            self.provider = MockAIProvider()

    def analyze(self, data: dict) -> dict:
        """
        Lv3で解析されたデータを受け取り、
        設定されたAI Providerで解析します。

        Args:
            data (dict): Lv3で解析された請求書データ

        Returns:
            dict: AI Providerが返した解析結果
        """
        return self.provider.analyze(data)