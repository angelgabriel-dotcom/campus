import json
import os
import urllib.request
import urllib.error
import socket

green = "\033[32;1m"
reset = "\033[0m"
red = "\033[31;1m"
yellow = "\033[33;1m"


MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL}:generateContent"
)


_original_getaddrinfo = socket.getaddrinfo


def _ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
    return _original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)


socket.getaddrinfo = _ipv4_only

def build_prompt(ticket):
    description = ticket.get("T_description") or ticket.get("description", "")
    return (
        "You are a campus IT helpdesk assistant. A user reported this problem:\n\n"
        f"{description}\n\n"
        "Suggest 3 to 5 possible ways to investigate or fix it. "
        "Reply as a short numbered list, one line each, with no introduction."
    )


def ask_ai(prompt):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return None, "Missing API key. Set the GEMINI_API_KEY environment variable."

    body = {"contents": [{"parts": [{"text": prompt}]}]}
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            reply = json.loads(resp.read().decode("utf-8"))
        text = reply["candidates"][0]["content"]["parts"][0]["text"]
        return text.strip(), None

    except urllib.error.HTTPError as e:       # must come BEFORE URLError
        if e.code in (400, 401, 403):
            return None, "The request was rejected. Check that your API key is valid."
        if e.code == 404:
            return None, f"Model '{MODEL}' is unavailable. Try another with GEMINI_MODEL."
        if e.code == 429:
            return None, "Rate limit or free quota reached. Wait a bit and try again."
        if e.code >= 500:
            return None, "The AI service is having problems. Try again later."
        return None, f"The AI service returned an error (code {e.code})."
    except urllib.error.URLError as e:
        return None, f"Could not reach the AI service ({e.reason})."
    except TimeoutError:
        return None, "The AI service took too long to answer."
    except (KeyError, IndexError, TypeError, json.JSONDecodeError):
        return None, "The AI sent a reply that could not be read."


def show_suggestions(ticket):
    print(f"\n{green}Wait A Little for Response{reset}")
    text, error = ask_ai(build_prompt(ticket))
    print(f"\n{green}Wait a Little Getting AI suggestions...{reset}\n")
    if error:
        print(f"{red}Could not get suggestions:{reset} {error}")
        return
    print(f"{yellow}Suggestions:{reset}\n")
    print(f"{green}{text}{reset}")

