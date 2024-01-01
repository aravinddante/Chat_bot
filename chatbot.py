import os
import chainlit as cl
from langchain import HuggingFaceHub, PromptTemplate, LLMChain
from getpass import getpass


HUGGINGFACEHUB_API_TOKEN = getpass()
conv_model = HuggingFaceHub(huggingfacehub_api_token = os.environ['HUGGINGFACEHUB_API_TOKEN'],
repo_id = model_id, model_kwards = {"temperature":0.6, "max_new_tokens":150})

template = """ You are a medical AI assistant that helps patients with their medical doubts and suggest a connection to a doctor when you are not sure 
{query}
"""


@cl.on_chat_start
def main():
  prompt = PromptTemplate(template = template, input_variables = ['query'])
  conv_chain = LLMChain(llm = conv_model, prompt = prompt, verbose = True)
  cl.user_session.set("llm_chain", conv_chain)

@cl.on_message
async def main(message:str):
  llm_chain = cl.user_session.get("llm_chain")
  res = await llm_chain.acall(message, callbacks = [cl.AsyncLangchainCallbackHandler()])
  await cl.message(content = res["text"]).send()
