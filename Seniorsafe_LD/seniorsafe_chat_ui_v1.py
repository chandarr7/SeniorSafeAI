from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

import chainlit as cl

@cl.set_starters
async def set_starters():
    return [
    	cl.Starter(
        	label="Identity Stolen",
        	message="What should I do if my identity has been stolen in an online scam?",
        	icon="/public/identity_theft.png",
    ),
    	cl.Starter(
        	label="Financial Loss",
        	message="How can I recover money lost to a scammer?",
        	icon="/public/financial_loss.png",
    ),
    	cl.Starter(
        	label="Protecting Accounts",
        	message="How can I protect my bank accounts after being scammed?",
        	icon="/public/protect_accounts.png",
    ),
    	cl.Starter(
        	label="Reporting a Scam",
        	message="Who should I report a cyber scam to?",
        	icon="/public/report_scam.png",
        ),
        cl.Starter(
            label="Tech Support Scam",
            message="I received a call claiming to be from tech support. What should I do?",
            icon="/public/protect_accounts.png",
        ),
        cl.Starter(
            label="Phishing Email",
            message="I clicked on a suspicious link in an email. What are my next steps?",
            icon="/public/identity_theft.png",
        )
    ]

@cl.on_chat_start
async def on_chat_start():
    model = Ollama(model="mistral") ## default
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a knowledgeable, empathetic, and honest assistant designed to help victims of cybercrime. "
                "Provide clear, step-by-step advice in simple language that seniors can easily understand. "
                "Be patient, supportive, and reassuring. Break down complex technical concepts into easy-to-follow instructions. "
                "Always prioritize the user's safety and security.",
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)

    # Send a welcoming message
    await cl.Message(
        content="Hello! I'm SeniorSafe AI, your personal cybersecurity assistant. "
                "I'm here to help you if you've been affected by online scams or cybercrime. "
                "You can ask me anything, or choose one of the quick start options above. "
                "Don't worry - we'll work through this together, step by step."
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)
    await msg.stream_token("&*&8")
    await msg.send()
