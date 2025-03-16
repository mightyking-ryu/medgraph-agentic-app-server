import re

import networkx as nx
import nx_arangodb as nxadb

from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_community.graphs import ArangoGraph
from langchain_community.chains.graph_qa.arangodb import ArangoGraphQAChain

from config.settings import ARANGODB_CONFIG
from db.arangodb_manager import ArangoDBManager

# -------------------------
# 3. LangChain/LangGraph Agent
# -------------------------

# Generate ArangoGraph
arangodb_manager = ArangoDBManager(ARANGODB_CONFIG)

arango_graph = ArangoGraph(arangodb_manager.db)
G_adb = nxadb.Graph(name="MyGraph", db=arangodb_manager.db)


# generate LLM Object (GPT-4o)
llm = ChatOpenAI(temperature=0, model_name="gpt-4o")


@tool
def text_to_aql_to_text(query: str):
    """This tool is available to invoke the
    ArangoGraphQAChain object, which enables you to
    translate a Natural Language Query into AQL, execute
    the query, and translate the result back into Natural Language.
    """
    chain = ArangoGraphQAChain.from_llm(
    	llm=llm,
    	graph=arango_graph,
    	verbose=True,
        allow_dangerous_requests=True
    )

    result = chain.invoke(query)

    return str(result["result"])

# 도구 3: Text to NetworkX/cuGraph 알고리즘 도구 (자연어 -> Python 코드 생성 및 실행)
@tool
def text_to_nx_algorithm_to_text(query: str):
    """ docstring"""
    print("1) Generating NetworkX code")
    code_response = llm.invoke(f"""
    I have a NetworkX Graph called `G_adb`. Its schema is: {arango_graph.schema}.
    For the query: {query},
    generate Python code using `G_adb` that answers the query.
    Ensure the final answer is stored in a variable named FINAL_RESULT.
    Your code:
    """).content

    code_clean = re.sub(r"^```python\n|```$", "", code_response, flags=re.MULTILINE).strip()
    print("Generated code:\n", code_clean)

    global_vars = {"G_adb": G_adb, "nx": nx}
    local_vars = {}
    try:
        exec(code_clean, global_vars, local_vars)
    except Exception as e:
        return f"EXEC ERROR: {e}"
    FINAL_RESULT = local_vars.get("FINAL_RESULT", "No result produced")

    answer = llm.invoke(f"""
        I have a NetworkX Graph called `G_adb` with schema: {arango_graph.schema}.
        For the query: {query},
        after executing the following Python code:
        {code_clean}
        The FINAL_RESULT is: {FINAL_RESULT}.
        Generate a concise answer.
        Your response:
    """).content
    return answer

tools = [text_to_aql_to_text, text_to_nx_algorithm_to_text]

def query_graph(query: str) -> str:
    agent = create_react_agent(llm, tools)
    final_state = agent.invoke({"messages": [{"role": "user", "content": query}]})
    return final_state["messages"][-1].content