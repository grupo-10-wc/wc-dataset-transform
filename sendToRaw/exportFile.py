import boto3
import os
import downloadFile as downloadFile
from dotenv import load_dotenv

load_dotenv()

def send_to_s3(local_folder, bucket_name='wc-data-teste', s3_prefix='arquios/'):
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
        region_name=os.getenv('AWS_DEFAULT_REGION')
    )
    

    if not os.path.exists(local_folder):
        print(f"Pasta local {local_folder} não existe.")
        return False
    
    try:
        uploaded_files = 0
        for filename in os.listdir(local_folder):
            local_path = os.path.join(local_folder, filename)
            
            
            if os.path.isfile(local_path):
               s3_key = f"{s3_prefix}{filename}" if s3_prefix else filename
               s3_client.upload_file(local_path, bucket_name, s3_key)
               print(f"Enviado {local_path} para s3://{bucket_name}/{s3_key}")
               uploaded_files += 1
        
        print(f"Upload concluído! {uploaded_files} arquivo(s) enviado(s).")
        return True
        
    except Exception as e:
        print(f"Erro ao enviar pasta para S3: {e}")
        return False

if __name__ == "__main__":
    downloadFile.download("https://igce.rc.unesp.br/Home/ComissaoSupervisora-old/ConservacaodeEnergiaCICE/tabela_consumo.pdf", "consumoAparelho.pdf")
    downloadFile.download("https://pda-download.ccee.org.br/korJMXwpSLGyVlpRMQWduA/content", "horarioPrecoDiff.csv")
    downloadFile.download_specific_zip_file("https://portal.inmet.gov.br/uploads/dadoshistoricos/2025.zip","INMET_SE_SP_A771_SAO PAULO - INTERLAGOS_01-01-2025_A_31-08-2025.csv")
    #send_to_s3("./sendToRaw/files")
