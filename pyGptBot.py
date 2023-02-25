from os.path import exists
import openai

class ChatBot():

    def __init__(self,botName,personalityFile="",tokenLimit=1000,organization="",apiKey="",debug=False):
        config = {"organization":organization,"apiKey":apiKey}

        self.debug = debug
        self.__init__OpenAIAPI(config)

        self.botName         = botName
        self.tokenLimit      = tokenLimit
        self.personality     = ""
        self.prompt_buffer   = self.__remind()
        self.personalityFile = personalityFile
        if self.loadPersonalityFile:
            self.loadPersonalityFile()

        self.__helloFlag      = False

    def loadPersonalityFile(self):
        with open(self.personalityFile,"r",encoding="utf-8") as f:
            self.personality = f.read()
            if self.debug:
                print(f"PERSONALITY:{self.personality}")

    def __memorize(self):
        with open(self.botName+".txt","w+",encoding="utf-8") as f:
            f.write(self.prompt_buffer)

    def __remind(self):
        filename = self.botName+".txt"
        prompt_buffer = ""
        if exists(filename):
            with open(self.botName+".txt","r", encoding="utf-8") as f:
                prompt_buffer = f.read()
        return prompt_buffer

    def __addToPrompt(self,prompt,username):
        # adding username
        self.prompt_buffer += f"{username}:\n"
        self.prompt_buffer += prompt

        if len(self.prompt_buffer)/4 > self.tokenLimit:
            self.prompt_buffer = self.prompt_buffer[-self.tokenLimit:]

        return self.prompt_buffer

    def __init__OpenAIAPI(self,config):
        # print(config["organization"])
        openai.organization = config["organization"]
        openai.api_key = config["apiKey"]

    def __askOpenAI(self, message):
        ret_completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            temperature=0.5,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return ret_completion["choices"][0]["text"]

    def __sayHello(self):
        if self.__helloFlag == False:
            self.__helloFlag = True
            response = self.ask("hello")
            return response

    def ask(self,message):

        message = self.__addToPrompt(message,"USER:")
        message += f"\n{self.botName}:\n"

        prompt = f"This AI follows those rules: \"{self.personality}\" \n\nConversation:\n"+ message+"AI:"
        if self.debug:
            print(f"SENDING PROMPT:\n{prompt}")

        response = self.__askOpenAI(prompt)
        self.__addToPrompt(response,"AI:")
        self.__memorize()
        # self.update_file("gpt",response)

        return response