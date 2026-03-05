# main.py
import os, json, base64
import pandas as pd

def get_pdf_base64(pdf_path):
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    return f"data:application/pdf;base64,{base64_pdf}"


# --- 0) Load CSV ---
from langchain_aws import BedrockEmbeddings
import boto3
import botocore
from langchain_aws import ChatBedrock, ChatBedrockConverse
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.utils.math import cosine_similarity
import os
import pickle
import pandas as pd
import deadlies
from dataclasses import dataclass, field
from typing import List, Any

CSV_FILE = ""
EMBEDDING_FILE = ""
emb_model = BedrockEmbeddings(region_name="us-east-1", model_id = "amazon.titan-embed-text-v2:0")
BUCKET_NAME = "claimlens-content-storage-uidev2"

@dataclass
class agent_executor():
    executor: Any = ""

aex = agent_executor()

@dataclass
class cols():
    col_names: List[str] = field(default_factory=list)
    descr_col: str = ""
    incurred_col : str = ""

c = cols()

def sanitize_columns():
    
    if df is None or df.empty:
        raise ValueError("ERROR: DataFrame 'df' is empty. Call ask_agent() before this method.")

    # 1. --- SANITIZE COLUMNS ---
    df.columns = (
        df.columns.str.strip()
        .str.replace("\n", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True)
    )
    print("Sanitized columns:", df.columns.tolist())
    # 2. --- Detect schema based on sanitized names ---
    if {"Claim Number", "Incident Description", "Paid Expense", "Total Incurred"}.issubset(df.columns):
        c.col_names = ["Claim Number", "Incident Description", "Paid Expense", "Total Incurred"]
        c.descr_col = c.col_names[1]
        c.incurred_col = "Total Incurred"
    else:
        c.col_names = ["Claim Number", "Injury Description", "Total Payments", "Total Incurred"]
        c.descr_col = c.col_names[1]
        c.incurred_col = "Total Incurred"

def get_xlsx_std_cols(bucket: str, fname: str):

    print("Looking up for xlsx std col names..")
    s3 = boto3.client("s3")

    json_filename = fname.replace(".csv", ".json")
    # try:
    #     s3_object = s3.get_object(Bucket=bucket, Key=json_filename)
    # except s3.exceptions.NoSuchKey:
    #     print("No std columns json file found. The file could be non-XLSX")
    #     return {}
    try:
        with open(json_filename, 'r') as f:
            cols_mapping = json.load(f)
    except FileNotFoundError as e:
        print(f"Didnt find json file - {e}")
        return {}
    print(cols_mapping)

    rev_map = {v: k for k, v in cols_mapping.items()}

    return rev_map
# --- 1) Define tools ---
from langchain_core.tools import tool

# === EDA tools ===
def get_df_w_medical_conditions(df, medical_conditions: list) -> str:
    """Returns list of all matching medical conditions records along with paid and total incurred."""
    # title_dict = {}
    # # df_rows = []
    # with open(EMBEDDING_FILE, 'rb') as pkl:
    #     title_dict = pickle.load(pkl)
    # if "Loss Run" in CSV_FILE:
    #     col_names = ["Claim Number", "Incident Description", " Paid\nExpense ", " Total\nIncurred "]
    #     incurred_col = " Total\nIncurred "
    # # else:
    # #     col_names = ["Claim Number", "In Description", "Incurred"]
    # #     incurred_col = "Incurred"
    # df_filtered = pd.DataFrame(columns=col_names)
    # for query in medical_conditions:
    #     # query = medical_condition
    #     print(query)
    #     emb_query = emb_model.embed_query(query)
    #     sim = cosine_similarity([emb_query], title_dict["embeddings"])

    #     print(max(sim[0]), sim[0].argmax())
    #     print(title_dict["titles"][sim[0].argmax()])

    #     matches = sorted([(title_dict["titles"][i], sim[0][i]) for i in range(len(title_dict["titles"]))], key=lambda x: x[1], reverse=True)[:100]
    #     # print(matches[29])
    #     for match in matches:
    #         if match[1] > 0.2:
    #             df1 = df.loc[df[col_names[1]] == match[0], col_names]
    #             df_filtered = pd.concat([df_filtered, df1], ignore_index=True)
    #             df_filtered.drop_duplicates(subset="Claim Number", inplace=True)
    if df is None or df.empty:
        raise ValueError("ERROR: DataFrame 'df' is empty. Call ask_agent() before this method.")

    df_filtered = pd.DataFrame(columns=c.col_names)
    for query in medical_conditions:
        # query = medical_condition
        print(query)
        if search_cat:
            kw_list = get_keywords_for_query(query)
        else:
            kw_list = []
        print(f"Keyword List for {query} - {kw_list}")
        if kw_list:
            joined_conditions = "|".join(kw_list)
        else:
            joined_conditions = query
        print(joined_conditions)
        df1 = df.loc[df[c.descr_col].str.contains(joined_conditions, case = False), c.col_names]
        print(df1)
        df_filtered = pd.concat([df_filtered, df1], ignore_index=True)
        if 'Claim Number' in df.columns and kw_list:
            # df_filtered.drop_duplicates(subset="Claim Number", inplace=True)
            df_filtered.drop_duplicates(inplace=True)
    
    return df_filtered

def get_keywords_for_query(query: str) -> list:
    
    if query is not None and query in deadlies.sins:
        return deadlies.sins[query]
    
    return []

def get_filtered_df_stats():
    
    df_rows = []
    counts = {}
    
    incurred_col = c.incurred_col
    df_filtered[incurred_col] = df_filtered[incurred_col].apply(pd.to_numeric)
    df_filtered.sort_values(by=[incurred_col], ascending=False, inplace=True)
    df_filtered_sum = df_filtered[incurred_col].sum()
    if not df_filtered.empty:
        df_filtered_top = df_filtered[incurred_col].nlargest()
        counts["Top 5 claims of Total Incurred "] = df_filtered_top.to_json(orient="records")
    df_filtered_count = int((df_filtered[incurred_col] != 0).sum())
    df_rows = df_filtered.to_json(orient="records")
    counts["Total number of records"] = int(df_filtered.shape[0])
    counts["Count of non-zero Total Incurred"] = df_filtered_count
    counts["Sum of Total Incurred"] = int(df_filtered_sum)
    
    return df_rows, counts
  
@tool
def get_records_incurred_and_medical_conditions(medical_conditions: list, min_value: int, max_value:int) -> (str, str):
    """Returns list of matching medical conditions above or below a certain incurred amount."""
    global df_filtered
    print(f"Calling get_records_incurred_and_medical_conditions {medical_conditions}, {min_value}, {max_value}")
    
    df_rows = []
    counts = {}
    
    sanitize_columns()
    #  Remove " - " entries
    # df_sub = df.loc[df[c.incurred_col].str.contains("\\d", regex=True), c.col_names]
    
    # # Remove commas and convert to numeric
    # s = pd.to_numeric(df_sub[c.incurred_col].str.replace(",", ""), errors='coerce')

    if min_value is not None and max_value is not None:
        df_slice = df.loc[df[c.incurred_col].between(min_value, max_value), c.col_names]
    
    print(df_slice)

    df_filtered = get_df_w_medical_conditions(df_slice, medical_conditions)

    df_rows, counts = get_filtered_df_stats()
    
    print(counts)
    
    return json.dumps(df_rows), json.dumps(counts)
@tool
def get_records_for_total_incurred_range(min_value: int, max_value: int) -> (str, str):
    """Returns list of all matching records for a given amount range."""
    global df_filtered
    print(f"Calling get_records_for_total_incurred_range {min_value}, {max_value}")

    sanitize_columns()
    # #  Remove " - " entries
    # df_sub = df.loc[df[c.incurred_col].str.contains("\\d", regex=True), c.col_names]
    # # Remove commas and convert to numeric
    # s1 = pd.to_numeric(df_sub[c.incurred_col].str.replace(",", ""), errors='coerce')

    if min_value is not None and max_value is not None:
        df_filtered = df.loc[df[c.incurred_col].between(min_value, max_value), c.col_names]
        # df_filtered = pd.concat([df_filtered, df_great], ignore_index=True

    print(df_filtered)
    df_rows = df_filtered.to_json(orient="records")
    df_filtered_sum = df_filtered[c.incurred_col].sum()
    # print(df_rows)

    return json.dumps(df_rows), f"Sum of Total Incurred - {df_filtered_sum}"
@tool
def get_records_for_medical_conditions(medical_conditions: list) -> (str, str, str) :
    """Returns list of all matching medical conditions records and sum of total incurred."""
    global df_filtered
    print(f"Calling get_records_for_medical_conditions {medical_conditions}")
    title_dict = {}
    df_rows = []
    with open(EMBEDDING_FILE, 'rb') as pkl:
        title_dict = pickle.load(pkl)
    if "Loss Run" in CSV_FILE:
        col_names = ["Claim Number", "Incident Description", " Paid\nExpense ", " Total\nIncurred "]
        incurred_col = " Total\nIncurred "
    else:
        col_names = ["Claim Number", "Injury Description", "Incurred"]
        incurred_col = "Incurred"
    df_filtered = pd.DataFrame(columns=col_names)
    counts = {}
    for query in medical_conditions:
        df_concat = pd.DataFrame(columns=col_names)
        # query = medical_condition
        print(query)
        emb_query = emb_model.embed_query(query)
        sim = cosine_similarity([emb_query], title_dict["embeddings"])

        print(max(sim[0]), sim[0].argmax())
        print(title_dict["titles"][sim[0].argmax()])

        matches = sorted([(title_dict["titles"][i], sim[0][i]) for i in range(len(title_dict["titles"]))], key=lambda x: x[1], reverse=True)[:100]
        # print(matches[29])
        kw_list = get_keywords_for_query(query)
        for match in matches:
            if match[1] > 0.2:
                # df1 = df.loc[df[col_names[1]] == match[0], col_names]
                df1 = df.loc[df[col_names[1]] == match[0], col_names]
                df_concat = pd.concat([df_concat, df1], ignore_index=True)
                df_concat.drop_duplicates(subset="Claim Number", inplace=True)
                # print(df1)
        counts[query] = df_concat.shape[0]
        df_filtered = pd.concat([df_filtered, df_concat], ignore_index=True)
        df_filtered.drop_duplicates(subset="Claim Number", inplace=True)
        print(df_concat.shape[0], df_filtered.shape[0])
    df_filtered.index += 1


    df_filtered_sum = df_filtered[incurred_col].sum()
    df_rows = df_filtered.to_json(orient="records")
    counts["Total records"] = df_filtered.shape[0]
    counts["Sum Total Incurred"] = df_filtered_sum
    print(counts)

    return json.dumps(df_rows), json.dumps(counts)#, f"Sum of Total Incurred - {df_filtered_sum}"
@tool
def get_records_with_medical_conditions(medical_conditions: list) -> (str, str) :
    """Returns list of all matching medical onditions records and sum of total incurred."""
    global df_filtered
    print(f"Calling get_records_with_medical_conditions {medical_conditions}")
    # title_dict = {}
    df_rows = []
    counts = {}
    
    sanitize_columns()
    
    df_filtered = get_df_w_medical_conditions(df, medical_conditions)
    
    print(df_filtered[c.incurred_col].head())
    # s = pd.to_numeric(df_filtered[c.incurred_col].str.replace(",", ""), errors='coerce')

    df_rows, counts = get_filtered_df_stats()
    
    # print(counts)

    return json.dumps(df_rows), json.dumps(counts)

@tool
def get_summary_all_records() -> (str, str) :
    """Returns list and summary of all records and sum of total incurred."""
    global df_filtered
    # title_dict = {}
    df_rows = []
    counts = {}
    
    sanitize_columns()
    
    df_filtered = df[c.col_names]
    
    print(df_filtered[c.incurred_col].head())
    # s = pd.to_numeric(df_filtered[c.incurred_col].str.replace(",", ""), errors='coerce')

    df_rows, counts = get_filtered_df_stats()
    
    # print(counts)

    return json.dumps(counts)
# --- 2) Wire up tools for LangChain ---
tools = [
    get_records_for_total_incurred_range,
    get_records_with_medical_conditions,
    get_records_incurred_and_medical_conditions,
    get_summary_all_records,
]

# --- 3) Configure LLM ---

def configure_agent(creds: dict):
    config = botocore.config.Config(
        read_timeout=900, connect_timeout=900, retries={"max_attempts": 0}
    )
    bedrock_client = boto3.client(
        service_name="bedrock-runtime", region_name="us-east-1", config=config
    )

    modelId = 'us.anthropic.claude-3-5-sonnet-20241022-v2:0'
    # modelId = 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'
    # model_id = 'openai.gpt-oss-120b-1:0'

    llm = ChatBedrockConverse(
        model_id=modelId,
        region_name="us-east-2",
        max_tokens=2000,
        aws_access_key_id=creds["aws_access_key"],
        aws_secret_access_key=creds["aws_secret_key"],
        aws_session_token=creds["aws_session_token"],
    )

    # --- 4) Narrow policy/prompt (agent behavior) ---

    SYSTEM_PROMPT = (
        "You are a data-focused assistant. "
        "If a question requires information from the CSV, first use an appropriate tool. "
        "Use only one tool call per step if possible. "
        "Don't try to do total count or breakdown of records, use the numbers in the provided output. "
        "You can provide Sum of Total Incurred if relevant. "
        "Answer concisely and in a structured way. "
        "If no tool fits the user query, just respond that you cannot answer, and NEVER list available tools in your response.\n\n"
        "Available tools:\n{tools}\n"
        "Use only these tools: {tool_names}."
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    _tool_desc = "\n".join(f"- {t.name}: {t.description}" for t in tools)
    _tool_names = ", ".join(t.name for t in tools)
    prompt = prompt.partial(tools=_tool_desc, tool_names=_tool_names)

    # --- 5) Create & run tool-calling agent ---

    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    aex.executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,   # optional: True for debug logs
        max_iterations=3,
    )
    
    return
    

# --- Public API ---
def ask_agent(query: str,  use_cat: bool, filename: str) -> str:
    """Backward-compatible: text-only answer (for mini_eval etc.)."""

    global df_filtered, df, EMBEDDING_FILE, CSV_FILE, search_cat
    
    df_filtered = pd.DataFrame()

    CSV_FILE = filename
    EMBEDDING_FILE = os.path.splitext(CSV_FILE)[0] + ".pickle"
    search_cat = use_cat
    
    print(f"Loading CSV file: {CSV_FILE} and embedding file: {EMBEDDING_FILE}")
    df = pd.read_csv(CSV_FILE)
    #CSV_FILE = "Loss Run.xlsx"
    #df = pd.read_excel(CSV_FILE)
    sanitize_columns()
    cols_map = get_xlsx_std_cols(BUCKET_NAME, CSV_FILE)
    if cols_map:
        # If std cols map is present, rename col names. It is set for XLSX files.
        df = df.rename(columns=cols_map)
        # print(df.columns)
    
    out = aex.executor.invoke({"input": query})["output"]
    
    return out, df_filtered


if __name__ == "__main__":
    # Example that will definitely trigger a response:
    demo_q = "Get me records for Liver Transplant with death and their total paid expenses."
    text = ask_agent(demo_q)
    print("\n=== AGENT ANSWER ===")
    print(text)
