import os
import requests
import streamlit as st
import pandas as pd
from databricks import sql
from databricks.sdk.core import Config
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.dashboards import GenieAPI

# --- Sidebar menu ---
st.set_page_config(layout="wide")
menu = st.sidebar.radio(
    "Menu",
    options=["Dashboard", "Genie", "Detalhes"],
    index=0
)

# --- Shared SQL connection ---
def sqlQuery(query: str) -> pd.DataFrame:
    cfg = Config()
    with sql.connect(
        server_hostname=cfg.host,
        http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_WAREHOUSE_ID')}",
        credentials_provider=lambda: cfg.authenticate
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall_arrow().to_pandas()

@st.cache_data(ttl=30)
def getData():
    return sqlQuery("select * from workshop_rails.rails.telemetria limit 100")

# --- Dashboard Page ---
if menu == "Dashboard":
    st.header("Dashboard Embed Databricks")
    dashboard_url = "<<URL DASHBOARD AQUI>>"
    st.components.v1.iframe(
        src=dashboard_url,
        height=800,
        width=1200
    )

# --- Genie Page ---
elif menu == "Genie":
    st.header("🤖 Genie: IA para consulta dos dados")
    st.markdown("Pergunte o que quiser sobre o dataset de inadimplência e obtenha insights em linguagem natural!")

    genie_space_id = "<<ID GENIE SPACE AQUI>>""
    workspace_client = WorkspaceClient()
    genie_api = GenieAPI(workspace_client.api_client)
    conversation_id = st.session_state.get("genie_conversation_id", None)

    def ask_genie_sync(question: str, space_id: str, conversation_id: str = None):
        import asyncio
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            if conversation_id is None:
                initial_message = loop.run_until_complete(
                    loop.run_in_executor(None, genie_api.start_conversation_and_wait, space_id, question)
                )
                conversation_id_local = initial_message.conversation_id
            else:
                initial_message = loop.run_until_complete(
                    loop.run_in_executor(None, genie_api.create_message_and_wait, space_id, conversation_id, question)
                )
                conversation_id_local = conversation_id

            answer_json = {"message": ""}
            for attachment in initial_message.attachments:
                if getattr(attachment, "text", None) and getattr(attachment.text, "content", None):
                    answer_json["message"] = attachment.text.content
                    break
                if getattr(attachment, "query", None):
                    query_result = loop.run_until_complete(
                        loop.run_in_executor(None, genie_api.get_message_query_result,
                            space_id, initial_message.conversation_id, initial_message.id)
                    ) if hasattr(genie_api, "get_message_query_result") else None
                    if query_result and hasattr(query_result, "statement_response") and query_result.statement_response:
                        sql_results = loop.run_until_complete(
                            loop.run_in_executor(None, workspace_client.statement_execution.get_statement,
                                query_result.statement_response.statement_id)
                        )
                        answer_json["columns"] = sql_results.manifest.schema.as_dict()
                        answer_json["data"] = sql_results.result.as_dict()
                        desc = getattr(attachment.query, "description", "")
                        answer_json["query_description"] = desc
                        answer_json["sql"] = getattr(attachment.query, "query", "")
                        break
            loop.close()
            return answer_json, conversation_id_local
        except Exception as e:
            return {"message": f"Erro consultando Genie: {str(e)}"}, conversation_id

    def process_query_results(answer_json):
        response_blocks = []
        if "query_description" in answer_json and answer_json["query_description"]:
            response_blocks.append(f"**Descrição da Consulta:** {answer_json['query_description']}")
        if "sql" in answer_json:
            with st.expander("SQL gerado pelo Genie"):
                st.code(answer_json["sql"], language="sql")
        if "columns" in answer_json and "data" in answer_json:
            columns = answer_json["columns"]
            data = answer_json["data"]
            if isinstance(columns, dict) and "columns" in columns:
                col_names = [col["name"] for col in columns["columns"]]
                df = pd.DataFrame(data["data_array"], columns=col_names)
                st.markdown("**Resultados da Consulta:**")
                st.dataframe(df)
        elif "message" in answer_json:
            st.markdown(answer_json["message"])
        else:
            st.info("Sem resultados retornados.")
        for block in response_blocks:
            st.markdown(block)

    user_input = st.chat_input("Faça uma pergunta para Genie...")

    if user_input:
        st.chat_message("user").markdown(user_input)
        with st.chat_message("assistant"):
            with st.spinner("Consultando Genie..."):
                answer_json, new_conversation_id = ask_genie_sync(user_input, genie_space_id, conversation_id)
                st.session_state["genie_conversation_id"] = new_conversation_id
                process_query_results(answer_json)

# --- Detalhes Page ---
elif menu == "Detalhes":
    st.header("Detalhes")
    data = getData()
    st.dataframe(data=data, height=600, use_container_width=True)