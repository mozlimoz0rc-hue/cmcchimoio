from flask import Flask, render_template, url_for,request,jsonify
import requests as req
import json
import cloudinary
import cloudinary.uploader


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import os

import random
import datetime

app = Flask(__name__)

# Configurar Cloudinary com suas credenciais
cloudinary.config(
    cloud_name='dhfytj5nq',
    api_key='144515411569918',
    api_secret='qvlOr_FAX61h61GzlkMig9W2p6w'
)



app = Flask(__name__)





def addproduto(nome,category,preco,descricao,image_url,n_artgo):
	
	fire_url = "https://bs-siteof-sell-default-rtdb.firebaseio.com/produtos/.json"
	
	
	num_artigo = n_artgo
	produto = {
			"nome": nome,
			"numero": num_artigo,
			"preco": preco,
			"category": category,
			"obse": descricao,
			"img_link": image_url,	
			}
	
	res = req.post(url =fire_url, data = json.dumps(produto) )
	
	
	print(res.text)
		
	
	

# simular o firebase


def my_banco_base(aba):
	rota = ""
	if aba == "p":
		rota = "/produtos"
	elif aba == "m":
		rota = "/mensagens"
	elif aba == "i":
		rota = "/interacoes"
	elif aba == "r":
		rota = "/reservas"
	
		
		
	
	url = "https://bs-siteof-sell-default-rtdb.firebaseio.com"+rota+"/.json"
	
	res = req.get(url)
	
	respo= res.json()
	return respo
	
	
	

def loadProd():
	#p significa que estou a requesitar somente produtos
	bancoBD = my_banco_base("p")
	
	
	
	linkimg = url_for('static', filename='imageProdut/carbrador.webp')
	
	
	
	prod = ""
	for i in bancoBD:
		
		produto = bancoBD[i]
		
		nome_prod = produto["nome"]
		preco_prod = produto["preco"]
		num_prod = produto["numero"]
		link_img = produto["img_link"]
		
		linkimg = link_img
		
		
		
		prod = prod + f"""
	<div class="box-sell swiper-slide">
		  <a href="/detalhes/{nome_prod+'_'+num_prod}">
          <img style="height: 50%;" src="{linkimg}" >
          <h5>{nome_prod}</h5>
          <p class="pna">artigo n°: 
          {num_prod}</p>
          <b><p>PRECO: {preco_prod} MTN</p></b>
          <button>comprar peca</button>
          </a>
        </div>
       
	"""
	
	products = prod
	return products


def loadProdDetalhes(prod):
	
	bancoBD = my_banco_base("p")
	
	
	prod_link = prod.split("_")
	
	nome_link = prod_link[0]
	num_link = prod_link[1]
	
	
	
	
	
	
	
	
	linkimg = url_for('static', filename='imageProdut/carbrador.webp')
	
	
	
	prod = ""
	for i in bancoBD:
		
		produto = bancoBD[i]
		
		nome_prod = produto["nome"]
		
		
		preco_prod = produto["preco"]
		num_prod = produto["numero"]
		link_img = produto["img_link"]
		detalhe_prod = produto["obse"]
		
		linkimg = link_img
		
		if nome_prod == nome_link:
			
			return [nome_prod,preco_prod,num_prod,linkimg,detalhe_prod]
		
		
	
	return ["error"]


def doReserv(prod,nomecl,tellcl):
	
	bancoBD = my_banco_base("p")
	
	precoP = ""
	prod_link = prod.split("_")
	
	nome_link = prod_link[0]
	num_link = prod_link[1]
	
	nomeCliente = nomecl
	tellCliente = tellcl
	
	dataAgora = datetime.datetime.now()
	
	
	dataAgora = str(dataAgora).split(" ")[0]
	
	
	dataAgora = dataAgora.replace("-","/")
	
	
	for cp in bancoBD:
		
		prodt = bancoBD[cp]
		
		numProd = prodt["numero"]
		
		
		if str(numProd) == str(num_link):
			
			precoP = prodt["preco"]
		
	
	
	
	urlReserv = "https://bs-siteof-sell-default-rtdb.firebaseio.com/reservas/.json"
	
	
	
	idsrvs = [627,72782,25522]
	while True:
		idrv = random.randint(10000,99999)
		
		if idrv in idsrvs:
			continue
		else:
			break
	
	
	dataPush = {
		"artigo n": num_link,
		"nome" : nomeCliente,
		"preco": precoP,
		"produto": nome_link,
		"status" : "pentente",
		"tell" : tellCliente,
		"idrv" : str(idrv),
		
		"data": dataAgora
	
	}
	
	
	
	if 1 == 1:
		
		resP = req.post(urlReserv, json.dumps(dataPush))
		
		
		
		
		
		
		
		if resP.status_code == 200:
			return ["Reserva Feita com sucesso",str(idrv)]
	else:
		
		...
	
	
	
		
		
	
	return ["error"]

def loadRmProduct(prod):
	rota = "/produtos"
	
	
	urlPDT = "https://bs-siteof-sell-default-rtdb.firebaseio.com"+rota+"/.json"
	
	
	resProd = req.get(urlPDT)
	
	bancoProd = resProd.json()
	
	
	
	#print(bancoProd)
	
	prod_link = prod.split("_")
	
	nome_prod_link = prod_link[0]
	num_artigo_link = prod_link[1]
	
	linkimg = url_for('static', filename='imageProdut/carbrador.webp')
	
	
	
	prod = ""
	for i in bancoProd:
		
		produto = bancoProd[i]
		
		nome_prod = produto["nome"]
		
		
		preco_prod = produto["preco"]
		num_prod = produto["numero"]
		link_img = produto["img_link"]
		detalhe_prod = produto["obse"]
		
		linkimg = link_img
		
		if nome_prod == nome_prod_link:
			
			#Eliminar este Produto...
			urlRM = "https://bs-siteof-sell-default-rtdb.firebaseio.com"+rota+"/"+i+".json"
			
			res = req.delete(urlRM)
			print("FUNCIONOU... BUCH")
			
			
			
			
			return [nome_prod,preco_prod,num_prod,linkimg,detalhe_prod]
		
		
	
	return ["error"]


def loadExist(prod):
	
	
	
	return True




def loadInteracoes():
	
	
	
	return numIntera


def loadDash():
	
	dados = my_banco_base("all")
	
	
	#daniel 7:25
	
	prod = dados["produtos"]
	msg = dados["mensagens"]
	intera = dados["interacoes"]
	reserv = dados["reservas"]
	
	lenProd = len(prod)
	lenMsg = len(msg)
	lenIntera = len(intera)
	lenReserv = len(reserv)
	
	dadosLen = [str(lenProd),str(lenMsg),str(lenIntera),str(lenReserv)]
	
	
	reservData = ""
	
	for r in reserv:
		
		reserva = reserv[r]
		
		nomeR = reserva["nome"]
		dataR =reserva["data"]
		prodR = reserva["produto"]
		tellR = reserva["tell"]
		precoR = reserva["preco"]
		numArg = reserva["artigo n"]
		statusR = reserva["status"]
		
		reservData = reservData + f"""
			<tr>
                            <td>{dataR}</td>
                            <td>{nomeR}</td>
                            <td>{prodR}</td>
                            <td>{tellR}</td>
                            
                            <td>{precoR}</td>
                            <td>{numArg}</td>
                            <td>{statusR}</td>
                            <td><button style="border: 1px solid green; padding: 3px;">Concluir</button></td>
                        </tr>
                        
		
		"""
	
	
	
	
	prodData = ""
	
	for p in  prod:
		produto = prod[p]
		
		nome_prod = produto["nome"]
		preco_prod = produto["preco"]
		num_prod = produto["numero"]
		link_img = produto["img_link"]
		
		linkimg = link_img
		
		
		
		prodData = prodData + f"""
	<div class="box-sell swiper-slide">
		  <a href="/editprodutel/{nome_prod+'_'+num_prod}">
          <img style="height: 50%;" src="{linkimg}" >
          <h5>{nome_prod}</h5>
          <p class="pna">artigo n°: 
          {num_prod}</p>
          <b><p>PRECO: {preco_prod} MTN</p></b>
          <button>Editar produto</button>
          </a>
        </div>
       
	"""
		
	
	
	
	MSGData = ""
	for m in  msg:
		
		dadoMsg = msg[m]
		
		nomeMsg = dadoMsg["nome"]
		
		mensagem = dadoMsg["msg"]
		
		MSGData = MSGData +f"""<div class="msg">
                    

                        <h3 class="msg--name">{nomeMsg}</h3>
                    
                    
                        <p class="msg--body">{mensagem}</p>
                    
                </div>"""
	
	
	dadosLoad = [prodData,MSGData,reservData]
	
	allDados = [dadosLen,dadosLoad]
	return allDados


def loadSearch(dado):
	
	
	dadosSh = dado
	dados = my_banco_base("all")
	
	
	#daniel 7:25
	
	prod = dados["produtos"]
	
	prodData = ""
	addprod= False
	for p in  prod:
		produto = prod[p]
		
		nome_prod = produto["nome"]
		preco_prod = produto["preco"]
		num_prod = produto["numero"]
		link_img = produto["img_link"]
		
		linkimg = link_img
		
		if " " in dadosSh:
			dadoP = dadosSh.split(" ")
			
			for cada_sh in dadoP:
				
				if cada_sh in nome_prod:
					addprod= True
		else:
			
			if dadosSh in nome_prod:
				addprod= True
				
				
			
			
		
		
		
		
		
		if addprod== True:
			prodData = prodData + f"""
	<div class="box-sell swiper-slide">
		  <a href="/editprodutel/{nome_prod+'_'+num_prod}">
          <img style="height: 50%;" src="{linkimg}" >
          <h5>{nome_prod}</h5>
          <p class="pna">artigo n°: 
          {num_prod}</p>
          <b><p>PRECO: {preco_prod} MTN</p></b>
          <button>Editar produto</button>
          </a>
        </div>
       
	"""
		
		addprod= False
	allDados = prodData
	
	
	
	return allDados



def loadLoginDash(nome,passw):
	
	
	
	url = "https://bs-siteof-sell-default-rtdb.firebaseio.com/confseet/.json"
	
	
	
	
	
	res = req.get(url)
	
	respo= res.json()
	
	#print(str(respo)+"_ resposta")
	print(nome,passw)
	
	nServer = respo["accessnameb1282"]
	pServer = respo["accesspassa1207"]
	
	
	if nServer == nome:
		
		if str(pServer) == str(passw):
			#print("sim sao nomes iguais!")
			return "da"
		
	#print("nao sao nomes iguais")
	return "se"
	
	
	
def sendMsg(nome,tell,email,msg1):
	allMSG = "Nome: "+ nome+"\n<br>Tell: "+ tell+"\n<br>Email: "+email+"\n<br>"+msg1+"\n<br>Mensagem do site a Venda."
	
	msg = MIMEMultipart()
	
	
	msg["Subject"] = "Mensagem de: "+nome
	msg["From"] = "mozlimoz0rc@gmail.com"
	msg["To"] = "buchsoftware@gmail.com"
	password = "vqcmikhtvwmvooab"
	
	#enviando a mensagem!
	msg.attach(MIMEText(allMSG,"html"))
	
	#credenciais
	
	s = smtplib.SMTP("smtp.gmail.com: 587")
	s.ehlo()
	s.starttls()
	s.login(msg["From"],password)
	s.sendmail(msg["From"],[msg["To"]],msg.as_string())
	s.quit()
	
	
	
	return nome


@app.route("/",methods=["post","get"])
@app.route("/home",methods=["post","get"])
def home():
	products = loadProd()
	a = "aa"
	
	
	if request.method == "POST":
		
		nome = request.form["nome"]
		tell = request.form["tell"]
		email = request.form["email"]
		msg = request.form["msg"]
		
		
		try:
			res = sendMsg(nome,tell,email,msg)
			
			return render_template("index.html",products=str(products),go_dash="ir ao DASH",pop = "Mensagem enviada com sucesso!")
		except:
			return render_template("index.html",products=str(products),go_dash="ir ao DASH",pop = "Mensagem nao foi enviada! Erro de Conexao...")
			
	
	return render_template("index.html",products=str(products),go_dash="ir ao DASH",pop = "")


@app.route("/detalhes/<prod>")
def detalhes(prod):
	
	DProd = loadProdDetalhes(prod)
	
	lengthProd = len(DProd)
	
	if lengthProd == 1:
		return render_template("about.html")
	else:
		
		nome = DProd[0]
		
		nArtigo = DProd[2]
		linkImg = DProd[3]
		detalheProd = DProd[4]
		precoProd = DProd[1]
		
		
		
		return render_template("detalhes.html",imgProd = linkImg,nomeProd = nome,precoProd = precoProd,detalheProd = detalheProd,linkReserv = prod)
	
	
	
	
@app.route("/editprodutel/<prod>")
def edit_product(prod):
	
	DProd = loadProdDetalhes(prod)
	
	lengthProd = len(DProd)
	
	if lengthProd == 1:
		return render_template("about.html")
	else:
		
		nome = DProd[0]
		
		
		nArtigo = DProd[2]
		linkImg = DProd[3]
		detalheProd = DProd[4]
		precoProd = DProd[1]
		linkRM = nome+"_"+nArtigo
		
		
		
		return render_template("edit_product.html",imgProd = linkImg,nomeProd = nome,precoProd = precoProd,detalheProd = detalheProd,linkReserv = prod,linkrm = linkRM)
	
	
@app.route("/eletro-rm-product/<linkRM1>")
def rm_product(linkRM1):
	
	rmLink = linkRM1
	
	DProd = loadRmProduct(rmLink)
	
	rmLink = rmLink.split("_")
	
	
	#print("_____--_____--______")
	#print(str(rmLink))
	
	
	p_nome = rmLink[0]
	n_artigo = rmLink[1]
	
	#print(DProd)
	
	#print("_____--_____--______")
	
	
	
	return jsonify({'nome': p_nome})
	

@app.route("/reserv/<prod>", methods=["POST","GET"])
def reserv(prod):
	
	loadExist = True
	#loadExist(prod)
	nome = prod.split("_")[0]
	artigon = prod.split("_")[1]
	lpost = "/reserv/"+prod
	
	
	
	if request.method == "POST":
		#prod = "buch"
		print("o metodo é post agora")
		
		nomeCl = request.form.get("nome")
		tellCl= request.form.get("tell")
		#precoP = request.form.get("precoproduto")
		
		res = doReserv(prod,nomeCl,tellCl)
		
		dmsg = res[0]+"\n"+res[1]
		return render_template("reserv.html",nomeProd = nome, artigoN = artigon,lpost = lpost,dataMsg = dmsg)
	
	
	dataMsg = ""
	
	
	if loadExist == False:
		
		
		return render_template("about.html")
		
	
	
	
	return render_template("reserv.html",nomeProd = nome, artigoN = artigon,lpost = lpost,dataMsg = dataMsg)





	
	




@app.route('/dashboard/add_product', methods=['GET', 'POST'])
def add_product():
    image_url = None
    if request.method == 'POST':
        file = request.files.get('imagem')
        
        nome = request.form["nome"]
        category = request.form["categoria"]
        preco = request.form["preco"]
        n_artgo = request.form["artg-n"]
        descricao = request.form["descricao"]
        
        
        if file:
            result = cloudinary.uploader.upload(file)
            image_url = result.get('secure_url')
            
            
            addproduto(nome,category,preco,descricao,image_url,n_artgo)
            
    return render_template('add_produto.html', image_url=image_url)



@app.route("/findpeca", methods=["post","get"])
def findPeca():
	
	products = loadProd()
	
	
	if request.method == "POST":
		dados = request.form["in_search"]
		
		lsearch = loadSearch(dados)
		
		return render_template("findpeca.html", products = lsearch)
	
	
	return render_template("findpeca.html",products = str(products))


@app.route("/eletro-admin-login",methods=["post","get"])
def goAdmin():
	
	if request.method == "POST":
		
		nome2 = request.form["nome"]
		senha3 = request.form["senha"]
		
		
		res = loadLoginDash(nome2,senha3)
		
		if res == "da":
			return admin()
		else:
			return render_template("logdash.html",info = "Senha ou Usuario Incorretos!")
	
	
	return render_template("logdash.html",info = "Prencha correctamente!")


@app.route("/dashbsboard17")
def admin():
	dados =  loadDash()
	dadosNum = dados[0]
	dadosLoad = dados[1]
	
	numIntera = dadosNum[0]
	
	numMSG = dadosNum[1]
	numProdut  = dadosNum[2]
	numReserv = dadosNum[3]
	
	loadMsg = dadosLoad[1]
	loadProd = dadosLoad[0]
	loadReserv = dadosLoad[2]
	
	
	
	
	return render_template("dash.html", interacoes = numIntera, numMsg = numMSG,numProdutos = numProdut,numReservas = numReserv,mensangens = loadMsg, products = loadProd,reservas = loadReserv)


@app.route("/contact", methods=["post","get"])
def contact():
	
	
	if request.method == "POST":
		nome = request.form["nome"]
		tell = request.form["tell"]
		email = request.form["email"]
		msg = request.form["msg"]
		
		
		try:
			res = sendMsg(nome,tell,email,msg)
			
			render_template("contact.html",pop = "Mensangem Enviado Com Sucesso!")
		except:
			render_template("contact.html",pop= "Mensagem Nao Enviado!")
			
		
		
			
	
	
	return render_template("contact.html",pop = "")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/services")
def service():
	return render_template("service.html")




if __name__ == "__main__":
    app.run(debug="True")