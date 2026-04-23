# -*- coding: utf-8 -*-
from __future__ import annotations
import logging
from typing import Any

logger = logging.getLogger(__name__)

# 关键：用相对导入
from ..app.channels.base import BaseChannel
from ..app.channels.schema import ChannelType


class XMPPChannel(BaseChannel):
    channel: ChannelType = "xmpp"
    display_name = "XMPP"
    uses_manager_queue = True

    def __init__(
        self,
        process,
        enabled=False,
        host="",
        port=5222,
        jid="",
        password="",
        room="",
        room_nick="",
        bot_prefix="",
        **kwargs,
    ):
        super().__init__(process, **kwargs)
        self.enabled = enabled
        self.bot_prefix = bot_prefix
        self.host = host
        self.port = port
        self.jid = jid
        self.password = password
        self.room = room
        self.room_nick = room_nick

    @classmethod
    def get_default_config(cls):
        return {
            "enabled": False,
            "bot_prefix": "",
            "host": "",
            "port": 5222,
            "jid": "",
            "password": "",
            "room": "",
            "room_nick": "",
        }

    @classmethod
    def from_config(cls, process, config, **kwargs):
        return cls(
            process=process,
            enabled=config.get("enabled", False),
            host=config.get("host", ""),
            port=config.get("port", 5222),
            jid=config.get("jid", ""),
            password=config.get("password", ""),
            room=config.get("room", ""),
            room_nick=config.get("room_nick", ""),
            bot_prefix=config.get("bot_prefix", ""),
            **kwargs,
        )

    async def start(self):
        if self.enabled:
            logger.info("✅ XMPP 渠道启动成功")

    async def stop(self):
        logger.info("🛑 XMPP 渠道已停止")

    async def send(self, to_handle, text, meta=None):
        logger.info(f"[XMPP] 发送到 {to_handle}: {text}")

    def build_agent_request_from_native(self, native_payload):
        payload = native_payload or {}
        return self.build_agent_request_from_user_content(
            channel_id=self.channel,
            sender_id=payload.get("sender_id", "unknown"),
            session_id=f"xmpp:{payload.get('sender_id', 'unknown')}",
            content_parts=[{"type": "text", "text": payload.get("text", "")}],
            channel_meta=payload.get("meta", {}),
        )