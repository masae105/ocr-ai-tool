from ai_provider import AIProvider


class MockAIProvider(AIProvider):
    """Phase2で使用するモックAI Providerです。"""

    def analyze(self, data: dict) -> dict:
        """
        Lv3で解析されたデータ全体を受け取り、
        異常・注意点の分析結果を返します。

        Args:
            data (dict): Lv3で解析された請求書データ

        Returns:
            dict: AIによる分析結果
        """

        issues = []

        # 金額チェック
        if data.get("金額チェック") == "NG":
            issues.append(
                "明細合計と請求金額が一致していません"
            )

        # 書類タイプ確認
        if not data.get("書類タイプ"):
            issues.append(
                "書類タイプが確認できません"
            )

        if issues:
            status = "warning"
            severity = "medium"
            recommendation = "請求書の内容を確認してください"
        else:
            status = "normal"
            severity = "low"
            recommendation = "特に問題は検出されませんでした"

        return {
            "source": "mock",
            "status": status,
            "severity": severity,
            "issues": issues,
            "recommendation": recommendation,
        }