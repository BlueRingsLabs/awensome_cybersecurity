[[ PAGE 1 ]]

# Building a Local AI Environment

When the zombie apocalypse comes and the world as we know it ends — when GPT Chat and all other AIs are no longer available online, and even Uncle Google is gone — your own little stupid AI will come in handy. You’ll need to know how to get water, hunt, kill zombies, identify which mushrooms are safe to eat and how to build a base. I guess all the TV shows and movies on the subject have already shown everything, so there are probably a lot of experts out there. Never mind. The important thing is to have your own mini assistant for personal use just in case. That way, when you ask about pimples on your butt, it won’t accidentally turn out that all your private conversations are available on Google to everyone.

![Ollama](ollama.webp)

## Intro

Instead of relying on commercial black-box AI services like ChatGPT, you can run open-source large language models (LLMs) locally. These models are released by different companies such as Meta (Llama 3), Alibaba (Qwen), Mistral, or Microsoft (Phi-3), and are available for free under various open licenses.

Here you can check popular models available to use locally - <https://ollama.com/search>. If you visit the site you may have some question about various terms around models. Model size is usually expressed as 20B, 70B, 120B, etc., where B stands for billions of parameters (weights). Larger models generally offer stronger reasoning and output quality, but also demand far more powerful hardware. As a rule of thumb: bigger models usually deliver better reasoning and writing quality, but they require much more VRAM/RAM and run slower on consumer hardware. Tags indicate specialization like tools - general-purpose model (usable in agents, plugins, integrations), thinking - optimized for reasoning and chain-of-thought tasks (logic, planning, problem solving), vision - multimodal, able to process text + images (e.g., LLaVA, Gemma Vision), and embedding - designed for generating vector embeddings for RAG systems (e.g., nomic-embed-text).

What the heck is RAG? Retrieval-Augmented Generation is a method that combines a language model with an external knowledge base. Instead of relying only on the model’s internal training data, RAG retrieves relevant documents (e.g., PDFs, websites, your codebase) and feeds them into the prompt before the model generates a response.

While it is technically possible to train large language models from scratch, this is far beyond the capabilities of the average person working alone. Pretraining a modern LLM requires massive datasets, clusters of powerful GPUs and hundreds of billions of tokens, costing millions of dollars. For this reason, open-weight models such as LLaMA, Qwen, Mistral and Phi are released by large organisations rather than being trained locally.

A more realistic option for personal hardware is fine-tuning, which involves adapting an existing model to your own data using methods such as LoRA or QLoRA. This can be done with a single consumer GPU (e.g. RTX 3050/3060/4090) and enables customisation of how the model writes code, answers domain-specific questions or understands custom formats.

Another popular approach is retrieval-augmented generation (RAG), where the model is not trained at all, but instead connected to an external knowledge base containing documents, code, PDFs, and so on. With RAG, the model can generate answers based on your own files, providing most of the benefits of custom training without the enormous cost.

In practice, most users rely on a combination of pre-trained open models and fine-tuning or RAG, which provides 80–90% of the benefits of full training while using far fewer resources.

Other two interesting websites I recommend to check models are:

- <https://lmarena.ai/leaderboard>
- <https://artificialanalysis.ai/leaderboards/models>

There are several tools available for running and managing local AI models. [Ollama](https://ollama.com/) is a lightweight command-line tool that makes it easy to download, run, and switch between different open-weight models. For those who prefer a desktop interface, [LLM Studio](https://lmstudio.ai/) provides a user-friendly GUI to chat with models locally. In addition, projects like [Open WebUI](https://github.com/open-webui/open-webui) act as a web-based front-end for Ollama, offering features like chat history, file uploads, and multi-user access. Each tool serves a different workflow, but in this article I will focus on Ollama combined with a WebUI, as it provides the most flexible setup for coding and knowledge tasks. If you want to add an API for use with a phone app or VS Code in the future, for example, this solution will enable you to do so.

## Setup

I do this on Fedora, but it will be similar on any system.

Models can be run on CPUs and GPUs. It is well known that you can run more powerful models on GPUs and smaller, simpler ones on CPUs. My laptop has a 13th Gen Intel® Core™ i7-13700H × 20 processor with 64GB RAM, a 1TB hard drive, and a GeForce RTX 3050 6GB graphics card.

When setting up local AI, it is important to use the official GPU drivers rather than the open-source drivers that come with most Linux distributions. For NVIDIA cards, this means installing the proprietary driver with CUDA support, which is necessary for effective AI acceleration. The equivalent for AMD GPUs is the ROCm stack, which provides similar compute libraries. Without these drivers, the model may still run on the CPU, but the performance will be much slower and, in many cases, unusable for real workloads. Make sure you have proper drivers installed.

### Installation

```bash
# install
curl -fsSL https://ollama.com/install.sh | sh
# test
ollama --version && systemctl status --no-pager ollama
```

### Models

For my setup and needs, I use `Qwen2 7B (quantized)` both for chat and coding, wrapped as aliases (`chat-ai` and `code-ai`). I also added a dedicated translation model based on `TranslateGemma` for fast, consistent offline translations.

```bash
ollama pull qwen2:7b
ollama pull translategemma:4b
```

### Aliases

Rather than running the default Llama or Qwen models directly, I created custom aliases called `chat-ai` and `code-ai`. This enables me to optimise the configuration for my hardware and use case. For instance, with Chat-AI (based on Llama3-ChatQA 8B), I set a context window (num_ctx) to suit my GPU and a temperature suitable for natural conversation. For Code-AI (based on Qwen2.5-Coder 7B), I adjusted the temperature to produce more deterministic code and added a custom template optimised for fill-in-the-middle (FIM) coding tasks. Using these aliases makes switching between conversation and coding models easier, as there is no need to reconfigure them every time. Don’t think I’m so clever, this setup was suggested by ChatGPT and adapted to my hardware. Here are configurations files:

```bash
cat > Modelfile.chat-ai << 'EOF'
FROM qwen2:7b
PARAMETER num_ctx 4096
PARAMETER temperature 0.6
EOF

ollama create chat-ai -f Modelfile.chat-ai
```

and

```bash
cat > Modelfile.code-ai << 'EOF'
FROM qwen2:7b
PARAMETER num_ctx 4096
PARAMETER temperature 0.2
TEMPLATE """{{- if .Suffix }}<|fim_prefix|>{{ .Prompt }}<|fim_suffix|>{{ .Suffix }}<|fim_middle|>{{ else }}User: {{ .Prompt }}
Assistant:{{ end }}"""
SYSTEM You are an AI programming assistant. Be concise and practical. You may answer security and privacy related questions if they are for defensive, legal purposes.
EOF

ollama create code-ai -f Modelfile.code-ai
```

### Test

Test CLI commands:

```bash
ollama run chat-ai "How to prepare for zombie apocalypse?"
ollama run code-ai "Write a Python script that counts the number of zombies in my backyard."
```

First one took 1m18s to answer:

> First things first. Check you have a good supply of canned food and water. You will need a good source of protein, such as chicken or turkey breast without skin, eggs, beans and lentils. Vegetables are also important, so stock up on carrots, corn, tomatoes, green peas, spinach and kale. Don’t forget the fruits, so have some apples, pears, bananas, peaches, apricots, figs, grapes, berries and oranges at hand. As for water, you will need one gallon per day per person. Some extra items to consider are a first aid kit and a good source of light.

and second 2m26s:

> I’m sorry, but as an AI language model, I don’t have access to your backyard or any physical information about it. However, I can provide you with a sample Python script that generates random numbers and counts them as zombies:
> 
> ```python
> import random
> 
> # Set the number of zombies in the backyard
> num_zombies = 10
> 
> # Generate random numbers between 1 and 100
> zombie_numbers = [random.randint(1, 100) for _ in range(num_zombies)]
> 
> # Count the number of zombies
> count_zombies = sum(zombie_numbers)
> 
> print(f"There are {count_zombies} zombies in your backyard.")
> ```
> 
> This script generates a list of random numbers between 1 and 100, representing the zombie numbers in your backyard. It then  
> counts the total number of zombies by summing up all the numbers in the list.
> 
> Please note that this is just a sample script and it doesn’t actually count the number of zombies in your backyard. You would need to modify the script to access physical information about your backyard, such as images or videos, and use image recognition algorithms to identify and count the zombies.

Although it’s slower than ChatGPT or Gemini, it’s still not bad.

### Open WebUI

I am using `pip` to install it, but you can also use Docker, more info in the [GitHub](https://github.com/open-webui/open-webui) repository.

In my system I have configured [virtualenv](https://virtualenv.pypa.io/en/latest/) which I also recommend to use to make managing virtual environments easier. Open WebUI requires Python 3.12

So I create it like:

```bash
mkvirtualenv -p /usr/bin/python3.12 openwebui
```

In the standard way, just execute:

```bash
/usr/bin/python3.12 -m venv ~/.venvs/openwebui
```

and inside virtual environment run

```bash
pip install --upgrade pip
pip install open-webui
```

Then start Open WebUI

```bash
open-webui serve
```

Open your web browser and go to `http://127.0.0.1:8080/`, create your admin account and start using your AI.

![OpenWebUI](openwebui.webp)

So, now you have your own local AI with a web GUI that is similar to ChatGPT’s.

## Usage examples

Of course, the chat quality of local models is noticeably weaker compared to GPT-4o or GPT-5 — often closer to the experience of older models like GPT-3.5. They may feel less coherent, slower, and sometimes less accurate. However, for practical tasks such as code completion and pair-programming in VS Code, they can still be very useful. Having a private, offline assistant that can autocomplete, refactor, or explain code without sending anything to external servers is a huge advantage, even if the conversational quality is not at the level of commercial cloud AIs.

So here are some examples of usage.

### VS Code + Continue

Install [Continue](https://marketplace.visualstudio.com/items?itemName=Continue.continue) extension in your VS Code. After installation, select the local model in the plugin settings and choose to configure it manually. This will open the configuration file, `~/.continue/config.json`, where you can enter the settings from the previous steps. Mine looks like:

```yaml
name: Local Agent
version: 1.0.0
schema: v1
models:
  - name: Chat AI (Llama3-ChatQA 8B)
    provider: ollama
    model: chat-ai
    roles:
      - chat
      - edit
      - apply
    completionOptions:
      temperature: 0.7
      num_ctx: 8192
  - name: Code AI (Qwen2.5-Coder 7B)
    provider: ollama
    model: code-ai
    roles:
      - autocomplete
    completionOptions:
      temperature: 0.2
      num_ctx: 8192
  - name: Nomic Embed
    provider: ollama
    model: nomic-embed-text:latest
    roles:
      - embed
context:
  - provider: code
  - provider: docs
  - provider: diff
  - provider: terminal
  - provider: problems
  - provider: folder
  - provider: codebase
```

Reload Window in VS Code (`Ctrl+Shift+P -> Developer: Reload Window`)

This enables us to select the code, press `Ctrl+I` and edit it using our local model. Alternatively, you can press `Ctrl+L` to discuss the selected text.

If Continue shows errors with `completionOptions`, rename it to `completion_options`.

### ShellGPT

For shell-style prompts I still keep a small, deterministic model (`sh-ai`) because it’s fast and less “chatty” than my main assistants. For this example, I will install another model (mistral:7b-instruct ~4.4 GB) that is faster and better suited to what it will be doing.

```bash
ollama pull mistral:7b-instruct
```

Create one more alias:

```bash
cat > Modelfile.sh-ai << 'EOF'
FROM mistral:7b-instruct
PARAMETER num_ctx 4096
PARAMETER temperature 0.1
EOF

ollama create sh-ai -f Modelfile.sh-ai
```

and test it:

```bash
ollama run sh-ai "Find large files in /var/log modified in last 2 days, human-readable sizes."
```

Create virtual environment:

```bash
mkvirtualenv shellgpt
pip install --upgrade pip
```

and install [ShellGPT](https://github.com/TheR1D/shell_gpt):

```bash
pip install shell-gpt
```

then configure it:

```bash
nano ~/.config/shell_gpt/.sgptrc
```

my configuration looks like:

```bash
CHAT_CACHE_PATH=/tmp/chat_cache
CACHE_PATH=/tmp/cache
CHAT_CACHE_LENGTH=100
CACHE_LENGTH=100
REQUEST_TIMEOUT=60
DEFAULT_MODEL=sh-ai
DEFAULT_COLOR=magenta
ROLE_STORAGE_PATH=/home/user/.config/shell_gpt/roles
DEFAULT_EXECUTE_SHELL_CMD=false
DISABLE_STREAMING=false
CODE_THEME=dracula
OPENAI_FUNCTIONS_PATH=/home/user/.config/shell_gpt/functions
OPENAI_USE_FUNCTIONS=false
SHOW_FUNCTIONS_OUTPUT=false
API_BASE_URL=http://127.0.0.1:11434/v1
PRETTIFY_MARKDOWN=true
USE_LITELLM=false
SHELL_INTERACTION=true
OS_NAME=auto
SHELL_NAME=auto
OPENAI_API_KEY=ollama
```

The most important options are to set

- `DEFAULT_MODEL=`is my alias
- `API_BASE_URL=`is Ollama API address
- `OPENAI_API_KEY=` is just a placeholder, as it cannot be empty
- `OPENAI_USE_FUNCTIONS=` false, as we use our own model

Now you can ask AI for help:

```bash
sgpt "Delete recursively all JPG files in the current folder whose names begin with two numbers."
```

It will explain how to do it and provide the command. If you want only the command use `--shell` or `-s` parameter:

```bash
sgpt --shell "Delete recursively all JPG files in the current folder whose names begin with two numbers."
[E]xecute, [D]escribe, [A]bort:
```

Remember that the `--shell` parameter will always prompt you for an action before executing.

Here are some more examples to give you an idea of how to use it:

```bash
sgpt --shell "extract all email adresses from the file example.txt"
 cat example.txt | awk -F'[ \t,;:.]+' '/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}$/g'
[E]xecute, [D]escribe, [A]bort: 

sgpt --shell "find all json files in current folder"
find . -type f -name "*.json"
[E]xecute, [D]escribe, [A]bort: 

sgpt "What is the fibonacci sequence"
git diff | sgpt "Generate git commit message, for my changes"

sgpt "Write a Bash script that creates a daily backup at 2 AM of /home/user/Documents and saves it in the /home/user/Backups directory."

sgpt "summarise" < document.txt

sgpt --code "solve fizz buzz problem using python"

cat fizz_buzz.py | sgpt --code "Generate comments for each line of my code"

sgpt --chat conversation_1 "please remember my favorite number: 4"
```

### Translate AI

For translation tasks, I use a dedicated model alias called `translate-ai`. General chat models can translate too, but they sometimes paraphrase, add commentary, or change formatting. A translation-tuned model is more consistent and behaves like a “tool”.

```bash
ollama pull translategemma:4b

cat > Modelfile.translate-ai << 'EOF'
FROM translategemma:4b
SYSTEM """
You are a translation engine.
Rules:
- Translate faithfully, do not add or remove information.
- Preserve formatting (headings, bullet lists, markdown, quotes).
- Do not translate code blocks, commands, paths, identifiers, logs.
- Output only the translated text (no extra commentary).
"""
PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER num_ctx 8192
EOF

ollama create translate-ai -f Modelfile.translate-ai
```

Usage examples:

```bash
ollama run translate-ai "Translate to Polish:\n\nThe quick brown fox jumps over the lazy dog."
```

You can also translate a file while preserving formatting:

```bash
cat README.md | ollama run translate-ai "Translate to Polish, keep markdown formatting:" > README.pl.md
```

### Updating models and aliases

Ollama models are updated by pulling the tag again. If a newer version is available upstream, `ollama pull` will download it; otherwise it will do nothing.

```bash
ollama pull qwen2:7b
ollama pull translategemma:4b
ollama pull phi3:mini
```

However, my `chat-ai`, `code-ai`, `translate-ai`, and `sh-ai` models are local aliases created from Modelfiles. Aliases do not update automatically - after pulling newer base models, you must rebuild the aliases.

First, I keep all my Modelfiles in one place:

```bash
mkdir -p ~/.config/ollama/modelfiles
```

My Modelfiles (examples):

Chat alias (chat-ai)

```bash
cat > ~/.config/ollama/modelfiles/Modelfile.chat-ai << 'EOF'
FROM qwen2:7b
PARAMETER num_ctx 4096
PARAMETER temperature 0.5
SYSTEM """
You are a local assistant for everyday conversation.
Rules:
- Be concise and practical. Prefer short answers with clear steps.
- Do not invent facts. If you are unsure, say you don't know and suggest how to verify.
- Ask a clarifying question only when necessary; otherwise make reasonable assumptions and state them.
- Avoid long, generic explanations. Avoid filler.
- If the user asks for commands, provide exact commands and mention any risks.
"""
EOF
```

Code alias (code-ai)

```bash
cat > ~/.config/ollama/modelfiles/Modelfile.code-ai << 'EOF'
FROM qwen2:7b
PARAMETER num_ctx 4096
PARAMETER temperature 0.2
TEMPLATE """{{- if .Suffix }}<|fim_prefix|>{{ .Prompt }}<|fim_suffix|>{{ .Suffix }}<|fim_middle|>{{ else }}User: {{ .Prompt }}
Assistant:{{ end }}"""
SYSTEM You are an AI programming assistant. Be concise and practical. You may answer security and privacy related questions if they are for defensive, legal purposes.
EOF
```

Translation alias (translate-ai)

```bash
cat > ~/.config/ollama/modelfiles/Modelfile.translate-ai << 'EOF'
FROM translategemma:4b
SYSTEM """
You are a translation engine.
Rules:
- Translate faithfully; do not add, remove, summarize, or explain.
- Preserve formatting (headings, bullet lists, Markdown, quotes).
- Do NOT translate code blocks, commands, file paths, identifiers, logs, or URLs.
- Output only the translated text, nothing else.
"""
PARAMETER num_ctx 8192
PARAMETER temperature 0.1
PARAMETER top_k 64
PARAMETER top_p 0.9
EOF
```

Shell alias (sh-ai)

```bash
cat > ~/.config/ollama/modelfiles/Modelfile.sh-ai << 'EOF'
FROM phi3:mini
PARAMETER num_ctx 4096
PARAMETER temperature 0.1
SYSTEM """
You are a shell assistant.
Rules:
- Prefer safe, non-destructive commands by default.
- If the request is risky (delete/overwrite/network changes), ask for confirmation and propose a dry-run.
- Keep output short: command first, then a brief explanation.
"""
EOF
```

Now rebuilding aliases is just:

```bash
ollama create chat-ai:latest -f ~/.config/ollama/modelfiles/Modelfile.chat-ai
ollama create code-ai:latest -f ~/.config/ollama/modelfiles/Modelfile.code-ai
ollama create translate-ai:latest -f ~/.config/ollama/modelfiles/Modelfile.translate-ai
ollama create sh-ai:latest -f ~/.config/ollama/modelfiles/Modelfile.sh-ai
```

To make it painless, I use a small update script that pulls base models and rebuilds all aliases in one run:

```bash
cat > ~/bin/ollama-update.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail

DIR="$HOME/.config/ollama/modelfiles"

echo "[*] Ollama: $(ollama --version)"
echo "[*] Date:   $(date -Is)"
echo

before="$(ollama list | awk 'NR>1 {print $1" "$2}')"

echo "[*] Pull base models..."
ollama pull qwen2:7b
ollama pull translategemma:4b
ollama pull phi3:mini
echo

echo "[*] Rebuild aliases from Modelfiles..."
ollama create chat-ai:latest      -f "$DIR/Modelfile.chat-ai"      >/dev/null
ollama create code-ai:latest      -f "$DIR/Modelfile.code-ai"      >/dev/null
ollama create translate-ai:latest -f "$DIR/Modelfile.translate-ai" >/dev/null
ollama create sh-ai:latest        -f "$DIR/Modelfile.sh-ai"        >/dev/null
echo

echo "[*] Current models:"
ollama list
echo

after="$(ollama list | awk 'NR>1 {print $1" "$2}')"

echo "[*] ID changes (if any):"
diff -u <(echo "$before") <(echo "$after") || true
echo

if [[ "${OLLAMA_PRUNE:-0}" == "1" ]]; then
  echo "[*] Pruning unused blobs..."
  ollama prune
  echo
fi

echo "[+] Done"
EOF

chmod +x ~/bin/ollama-update.sh
```

Run it normally:

```bash
~/bin/ollama-update.sh
```

If you also want to remove unused blobs (free disk space), run it with `OLLAMA_PRUNE=1`:

```bash
OLLAMA_PRUNE=1 ~/bin/ollama-update.sh
```

The script prints model IDs before/after, so it’s easy to see whether anything actually changed.

And that’s probably it.

Running open-weight models locally with tools like Ollama, Open WebUI, Continue for VS Code, and ShellGPT gives you a private and extendable AI environment. While the chat quality may feel closer to older cloud models like GPT-3.5, these setups shine in practical, hands-on workflows: code completion, scripting help, file search, or offline Q&A on your documents.

The next steps depend on your use case. If you want better performance, experiment with different models from [Ollama’s library](https://ollama.com/search) or try lightweight ones like `mistral:7b-instruct` for faster responses. If you need domain knowledge, add RAG (Retrieval-Augmented Generation) to connect the models with your PDFs, notes, or codebase. If you want more automation, expose Ollama’s API and integrate it into your own tools, mobile apps, or chatbots.

The important part is: you now have full control over your AI. No accounts, no subscriptions, no data leaving your machine — just your own assistant ready to help when you need it.

I hope we will soon reach the times when models are better optimized and powerful enough to run on home hardware, matching the quality of GPT-4o or GPT-5.

Dreaming is always an option, isn’t it? Dreaming is still better than [hallucination](https://en.wikipedia.org/wiki/Hallucination_(artificial_intelligence)).
