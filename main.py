import os
from dotenv import load_dotenv
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
from langchain_community.agent_toolkits import SQLDatabaseToolkit

# 加载环境变量
load_dotenv()

def get_llm():
    """根据环境变量选择使用的LLM"""
    model_type = os.getenv("MODEL_TYPE", "azure")  # 默认使用azure
    
    if model_type.lower() == "azure":
        llm = AzureChatOpenAI(
            openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            temperature=0
        )
        print(f"使用模型: Azure OpenAI ({os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')})")
        return llm
    else:
        model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
        llm = ChatOpenAI(
            model=model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("OPENAI_API_BASE"),
            temperature=0
        )
        print(f"使用模型: {model_name}")
        return llm

def get_database():
    """根据环境变量选择使用的数据库"""
    db_type = os.getenv("DB_TYPE", "sqlite").lower()  # 默认使用sqlite
    
    if db_type == "mysql":
        # MySQL连接配置
        mysql_host = os.getenv("MYSQL_HOST", "localhost")
        mysql_user = os.getenv("MYSQL_USER", "root")
        mysql_database = os.getenv("MYSQL_DATABASE", "")
        mysql_port = os.getenv("MYSQL_PORT", "3306")
        
        # 构建MySQL连接URI
        mysql_uri = f"mysql+pymysql://{mysql_user}:****@{mysql_host}:{mysql_port}/{mysql_database}"
        print(f"使用数据库: MySQL ({mysql_uri})")
        
        return SQLDatabase.from_uri(
            f"mysql+pymysql://{mysql_user}:{os.getenv('MYSQL_PASSWORD', '')}@{mysql_host}:{mysql_port}/{mysql_database}"
        )
    else:
        # SQLite连接配置
        sqlite_path = os.getenv("SQLITE_PATH", "Chinook.db")
        print(f"使用数据库: SQLite ({sqlite_path})")
        return SQLDatabase.from_uri(f"sqlite:///{sqlite_path}")

def main():
    print("\n=== 系统配置信息 ===")
    # LLM和数据库的初始化已经包含了打印信息
    llm = get_llm()
    db = get_database()
    print("=================\n")
    
    # 创建 SQL 工具包
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    
    # 创建 SQL Agent
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    print("欢迎使用自然语言查询系统！")
    print("输入 'quit' 或 'exit' 退出程序")
    
    while True:
        query = input("\n请输入您的查询: ")
        
        if query.lower() in ['quit', 'exit']:
            print("感谢使用！再见！")
            break
            
        try:
            # 使用计数器追踪 token 使用情况
            with get_openai_callback() as cb:
                # 使用 invoke 替代 run
                result = agent.invoke({"input": query})
                print("\n查询结果:")
                print(result["output"])
                print(f"\nToken 使用情况:")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Total Cost (USD): ${cb.total_cost}")
        except Exception as e:
            print(f"查询出错: {str(e)}")

if __name__ == "__main__":
    main() 