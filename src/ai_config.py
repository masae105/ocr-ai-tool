# AI Providerの選択を管理する設定ファイルです。

import os
import warnings
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_PROVIDER = "mock"

SUPPORTED_PROVIDERS = {
    "mock": "mock",
    "openai": "openai",
}

_ALLOWED_PROVIDER_NAMES = frozenset(SUPPORTED_PROVIDERS.keys())

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_dotenv_loaded = False


def _load_dotenv_once() -> None:
    """ローカル開発用に .env を1回だけ読み込みます。"""
    global _dotenv_loaded
    if _dotenv_loaded:
        return
    load_dotenv(_PROJECT_ROOT / ".env")
    _dotenv_loaded = True


def _normalize_provider_name(raw: str | None) -> str | None:
    """Provider名を正規化します。空文字の場合は None を返します。"""
    if raw is None:
        return None
    normalized = raw.strip().lower()
    if not normalized:
        return None
    return normalized


def get_provider_name() -> str:
    """環境変数 AI_PROVIDER から使用する AI Provider 名を返します。"""
    _load_dotenv_once()

    raw = os.environ.get("AI_PROVIDER")
    provider = _normalize_provider_name(raw)

    if provider is None:
        return DEFAULT_PROVIDER

    if provider in _ALLOWED_PROVIDER_NAMES:
        return provider

    warnings.warn(
        (
            f"AI_PROVIDER の値が不正です（許可: mock, openai）。"
            f'"{DEFAULT_PROVIDER}" を使用します。'
        ),
        UserWarning,
        stacklevel=2,
    )
    return DEFAULT_PROVIDER


def get_openai_api_key() -> str | None:
    """
    環境変数 OPENAI_API_KEY を返します。
    未設定または空の場合は None です。キーの値はログ出力しません。
    """
    _load_dotenv_once()

    raw = os.environ.get("OPENAI_API_KEY")
    if raw is None:
        return None
    key = raw.strip()
    return key or None
