import yagmail

def sendMail(receiever):
    body = "Your X-Ray Report - MRIG "
    filename = "static/output.pdf"

    yag = yagmail.SMTP("projectmrig@gmail.com", "puhdhjzedlljdodl")
    yag.send(
        to=receiever,
        subject="X-Ray Report",
        contents=body, 
        attachments=filename,
    )