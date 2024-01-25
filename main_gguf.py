from llama_cpp import Llama
import json
# import copy
import re
import pandas as pd
import sqlite3
import getopt
import sys

def fetchSchema(db):
    """
    Get database's schema, which is a dict with table name as key
    and list of column names as value
    :param db: database path
    :return: schema dict
    """
    schema = {}
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # fetch table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [str(table[0].lower()) for table in cursor.fetchall()]

    # fetch table info
    for table in tables:
        cursor.execute("PRAGMA table_info({})".format(table))
        schema[table] = [str(col[1].lower()) for col in cursor.fetchall()]

    st = ""
    for key in schema:
        st += key + " : " + str(schema[key]) + "\n"
    # print(st)
    return st

model_name = ''
test_set_name = ''
schema_on = False

argv = sys.argv[1:]
opt = "hm:t:s"
long_options = ["model=", "test_set=", "schema_on"]

try:
    opts, args = getopt.getopt(argv, opt, long_options)
except getopt.GetoptError:
    print('script.py -m <model_name> -t <test_set_name> -s')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print('script.py -m <model_name> -t <test_set_name> -s')
        sys.exit()
    elif opt in ("-m", "--model"):
        model_name = arg
    elif opt in ("-t", "--test_set"):
        test_set_name = arg
    elif opt in ("-s", "--schema_on"):
        schema_on = True

model_path = model_name + ".gguf"
if schema_on:
    csv_file_name = "results/" + model_path + "with_schema.csv"
else: csv_file_name = "results/" + model_path + "without_schema.csv"
db_path = "spider/database/"
llm = Llama(model_path=model_path)
print("model loaded")

f = open(test_set_name)
data = json.load(f)

df = pd.DataFrame(columns = ["Question","Query Gold","Query Generated"])

template = "Question: Convert the following text statement to sqlite query: " 
i=1
for item in data:
    
    temp = [item['question'],item['query']]
    db_path = db_path + "{}/{}.sqlite".format(item['db_id'],item['db_id'])
    schema = fetchSchema(db_path)
    output = llm(
        # "Question: Convert the following text statement to sqlite query : display all names of students whose marks are above average of all marks of students. Answer:",
        prompt= template + item['question'] + "The schema is given by :{}\nAnswer:".format(schema),
        max_tokens=300,
        temperature=0.1,
        stop=["Explanation:"], 
        echo=True
    )
    # print(json.dumps(output,indent=2))
    response = output["choices"][0]["text"]
    # print(response + "\n")
    match = re.search("SELECT .*",response,re.DOTALL)
    if(match):  
        print("match")
        temp.append(match.group(0))
    else:   temp.append("NULL")
    df.loc[len(df)] = temp
    i+=1
    if i==3: break
    # print(i)
df.to_csv(csv_file_name)



