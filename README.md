# Séance 🕯️

Summon the ghost of a dead programming language and talk to it, fully offline.

Séance is a terminal chatbot that channels COBOL, Pascal, ActionScript (Flash) or
FORTRAN 77. Each ghost has its own voice, its own grudge against the modern world,
and real facts about its own era. It runs on **Gemma 3 4B**, an open-weight model,
through **Ollama** on your own machine. There is no API key, no account, and no internet.

Built for the DEV **Hacktoberfest Open-Source AI Challenge, Week 4: "Ghost in the Machine"**.

```
The candles gutter. The fans spin down. Something old answers...
IDENTIFICATION DIVISION. PROGRAM-ID. GHOST. WHO DISTURBS THE MAINFRAME.

you> Are you an AI?
NEGATIVE, ABSOLUTELY NEGATIVE. I AM COBOL, BORN IN 1959 ...
```

## Run it

1. Install [Ollama](https://ollama.com) and pull the model:
   ```
   ollama pull gemma3:4b
   ```
2. Summon a ghost (Python 3.10+, standard library only):
   ```
   python3 seance.py cobol      # or pascal, flash, fortran; omit for a random one
   ```
3. Type `goodbye` to end the séance.

Use another model with `--model` or `SEANCE_MODEL`, for example `gemma3:1b` on slower machines.

## How it works

- `spirits.py` holds each ghost as data: name, birth, death, voice, grudge, greeting.
- `spirit_rules()` adds the séance rules that keep a small model in character: it
  senses modern tools only dimly, treats "are you an AI?" as an exorcism attempt,
  and grounds every joke in true facts about its language.
- `seance.py` builds the system prompt and streams the reply from Ollama's local
  `/api/chat` endpoint.

## Why open-weight

The whole séance happens on your laptop. It works with the Wi-Fi off, costs nothing
per message, and no conversation leaves the machine. Because the model is open, you
can swap it, run it on old hardware, or fine-tune a ghost of your own.

## License

MIT
