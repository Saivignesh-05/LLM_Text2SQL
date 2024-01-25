import json
import re
import google.generativeai as palm
import pandas as pd
import getopt,sys

test_set_name = ''
schema_on = False

try:
    opts, args = getopt.getopt(argv, "ht:s", ["test_set=", "schema_on"])
except getopt.GetoptError:
    print('script.py -t <test_set_name> -s')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print('script.py -t <test_set_name> -s')
        sys.exit()
    elif opt in ("-t", "--test_set"):
        test_set_name = arg
    elif opt in ("-s", "--schema_on"):
        schema_on = True

# Now you can use model_name, test_set_name, and schema_on in your script

palm.configure(api_key='AIzaSyCtgDN2xBVB2fLINckHC94V6eqmt3KcijU')

if schema_on:
    csv_file_name = "results/Palm/with_schema.csv"
else: csv_file_name = "results/Palm/without_schema.csv"

f = open(test_set_name)
data = json.load(f)

df = pd.DataFrame(columns = ["Question","Query Gold","Query Generated"])

template = "Question: Convert the following text statement to sqlite query: " 
i=1
for item in data:
    try:
        temp = [item['question'],item['query']]
        schemaPath = "./spider/database/{}/schema.sql".format(item['db_id'])
        # print(schema)
        output = palm.generate_text(prompt= (template + item['question']))
        # print((template + item['question'] + "The schema is given by : " + schema))
        response = output.result
        # print(response + "\n")
        match = re.search("SELECT .*",response,re.DOTALL)
        if(match):  
            print("match")
            temp.append(match.group(0))
        else:   temp.append("NULL")
        df.loc[len(df)] = temp
        i+=1
        # if i==30: break
        print(i)
    except: continue
df.to_csv(csv_file_name)










# stream = output = llm(
#     "Question: Convert the following text statement to sqlite3 query : display all names of students whose marks are above average of all marks of students. Answer:",
#     max_tokens=100,
#     temperature=0.1,
#     stop=["\n","Question","Q:"],
#     echo=True,
#     # stream=True
# )
# for output in stream:
#     fragment = copy.deepcopy(output)
#     print(fragment["choices"][0]["text"])



