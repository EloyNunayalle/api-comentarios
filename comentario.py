import boto3
import uuid
import os
import json                              
from datetime import datetime

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    nombre_tabla = os.environ["TABLE_NAME"]
    bucket_name = os.environ["BUCKET_NAME"]

    # Proceso
    uuidv1 = str(uuid.uuid1())
    fecha = datetime.utcnow().isoformat()
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
          'texto': texto
        }
    }
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    response = table.put_item(Item=comentario)

    # Guardar comentario como archivo JSON en S3               
    s3 = boto3.client('s3')                                   
    key = f"{tenant_id}/{uuidv1}_{fecha}.json"               
    s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(comentario))  

    # Salida (json)
    print(comentario)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'response': response
    }

