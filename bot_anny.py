import logging
import pytesseract
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from pdf2image import convert_from_path # <-- Nova biblioteca importada
import os # <-- Usado para gerenciar arquivos

# --- CONFIGURAÇÕES DO SEU BOT ---
TOKEN = "7848678591:AAG6PHNuKpb6ZCgZ4M-6lnvqWwQKdNBFfF0" 

# --- DADOS DE PAGAMENTO ---
CHAVE_PIX = "8e7fc37c-634d-4408-9e81-3fbea689d8b2"
VALOR_ESPERADO_COMPLETO = "25,00"
VALOR_ESPERADO_CURTO = "25"
NOME_RECEBEDOR_ESPERADO = "Wandeson Conceicao dos Santos"
LINK_GRUPO = "https://t.me/+eG1u4tHDvzRkYWNh"

# --- CAMINHOS DOS PROGRAMAS ---
CAMINHO_TESSERACT = r'C:\Users\Wanderson\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
# ATENÇÃO: Coloque aqui o caminho para a pasta bin do Poppler que você extraiu
CAMINHO_POPPLER = r'C:\poppler-24.08.0\Library\bin' 

# --- CONFIGURAÇÃO BÁSICA ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
pytesseract.pytesseract.tesseract_cmd = CAMINHO_TESSERACT

# --- FUNÇÕES DO BOT ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia a mensagem de boas-vindas."""
    mensagem = (
        "👋 Olá! Seja bem-vindo.\n\n"
        "Para ter acesso ao conteúdo exclusivo, é necessário realizar o pagamento via Pix.\n\n"
        f"💸 Valor: R$ {VALOR_ESPERADO_COMPLETO}\n"
        f"🔢 Chave Pix: {CHAVE_PIX}\n"
        "📄 Descrição: Acesso Premium - PRIVADO DA ANNY\n\n"
        "Após o pagamento, envie o comprovante (imagem ou PDF) aqui mesmo para validarmos e liberarmos seu acesso."
    )
    await update.message.reply_text(mensagem)

async def processar_e_validar_comprovante(caminho_arquivo_imagem: str, update: Update):
    """Função central que lê uma imagem e valida o conteúdo."""
    try:
        texto_comprovante = pytesseract.image_to_string(Image.open(caminho_arquivo_imagem), lang='por').lower()
        logger.info(f"Texto extraído do comprovante: {texto_comprovante}")

        nome_encontrado = NOME_RECEBEDOR_ESPERADO.lower() in texto_comprovante
        valor_encontrado = (f"r${VALOR_ESPERADO_CURTO}" in texto_comprovante.replace(" ", "") or
                            f" {VALOR_ESPERADO_CURTO}," in texto_comprovante or
                            f" {VALOR_ESPERADO_CURTO}." in texto_comprovante)

        if valor_encontrado and nome_encontrado:
            mensagem_sucesso = (
                "✅ Pagamento confirmado!\n\n"
                "Clique no link abaixo para acessar o conteúdo exclusivo:\n\n"
                f"🔗 [Acessar Grupo/PRIVADO DA ANNY]({LINK_GRUPO})"
            )
            await update.message.reply_text(mensagem_sucesso, parse_mode="Markdown")
        else:
            debug_message = f"Debug: Nome encontrado? {nome_encontrado}. Valor encontrado? {valor_encontrado}."
            logger.info(debug_message)
            await update.message.reply_text(
                f"❌ Não conseguimos validar seu comprovante automaticamente.\n\n"
                f"Verifique se o valor (R$ {VALOR_ESPERADO_COMPLETO}) e o nome do destinatário ({NOME_RECEBEDOR_ESPERADO}) estão visíveis no arquivo. Se o erro persistir, aguarde um administrador."
            )
    except Exception as e:
        logger.error(f"Ocorreu um erro na função de OCR: {e}")
        await update.message.reply_text("Ocorreu um erro grave ao ler o arquivo. Tente novamente ou aguarde um administrador.")
    finally:
        # Limpa o arquivo de imagem após o uso
        if os.path.exists(caminho_arquivo_imagem):
            os.remove(caminho_arquivo_imagem)


async def receber_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe um comprovante enviado como FOTO."""
    await update.message.reply_text("Analisando sua imagem, aguarde um instante...")
    photo_file = await update.message.photo[-1].get_file()
    caminho_para_salvar = "comprovante.jpg"
    await photo_file.download_to_drive(caminho_para_salvar)
    await processar_e_validar_comprovante(caminho_para_salvar, update)

async def receber_documento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe um comprovante enviado como ARQUIVO (imagem ou PDF)."""
    documento = update.message.document
    caminho_para_salvar = documento.file_name
    file = await documento.get_file()
    await file.download_to_drive(caminho_para_salvar)

    if documento.mime_type == 'application/pdf':
        await update.message.reply_text("Recebemos seu PDF. Convertendo para imagem, aguarde...")
        try:
            # Converte o PDF para imagem
            imagens_do_pdf = convert_from_path(caminho_para_salvar, poppler_path=CAMINHO_POPPLER)
            caminho_imagem_convertida = "comprovante_from_pdf.jpg"
            imagens_do_pdf[0].save(caminho_imagem_convertida, 'JPEG')
            
            # Limpa o arquivo PDF original
            os.remove(caminho_para_salvar)
            
            # Chama a função de validação
            await processar_e_validar_comprovante(caminho_imagem_convertida, update)
        except Exception as e:
            logger.error(f"Erro ao converter PDF: {e}")
            await update.message.reply_text("Não foi possível processar o arquivo PDF.")
    elif "image" in documento.mime_type:
        await update.message.reply_text("Analisando seu arquivo de imagem, aguarde...")
        await processar_e_validar_comprovante(caminho_para_salvar, update)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, receber_foto))
    # Novo handler para receber documentos (PDFs e imagens como arquivo)
    app.add_handler(MessageHandler(filters.Document.ALL, receber_documento))

    print("Bot está rodando com suporte a Imagens e PDFs! Pressione Ctrl+C para parar.")
    app.run_polling()