import smtplib

def send_mail(msg, emails):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("tifmrp1324ip@gmail.com", "wussgood$$$")
	for email in emails:
		server.sendmail("tifmrp1324ip@gmail.com", email, msg)
	server.quit() 