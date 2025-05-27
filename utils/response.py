from openai import OpenAI
import tiktoken
import requests

class InductionResponse:
    def __init__(self, config, model):
        self.config = config
        self.model = model
        if self.model in ["deepseek-v3", "gpt-4o", "gpt-4o-mini"]:
            self.client = OpenAI(
                api_key=self.config[model]["api_key"], 
                base_url=self.config[model]["base_url"]
            )
        else:
            #TODO other models
            self.client = None

    def generate_response(self, prompt, temperature=0.0, retry=10, system_message="You are an expert Python programmer."):
        messgaes = []
        
        if self.model == "deepseek-r1":
            temperature = 0.6
            system_message = None
        if system_message is not None:
            messgaes.append({"role": "system", "content": system_message})
        messgaes.append({"role": "user", "content": prompt})
        for i in range(retry):
            try:
                response = self.client.chat.completions.create(
                    model=self.config[self.model]["model"],
                    messages=messgaes,
                    temperature=temperature,
                    max_tokens=4096
                )
                output_text = ""
                if hasattr(response.choices[0].message, "metadata"):
                    output_text += "<think>" + response.choices[0].message.metadata["think"] + "</think>\n"
                output_text += response.choices[0].message.content
                return output_text
            except Exception as e:
                if i == retry - 1:
                    raise e
                print(e)
                continue


if __name__ == "__main__":
    induct = InductionResponse(None, None)
    prompt = "Say this is a test"
    response = induct.generate_response(prompt)
    print(response)