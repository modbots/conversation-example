from openAI import OpenAi
import ijson


class OpenAiChat:

    def __init__(self, prefix, botName):
        self.prefix = prefix
        self.chatContextFile = "chatContext.json"
        self.chatContext = self.loadChatContext()
        self.openai = OpenAi(prefix=prefix)
        self.botName = botName

    def loadChatContext(self):
        # use ijason to parse the json file
        with open(self.chatContextFile, 'r') as f:
            if f.read() == '':
                return {}
            objects = ijson.items(f, 'item')
            chatContext = list(objects)

    def saveChatContext(self):
        with open(self.chatContextFile, 'w') as f:
            ijson.dump(chatContext, f)

    

    def askQuestion(self, question, chat_id, user_name, first_name, last_name=''):
        # check if chat_id exists in chatContext
        if chat_id in self.chatContext:
            # if exists, get the context
            context = self.chatContext[chat_id][user_name]
        else:
            # if not exists, create a new context
            context = "\nYou are chatting with "+first_name+" "+last_name
            self.chatContext[chat_id] = {}
            self.chatContext[chat_id][user_name] = context
        # ask question
        context += '\nQuestion: '+question+'\n'+'Answer: '
        reply = self.openai.askQuestion(context)
        # update context
        self.chatContext[chat_id][user_name] = context
        # save context
        self.saveChatContext()
        return reply

    def generateImage(self, question):
        return self.openai.generateImage(question)


if __name__ == "__main__":
    openi = OpenAiChat(prefix="This is a test", botName="testBot")
    openi.askQuestion("How are you?", "123", "@testUser",
                      "testFirstName", "testLastName")
