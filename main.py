from sendToRaw import download, download_specific_zip_file
from cleaning.localCleaningFile import process_consumo_aparelho, process_pld, process_dado_clima

if __name__ == "__main__":
    download(
        "https://igce.rc.unesp.br/Home/ComissaoSupervisora-old/ConservacaodeEnergiaCICE/tabela_consumo.pdf",
        "consumoAparelho.pdf"
    )
    download(
        "https://pda-download.ccee.org.br/korJMXwpSLGyVlpRMQWduA/content",
        "horarioPrecoDiff.csv"
    )
    download_specific_zip_file(
        "https://portal.inmet.gov.br/uploads/dadoshistoricos/2025.zip",
        "INMET_SE_SP_A771_SAO PAULO - INTERLAGOS_01-01-2025_A_31-08-2025.CSV"
    )

    process_consumo_aparelho()
    process_pld()
    process_dado_clima()
