import os # for file or folder operation
import subprocess # to run libre office from python
from telegram import Update #teh library i installed using pip
from telegram.ext import Application, MessageHandler ,filters, ContextTypes
import asyncio




from dotenv import load_dotenv
load_dotenv()
Token = os.getenv("Token")
download_folder = "downloads" # a folder where we temporarly store docx file

os.makedirs(download_folder, exist_ok=True)#creates the folder if it doesnt exist 




app =Application.builder().token(Token).build()


async def handle_document(update, context):
    nfile = update.message.document.file_name
    
    if not nfile.endswith(".docx"):
        await update.message.reply_text("please send a .docx file only!")
        return

    await update.message.reply_text("File received!\nConverting...")
    
    docx_path = f"{download_folder}/{nfile}"
    file = await context.bot.get_file(update.message.document.file_id)
    await file.download_to_drive(docx_path)

    subprocess.run([
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", download_folder,
        docx_path
    ])
    
    pdf_path = docx_path.replace(".docx", ".pdf")
    await update.message.reply_document(document=open(pdf_path, "rb"))
    os.remove(docx_path)
    os.remove(pdf_path)
    

async def handle_text(update , context):
    await update.message.reply_text("just send the docx file!")

app.add_handler(MessageHandler(filters.Document.ALL,handle_document))
app.add_handler(MessageHandler(filters.TEXT,handle_text))
app.run_polling()






#taskkill /F /IM python.exe