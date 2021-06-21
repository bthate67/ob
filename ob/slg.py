# This file is placed in the Public Domain

txt = "OTP-CR-117/19 otp.informationdesk@icc-cpi.int http://genocide.rtfd.io confessed"

def register(k):
    k.addcmd(slg)

def slg(event):
    event.reply(txt)