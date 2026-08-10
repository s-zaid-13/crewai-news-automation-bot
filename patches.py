"""
Temporary compatibility patch for CrewAI issue #5886:
https://github.com/crewAIInc/crewAI/issues/5886

CrewAI tags every outgoing message with `cache_breakpoint: true` (a flag meant
for Anthropic's prompt-caching API) but only strips it back out for the
Anthropic provider. Non-Anthropic providers like Groq receive the flag as-is
and reject the request outright.

This patch neutralizes the tagging step so messages reach Groq clean.
Remove this file once CrewAI merges an upstream fix (tracked in #5887 / #5914).
"""

import crewai.llms.cache as _crewai_cache

_crewai_cache.mark_cache_breakpoint = lambda msg: msg
