import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
from  tree_of_thoughts import AbstractLanguageModel

async def main():
    cookies = json.loads(open("./bing_cookies_test.json", encoding="utf-8").read())  # might omit cookies option
    bot = await Chatbot.create(cookies=cookies)
    response = await bot.ask(prompt="Hello world", conversation_style=ConversationStyle.creative, simplify_response=True)
    print(json.dumps(response, indent=2)) # Returns
    """
{
    "text": str,
    "author": str,
    "sources": list[dict],
    "sources_text": str,
    "suggestions": list[str],
    "messages_left": int
}
    """
    test = CustomLanguageModel(bot)
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())



class CustomLanguageModel(AbstractLanguageModel):
    def __init__(self, model):
        self.model = model

    def generate_thoughts(self, state, k):
        #implement the thought generation logic using self.model
        pass

    def evaluate_states(self, states):
        #implement state evaluation logic using self.model
        pass
