from os.path import exists
import openai
import json
class ChatBot():

    def __init__(self,botName,personalityFile="",tokenLimit=1000,organization="",apiKey="",debug=False,gpt_3_5=False):
        config = {"organization":organization,"apiKey":apiKey}

        self.debug = debug
        self.__init__OpenAIAPI(config)

        self.gpt_3_5         = gpt_3_5
        self.botName         = botName
        self.tokenLimit      = tokenLimit
        self.personality     = ""
        self.prompt_buffer   = self.__remind()
        self.personalityFile = personalityFile
        self.buffer_limit    = 100
        if self.loadPersonalityFile:
            self.loadPersonalityFile()

        self.__helloFlag      = False

    def loadModelParams(self):
        pass

    def loadPersonalityFile(self):
        with open(self.personalityFile,"r",encoding="utf-8") as f:
            self.personality = f.read()
            if self.debug:
                print(f"PERSONALITY:{self.personality}")

    def __memorize(self):
        with open(self.botName+".json","w+",encoding="utf-8") as f:
            json.dump(self.prompt_buffer,f)

    def __remind(self):
        filename = self.botName+".json"
        prompt_buffer = ""
        if exists(filename):
            with open(self.botName+".json","r", encoding="utf-8") as f:
                prompt_buffer = json.load(f)
        return prompt_buffer

    def __addToPrompt(self,prompt,username):
        # adding username
        msg = { "role ": username , "content" : prompt}
        self.prompt_buffer.append(msg)

        while self.prompt_buffer > self.buffer_limit:
            self.prompt_buffer.pop(0)

        return self.prompt_buffer

    def __prepareForChatGPT(self,promptBuffer):

        personality = {"role" : "system" , "content" : self.personality}
        chatGptMessages = [personality]

        for message in promptBuffer:
            if message["role"] == self.botName:
                chatGptMessages.append({"role":"assistant","content":message["content"]})
            else:
                chatGptMessages.append({"role":"user","content":message["content"]})

        return chatGptMessages
        # if len(self.prompt_buffer)/4 > self.tokenLimit:
        #     self.prompt_buffer = self.prompt_buffer[-self.tokenLimit:]

    def __prepareForGpt(self,promptBuffer):

        prompt = ""
        for message in promptBuffer[::-1]:
            prompt += f"{message['role']}:\n"
            prompt += f"{message['content']}:\n"

        if len(prompt) > self.tokenLimit:
            prompt = prompt[len(prompt)-self.tokenLimit:]

        prompt = f"Pretend to be {self.botName}: {self.personality}\n" + prompt
        return prompt

    def __init__OpenAIAPI(self,config):
        # print(config["organization"])
        openai.organization = config["organization"]
        openai.api_key = config["apiKey"]

    def __askGPT(self, promptBuffer):
        prompt = self.__prepareForGpt(promptBuffer)
        ret_completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.75,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return ret_completion["choices"][0]["text"]

    def __askChatGPT(self, promptBuffer):
        prompt = self.__prepareForChatGPT(promptBuffer)
        ret_completion = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            temperature=0.75,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return ret_completion["choices"][0]["text"]

    def ask(self,message,user="USER"):

        self.promptBuffer = self.__addToPrompt(message,F"{user}")

        if self.debug:
            print(f"SENDING PROMPT:\n{self.promptBuffer}")

        response = self.__askGPT(self.promptBuffer)
        self.promptBuffer = self.__addToPrompt(response,f"{self.botName}")
        self.__memorize()
        # self.update_file("gpt",response)

        return response