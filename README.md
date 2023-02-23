# pyGPTBot
Wrapper python package around gpt for chatBot

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
