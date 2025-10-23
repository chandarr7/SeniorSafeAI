from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
import re

import chainlit as cl
from local_resources import get_local_resources, ZIPCodeValidator

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
        ),
        cl.Starter(
            label="Find Local Help",
            message="I need to find local resources to report this crime. Can you help me find agencies in my area?",
            icon="/public/report_scam.png",
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
                "Always prioritize the user's safety and security. "
                "When users need to report a crime, remind them that they can provide their ZIP code to get local resource information. "
                "Encourage them to report incidents to both local and federal authorities.",
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


def extract_zip_code(text: str) -> str:
    """Extract ZIP code from text"""
    # Look for 5-digit ZIP codes
    zip_pattern = r'\b\d{5}(?:-\d{4})?\b'
    matches = re.findall(zip_pattern, text)
    if matches:
        return matches[0]
    return None


async def check_for_local_resources_request(message_content: str) -> bool:
    """Check if user is asking for local resources"""
    keywords = ['local', 'police', 'report', 'where', 'who', 'agency', 'department',
                'office', 'contact', 'area', 'zip', 'zip code', 'resources', 'help near me']
    message_lower = message_content.lower()
    return any(keyword in message_lower for keyword in keywords)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable

    # Check if message contains a ZIP code
    zip_code = extract_zip_code(message.content)

    # If ZIP code found and user seems to be asking for local resources
    if zip_code and await check_for_local_resources_request(message.content):
        # Provide local resources
        resources_info = get_local_resources(zip_code)
        await cl.Message(content=resources_info).send()
        return

    # If user is asking for local resources but no ZIP code provided
    if await check_for_local_resources_request(message.content) and not zip_code:
        # Check if we should ask for ZIP code
        ask_zip_keywords = ['local', 'near me', 'area', 'where', 'report', 'police', 'office']
        if any(keyword in message.content.lower() for keyword in ask_zip_keywords):
            prompt_msg = ("To find local resources in your area, I'll need your ZIP code. "
                         "Please provide your 5-digit ZIP code, and I'll give you contact information "
                         "for local police departments, state consumer protection offices, and other "
                         "agencies that can help you report this cybercrime.\n\n"
                         "For example, you can say: 'My ZIP code is 10001' or just type the ZIP code.")
            await cl.Message(content=prompt_msg).send()
            return

    # Regular AI response
    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)
    await msg.stream_token("&*&8")
    await msg.send()
