from smtplib import SMTP
import datetime as dt 
import time
import ssl

passw="pchc maro cwnw mvby"
sender="jashpalbhatti201282@gmail.com"
p=587
ss="smtp.gmail.com"
def email(start,end,rec,des):
    msg=f"""Hello your event "{des}" is scheduled at
    {start} to {end}
    """
    context=ssl.create_default_context()
    with SMTP(ss,p) as email:
        email.starttls(context=context)
        email.login(sender,passw)
        email.sendmail(sender,rec,msg)
        print("Email sent")