class AIProvider:
    """AI解析の共通インターフェースです。"""

    def analyze(self, data: dict) -> dict:
        """
        Lv3で解析されたデータを受け取り、
        AI解析結果を辞書で返します。

        Args:
            data (dict): Lv3で解析された請求書データ

        Returns:
            dict: AIによる解析結果
        """
        raise NotImplementedError("サブクラスで実装してください")