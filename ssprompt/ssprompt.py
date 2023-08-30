from __future__ import annotations

from typing import TYPE_CHECKING,Any
import os
class Ssprompt:
    
    def __init__(self) -> None:

        """获取GitHub access key 不使用access key访问，
        每小时只能访问60次github，配置后可以访问5000次/小时"""
        self._github_access_key =  os.environ.get('GITHUB_ACCESS_KEY', "")

        """
        访问github等失败尝试次数
        """
        self._max_retries = 3

        """
        访问github等失败尝试延迟时间(ms)
        """
        self._retry_delay = 200

    @property
    def github_access_key(self) -> str:
        return self._github_access_key
    
    @property
    def max_retries(self)->int:
        return self._max_retries
    
    @property
    def retry_delay(self)->int:
        return self._retry_delay
    