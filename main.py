from sendToRaw.downloadFile import download, get_clima
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
    get_clima()

    process_consumo_aparelho()
    process_pld()
    process_dado_clima()
