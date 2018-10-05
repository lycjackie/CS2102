import random
import string

def random_char(y):
	return ''.join(random.choice(string.ascii_letters) for x in range (y)) 

flavor = ['Funghi','Diavola','Hawaiian','Beef','Cheesy']
query = """
INSERT INTO "E0248110"."SELLS" (RNAME, PIZZA, PRICE) VALUES ('{}', '{}', '{}');
"""

q1 = """
INSERT INTO "E0248110"."LIKES" (CNAME, PIZZA) VALUES ('{}', '{}');
"""

q2 = """
INSERT INTO "E0248110"."RESTAURANTS" (RNAME, AREA) VALUES ('{}', '{}');
"""

Area = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','SG','MY','TW','US']

customer = ['Jackie','CH','Ben','Bel','JH']

# random.randint(0,4)

res = ['R1','R2','R3','R4','R5']

rname = "ASD,BCEPr,BnQvn,BqydS,DgXAE,EXzbc,Emksr,FAinz,FRaXc,Fyyri,GllOh,HeaGr,IZdwA,IoTdy,IvsUk,KlMLE,MsnSG,OSSLe,OcMbB,PAUts,PRdgk,PZlAp,PrYFN,QqsnD,R1,R2,R3,R4,R5,RwoTV,SkBSw,TfFcv,USybA,WXeqL,aFkNH,aItiD,aeaDg,ajyey,cdlyr,dDkBt,doFCl,efyes,hjPwV,iDEGS,iIdtM,jvuCD,lNYku,sdjOT,tXFSm,vMgrQ,vNDTn,vRJSR,vWdhx,vwRlU,xXAog,zCmc"
l = rname.split(',')

for i in range(100):
	print(query.format(l[random.randint(0,len(l)-1)],flavor[random.randint(0,4)],random.randint(5,10)))







