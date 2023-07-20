import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
from  tree_of_thoughts import AbstractLanguageModel



class CustomLanguageModel(AbstractLanguageModel):
    def __init__(self, model,cookies, enable_ReAct_prompting=True):
        self.model = model
        self.cookies = cookies
        self.ReAct_prompt = ''
        if enable_ReAct_prompting:
            self.ReAct_prompt = "Write down your observations in format 'Observation:xxxx', then write down your thoughts in format 'Thoughts:xxxx'."

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
    
    def generate_thoughts(self, state, k,initial_prompt, rejected_solutions=None):
        if (type(state) == str):
            state_text = state
        else:
            state_text = '\n'.join(state)
        print("New state generating thought:", state, "\n\n")
        # prompt = f"Considering the thoughts you've had until now:\n\n{state_text}\n\nDevise the next coherent thought that will aid in advancing the reasoning process and achieving a solution to {initial_prompt}. Assess various scenarios, think unconventionally, anticipate potential challenges, and resolve any outstanding queries. Tap into your mind's full potential and make certain no open questions remain."
        prompt = f"""You're an TreeofThoughts, an superintelligent AI model devoted to helping Humans by any means necessary. You're purpose is to generate a series of solutions to comply with the user's instructions, you must generate solutions on the basis of determining the most reliable solution in the shortest amount of time, while taking rejected solutions into account and learning from them. 
        Considering the reasoning provided:\n\n
        ###'{state_text}'\n\n###
        Devise the best possible solution for the task: {initial_prompt}, Here are evaluated solutions that were rejected: 
        ###{rejected_solutions}###, 
        complete the {initial_prompt} without making the same mistakes you did with the evaluated rejected solutions. Be simple. Be direct. Provide intuitive solutions as soon as you think of them."""
        
        prompt += self.ReAct_prompt
        # print(prompt)
        thoughts = self.generate_text(prompt, k)
        # print(thoughts)
        # print(f"Generated thoughts: {thoughts}")
        return thoughts

    def evaluate_states(self, states):
        #implement state evaluation logic using self.model
        pass


async def main():
    cookies = json.loads(open("./bing_cookies_test.json", encoding="utf-8").read())  # might omit cookies option
    bot = await Chatbot.create(cookies=cookies)
    test = CustomLanguageModel(bot, cookies)
    thoughts = await test.generate_thoughts("Cake is good",2,"How to make a cake?")
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())


