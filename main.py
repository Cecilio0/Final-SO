# Para lambda
# python3 -m venv venv
# source venv/bin/activate
# pip3 install -r requirements.txt
# 1. pip3 install -t dependencies -r requirements.txt
# 2. (cd dependencies; zip ../aws_lambda_artifact.zip -r .)
# 3. zip aws_lambda_artifact.zip -u main.py
from mangum import Mangum
from fastapi import FastAPI, UploadFile
import psycopg2
import boto3

s3 = boto3.client('s3',
                  aws_access_key_id='',
                  aws_secret_access_key='')
 
bucket_name = ""
       
conn = psycopg2.connect(database = "",
                        user = "",
                        host= '',
                        password = "",
                        port = 5432)

app=FastAPI()
handler=Mangum(app)
    

@app.get("/rds/get")
async def get(dbName: str):
    cur = conn.cursor()
    query = "SELECT * FROM " + dbName
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    return rows

@app.post("/s3/save")
async def save(file: UploadFile):
    s3.put_object(Bucket=bucket_name, Key=f"{file.filename}", Body=file.file.read())
    return {"status": "ok"}

    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0" , port=8000)