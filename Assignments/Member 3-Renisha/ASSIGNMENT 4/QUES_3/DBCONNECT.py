import ibm_db
conn=ibm_db.connect('DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA (1).crt;UID=mcb20916;PWD=iAPZMikUQf6agwXY','','')
sql="select * from information"
ibm_db.execute(stmt)
account=ibm_db.fetch_assoc(stmt)
print(account)