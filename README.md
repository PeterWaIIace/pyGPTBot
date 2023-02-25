# pyGPTBot
Wrapper python package around gpt3 for chatBot.

## Install:

```
pip install pyGPTBot
```

## Features:

- Can remember conversation 
- Its memmory is adjustable by length of tokens in prompt
- Easy to use
- Can have personality [WIP]

## How to use:

### SETUP:

```
config = {}
with open("src/config.json") as f:
    config = json.load(f)

lovelyBot = pyGptBot.ChatBot("MyLovelyBot",organization=config["organization"],apiKey=config["apiKey"])
```

### RUNTIME:

```
[...]

msg = "hello who are you"
reponse = lovelyBot.ask(msg)
print(reponse)

[...]
```
