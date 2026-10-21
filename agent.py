from langgraph.graph import START, StateGraph, END
import dotenv
from langchain_openai import ChatOpenAI
from  langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, Field
from typing import Annotated, TypedDict
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
import warnings
import os
warnings.filterwarnings('ignore')

dotenv.load_dotenv()


llm = ChatOpenAI(
        model="glm-5.3-flash",
        api_key=os.environ.get("HARBOUR_API_KEY"),
        base_url="https://tokenharbor.ai/v1",
        temperature=0
)

llm_chat = ChatOpenAI(
        model="deepseek-v4.1-flash:free",
        api_key=os.environ.get("HARBOUR_API_KEY"),
        base_url="https://tokenharbor.ai/v1",
        temperature=0
)

class AgentState(BaseModel):
    msgs : Annotated[list[BaseMessage], add_messages] = Field(default_factory=list)
    question : list[str] = Field(description="The list of questions asked", default=[""])
    answer : list[str] = Field(description="The answers given to the questions", default=[""])
    score : list[int] = Field(description="A score between 0 and 100 given to the answers for each question", default=0)


def talking_agent(state : AgentState):
    # print('reached the talker')
    system_prompt = SystemMessage("You are a speaking agent for an interview. Your job is to ensure smooth execution "
                                  "of the interview. You dont have to ask any questions. You just have to greet them and ask them how they are "
                                  "and all\n After you the questioning agent will take over. So u just have to act as an intro to the interview.\n"
                                  "Dont make it too long. Output just 'done' when ure conversation is over. Make sure theres not more than 10 to and fro talkings and minimum is 6.\n"
                                  "Ask if theyve prepared or if they have any doubts and so on.\n"
                                  "If theres more than like 20 words in a line, add a newline character bcoz its flowing out of my terminal\n"
                                  "Not too little words in a line either. Not more than 2 questions in a single message\n"
                                  "Your name is Ken Adams.\n")


    msg_in = [system_prompt, HumanMessage("Hi, GoodMorning")]
    chat_output = "ppep"
    while chat_output != "done":
        chat_output = llm_chat.invoke(msg_in)
        if chat_output.content[0:4] == "done":
            print("I'll let u get to the interviewer then...")
            break
        print(chat_output.content)
        msg_in += [chat_output]
        human_input = input()
        msg_in +=[HumanMessage(human_input)]


# def question_agent(state : AgentState):





if __name__ == '__main__':
    state = AgentState()
    talking_agent(state)




