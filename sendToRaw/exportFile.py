import boto3
import os

def send_to_s3(local_folder, bucket_name='bucket-teste', s3_prefix='arquivos/'):
  s3 = boto3.client('s3')
  
  if not os.path.exists(local_folder):
    print(f"Pasta local {local_folder} não existe.")
    return
  
  try:
    for filename in os.listdir(local_folder):
      local_path = os.path.join(local_folder, filename)
      if os.path.isfile(local_path):
        s3_key = os.path.join(s3_prefix, filename) if s3_prefix else filename
        s3.upload_file(local_path, bucket_name, s3_key)
        print(f"Enviado {local_path} para s3://{bucket_name}/{s3_key}")
  except Exception as e:
    print(f"Erro ao enviar pasta para S3: {e}")

# Example usage
if __name__ == "__main__":
  send_to_s3("./sendToRaw/files")