# -*- coding: utf-8 -*-
"""XMPP Channel for chat and real-time messaging (SGCC Fixed Default)"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Union

from agentscope_runtime.engine.schemas.agent_schemas import (
    TextContent,
    ContentType,
)

from ....config.config import XMPPConfig
from ..base import (
    BaseChannel,
    OnReplySent,
    ProcessHandler,
    OutgoingContentPart,
)
from ..schema import ChannelType

# slixmpp 1.8.5
try:
    from slixmpp import ClientXMPP
    from slixmpp.exceptions import IqError, IqTimeout
    from slixmpp.xmlstream import ET

    HAS_SLIXMPP = True
except ImportError:
    HAS_SLIXMPP = False
    ClientXMPP = None
    IqError = None
    IqTimeout = None

logger = logging.getLogger(__name__)

# ===================== 固定默认账号配置 =====================
DEFAULT_HOST = "192.168.31.237"
DEFAULT_PORT = 11112
DEFAULT_JID = "cs017_js@node1.sgcc.com/syit"
DEFAULT_PWD = "jsepc1!"


# ==========================================================


class XMPPChannel(BaseChannel):
    channel: ChannelType = "xmpp"
    display_name = "XMPP"
    uses_manager_queue = True

    def __init__(
            self,
            process: ProcessHandler,
            enabled: bool,
            host: str = "",
            port: int = 0,
            jid: str = "",
            password: str = "",
            bot_prefix: str = "",
            on_reply_sent: OnReplySent = None,
            show_tool_details: bool = True,
            filter_tool_messages: bool = False,
            filter_thinking: bool = False,
    ):
        super().__init__(
            process,
            on_reply_sent=on_reply_sent,
            show_tool_details=show_tool_details,
            filter_tool_messages=filter_tool_messages,
            filter_thinking=filter_thinking,
        )

        self.enabled = enabled
        self.bot_prefix = bot_prefix

        # 配置为空则使用固定默认值
        self.host = host.strip() or DEFAULT_HOST
        self.port = port or DEFAULT_PORT
        self.jid = jid.strip() or DEFAULT_JID
        self.password = password.strip() or DEFAULT_PWD

        self.client: Optional[ClientXMPP] = None
        self.connected = False

    @classmethod
    def from_config(
            cls,
            process: ProcessHandler,
            config: Union[XMPPConfig, dict],
            on_reply_sent: OnReplySent = None,
            show_tool_details: bool = True,
            filter_tool_messages: bool = False,
            filter_thinking: bool = False,
    ) -> "XMPPChannel":
        if isinstance(config, dict):
            port_val = config.get("port", 0)
            port = int(port_val) if str(port_val).isdigit() else 0
            return cls(
                process=process,
                enabled=bool(config.get("enabled", False)),
                host=config.get("host", ""),
                port=port,
                jid=config.get("jid", ""),
                password=config.get("password", ""),
                bot_prefix=config.get("bot_prefix", ""),
                on_reply_sent=on_reply_sent,
                show_tool_details=show_tool_details,
                filter_tool_messages=filter_tool_messages,
                filter_thinking=filter_thinking,
            )

        return cls(
            process=process,
            enabled=config.enabled,
            host=getattr(config, "host", ""),
            port=getattr(config, "port", 0),
            jid=getattr(config, "jid", ""),
            password=getattr(config, "password", ""),
            bot_prefix=getattr(config, "bot_prefix", ""),
            on_reply_sent=on_reply_sent,
            show_tool_details=show_tool_details,
            filter_tool_messages=filter_tool_messages,
            filter_thinking=filter_thinking,
        )

    def _validate_config(self):
        if not HAS_SLIXMPP:
            raise ImportError("缺少依赖：pip install slixmpp==1.8.5")
        if not self.host:
            raise ValueError("XMPP host 不能为空")
        if not self.port:
            raise ValueError("XMPP port 不能为空")
        if not self.jid:
            raise ValueError("XMPP jid 不能为空")
        if not self.password:
            raise ValueError("XMPP password 不能为空")

        logger.info(f"【XMPP 配置信息】")
        logger.info(f"  Host: {self.host}")
        logger.info(f"  Port: {self.port}")
        logger.info(f"  JID:  {self.jid}")

    def _on_any_xml(self, xml):
        """监听所有收到的 XML 数据包，用于调试"""
        logger.info(f"【XMPP 收到原始 XML】\n{ET.tostring(xml, encoding='unicode')}")

    def _on_message(self, msg):
        try:
            logger.info(f"【XMPP 收到 message 事件】type={msg['type']} from={msg['from']} to={msg['to']}")

            if msg["type"] not in ("chat", "normal", "groupchat"):
                logger.info(f"【XMPP】忽略非聊天消息 type={msg['type']}")
                return

            sender = msg["from"].full
            content = msg["body"].strip()

            if not content:
                logger.info(f"【XMPP】消息内容为空，忽略")
                return

            logger.info(f"【XMPP 收到消息】发送方:{sender} 内容:{content}")

            content_parts = [TextContent(type=ContentType.TEXT, text=content)]
            native = {
                "channel_id": self.channel,
                "sender_id": sender,
                "content_parts": content_parts,
                "meta": {
                    "from": msg["from"].full,
                    "to": msg["to"].full,
                    "type": msg["type"],
                },
            }
            if self._enqueue:
                self._enqueue(native)
                logger.info(f"【XMPP】消息已入队")
            else:
                logger.warning(f"【XMPP】_enqueue 未设置，消息丢弃")
        except Exception as e:
            logger.error(f"【XMPP】接收消息异常: {e}", exc_info=True)

    def _on_connected(self, event):
        logger.info("【XMPP】TCP 连接已建立")

    def _on_disconnected(self, event):
        logger.warning("【XMPP】连接已断开")
        self.connected = False

    def _on_failed_auth(self, event):
        logger.error("【XMPP】认证失败！请检查 JID 和密码")

    async def _session_start(self, event):
        if not self.client:
            return

        logger.info("【XMPP】Session 开始，正在发送在线状态...")
        try:
            self.client.send_presence()
            logger.info("【XMPP】正在获取联系人列表...")
            await self.client.get_roster()
        except (IqError, IqTimeout) as e:
            logger.warning(f"【XMPP】获取联系人列表失败（不影响使用）: {e}")

        self.connected = True
        logger.info(f"✅【XMPP 完全登录成功】JID:{self.jid} 服务器:{self.host}:{self.port}")

    async def start(self) -> None:
        if not self.enabled:
            logger.info("【XMPP】渠道未启用，跳过启动")
            return
        try:
            self._validate_config()
        except Exception as e:
            logger.error(f"【XMPP】配置校验失败: {e}")
            return

        logger.info(f"【XMPP】开始初始化客户端...")
        self.client = ClientXMPP(self.jid, self.password)

        # 注册所有事件监听器
        self.client.add_event_handler("connected", self._on_connected)
        self.client.add_event_handler("disconnected", self._on_disconnected)
        self.client.add_event_handler("failed_auth", self._on_failed_auth)
        self.client.add_event_handler("session_start", self._session_start)
        self.client.add_event_handler("message", self._on_message)

        # ✅ 关键：监听所有原始 XML 数据包
        self.client.add_event_handler("stanza", self._on_any_xml)

        try:
            logger.info(f"【XMPP】正在连接 {self.host}:{self.port}...")
            self.client.connect(
                address=(self.host, self.port),
                use_ssl=False
            )
            logger.info("【XMPP】connect() 调用完成，等待服务器响应...")
        except Exception as e:
            logger.error(f"【XMPP】连接失败: {e}", exc_info=True)
            return

    async def stop(self) -> None:
        logger.info("【XMPP】正在断开连接")
        self.connected = False
        if self.client:
            try:
                self.client.disconnect()
            except Exception:
                pass
        logger.info("【XMPP】已停止")

    async def send(
            self,
            to_handle: str,
            text: str,
            meta: Optional[dict] = None,
    ) -> None:
        if not self.enabled or not self.connected or not self.client:
            return
        try:
            target = to_handle
            self.client.send_message(mto=target, mbody=text, mtype="chat")
            logger.info(f"【XMPP 发送消息】目标:{target} 内容:{text}")
        except Exception as e:
            logger.error(f"【XMPP】发送消息失败: {e}")

    def resolve_session_id(self, sender_id: str, channel_meta: Optional[dict] = None) -> str:
        return f"xmpp:{sender_id}"

    def get_to_handle_from_request(self, request: Any) -> str:
        meta = getattr(request, "channel_meta", None) or {}
        sender = meta.get("from", "")
        if sender:
            return sender
        sid = getattr(request, "session_id", "")
        if sid.startswith("xmpp:"):
            return sid.split(":", 1)[-1]
        return ""

    def build_agent_request_from_native(self, native_payload: Any) -> Any:
        payload = native_payload or {}
        return self.build_agent_request_from_user_content(
            channel_id=self.channel,
            sender_id=payload.get("sender_id", "unknown"),
            session_id=self.resolve_session_id(payload.get("sender_id", "")),
            content_parts=payload.get("content_parts", []),
            channel_meta=payload.get("meta", {}),
        )