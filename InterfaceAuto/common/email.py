"""
邮件类。用来给指定用户发送邮件。可指定多个收件人，可带附件。
"""
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import error,gaierror
import logging.config
from AppAuto.common.data_handle import PATH
# logging.config.fileConfig(PATH("data\\log_config.ini"))
# mylogger=logging.getLogger("main")

class Email:
    def _attach_file(self,att_file,msg):
        att=MIMEText(open(att_file,"rb").read(),"html","utf-8")
        file_name=re.split(r"[\\|/]",att_file)
        att["Content-Disposition"]='attachment_path;filename="%s'%file_name[-1]
        msg.attach(att)
        # mylogger.info("attach file")

    def send_email(self,email_config_info):
        server=email_config_info["server"]
        sender=email_config_info["sender"]
        password = email_config_info["password"]
        receiver=email_config_info["receiver"]
        title=email_config_info["title"]
        message=email_config_info["message"]
        attachment_path=email_config_info.get("attachment_path")


        msg = MIMEMultipart("related")
        msg["Subject"] =title
        msg["From"]=sender
        msg["To"]=";".join(receiver)

        #邮件正文
        if message:
            msg.attach(MIMEText(message))

        #邮件附件
        if attachment_path:
            if isinstance(attachment_path,list):
                for f in attachment_path:
                    self._attach_file(f,msg)
            elif isinstance(attachment_path,str):
                self._attach_file(attachment_path,msg)

        #连接服务器发生
        try:
            smtp_server=smtplib.SMTP()
            smtp_server.connect(server)
        except (gaierror or error) as e:
            # mylogger.exception()
            print("发送邮件失败，无法连接到SMTP服务器，检查网络及SMTP服务器.%s",e)
        else:
            try:
                smtp_server.login(sender,password)
            except smtplib.SMTPAuthenticationError as e:
                # mylogger.exception("用户名、密码验证失败！%s",e)
                print("用户名、密码验证失败！%s",e)
            else:
                try:
                    smtp_server.sendmail(sender,receiver,msg.as_string())
                except smtplib.SMTPSenderRefused:
                    # mylogger.error()
                    print("xxx")
            finally:
                smtp_server.quit()




