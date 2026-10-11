# SPDX-License-Identifier: Apache-2.0
"""Yusuke six-day public-state Fieldbook (Python port). Live 56028043 PENDING.

Windows-runnable later-block reselect at 144/288/432/576. Does not load
agent.so and is not a 227/242/266 sheep wrap of Fieldbook BALANCED.
"""

from __future__ import annotations

from sixday_logic import make_agent

agent = make_agent()
main = agent
