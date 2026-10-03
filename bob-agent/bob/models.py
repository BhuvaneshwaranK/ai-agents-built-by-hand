"""Ways to talk to a language model.

Every model in this file has the same method:

    reply = model.chat(messages, tools)

That shared shape is the whole trick. The agent loop does not care
which model it talks to, so you can learn with the free, offline
PracticeModel and later switch to a real model by changing one line.
"""

import json
import os
import re
import urllib.error
import urllib.request


class ModelError(Exception):
    """Raised when a model cannot give us a usable reply."""


# ---------------------------------------------------------------------
# Helpers for writing practice scripts
# ---------------------------------------------------------------------

def say(text):
    """A scripted reply where the model simply answers in words."""
    return {"role": "assistant", "content": text}


def call_tool(name, **arguments):
    """A scripted reply where the model asks us to run one tool."""
    return {
        "role": "assistant",
        "content": None,
        "tool_calls": [
            {
                "id": "call_" + name,
                "type": "function",
                "function": {
                    "name": name,
                    "arguments": json.dumps(arguments),
                },
            }
        ],
    }


# ---------------------------------------------------------------------
# The practice model: free, offline, and predictable
# ---------------------------------------------------------------------

class PracticeModel:
    """A pretend model that plays back replies you wrote in advance.

    It does not understand anything. It exists so you can watch the
    agent loop work, step by step, without an internet connection,
    an account, or any cost. Because the replies are fixed, the
    output is the same every time, which also makes testing easy.
    """

    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = 0

    def chat(self, messages, tools=None):
        self.calls += 1
        if not self.replies:
            raise ModelError(
                "The practice script has run out of replies.")
        return self.replies.pop(0)


# ---------------------------------------------------------------------
# A real model, reached over HTTP
# ---------------------------------------------------------------------

class ChatModel:
    """Talks to any server that speaks the OpenAI-compatible
    Chat Completions format.

    Local example (free, runs on your own computer with Ollama):
        ChatModel("qwen3:4b")

    Cloud example (needs an account and may cost money):
        ChatModel("model-name", base_url="https://provider.example/v1",
                  api_key_env="PROVIDER_API_KEY")

    The API key is read from an environment variable, never typed
    into the code, so it cannot leak if you share your files.
    """

    def __init__(self, model, base_url="http://localhost:11434/v1",
                 api_key_env=None, timeout=120, temperature=None):
        self.model = model
        self.temperature = temperature
        self.base_url = base_url.rstrip("/")
        self.api_key_env = api_key_env
        self.timeout = timeout
        self.calls = 0
        self.tokens_used = 0

    def chat(self, messages, tools=None):
        self.calls += 1
        body = {"model": self.model, "messages": messages}
        if tools:
            body["tools"] = tools
        if self.temperature is not None:
            body["temperature"] = self.temperature

        headers = {"Content-Type": "application/json"}
        if self.api_key_env:
            key = os.environ.get(self.api_key_env)
            if not key:
                raise ModelError(
                    f"Set the {self.api_key_env} environment variable "
                    "to your API key first."
                )
            headers["Authorization"] = "Bearer " + key

        request = urllib.request.Request(
            self.base_url + "/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request,
                                        timeout=self.timeout) as r:
                data = json.load(r)
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", "replace")[:300]
            raise ModelError(
                f"The model server said {error.code}: {detail}")
        except urllib.error.URLError as error:
            raise ModelError(
                f"Could not reach {self.base_url}. Is the model server "
                f"running? ({error.reason})"
            )

        usage = data.get("usage") or {}
        self.tokens_used += usage.get("total_tokens", 0)

        message = data["choices"][0]["message"]
        reply = {"role": "assistant", "content": message.get("content")}
        if message.get("tool_calls"):
            reply["tool_calls"] = message["tool_calls"]
        return reply


def strip_thinking(text):
    """Remove <think>...</think> reasoning that some model setups put
    inside the answer text (Appendix C). Other text is unchanged."""
    if not text:
        return text
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    if cleaned == text:
        return text
    return cleaned.strip()
