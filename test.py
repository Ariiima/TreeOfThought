import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
from  tree_of_thoughts import AbstractLanguageModel



class CustomLanguageModel(AbstractLanguageModel):
    def __init__(self, model,cookies):
        self.model = model
        self.cookies = cookies

    async def generate_text(self, prompt, k):
        if self.model:
            thoughts = []
            for _ in range(k):
                response = await self.model.ask(prompt=prompt, conversation_style=ConversationStyle.balanced, simplify_response=True)
                text = response['text']
                thoughts += [text]
                print(f'thoughts: {thoughts}')
                await self.model.delete_conversation()
                self.model = await Chatbot.create(cookies=self.cookies)
            return thoughts
        return None
    
    def generate_thoughts(self, state, k):
        #implement the thought generation logic using self.model
        pass

    def evaluate_states(self, states):
        #implement state evaluation logic using self.model
        pass


async def main():
    cookies = json.loads(open("./bing_cookies_test.json", encoding="utf-8").read())  # might omit cookies option
    bot = await Chatbot.create(cookies=cookies)
    test = CustomLanguageModel(bot, cookies)
    thoughts = await test.generate_text("just output what's 3+2?", 3)
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())


