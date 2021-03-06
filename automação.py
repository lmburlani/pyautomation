# objetivo da minha demonstração é usar um banco de dados aleatório para gerar um ranking  atualizado com as 25 lojas contendo 3 informações e iremos enviar essa informação via e-mail
#1 faturamento
#2 quantidade de mercadorias vendidas
#3 ticket médio das mercadorias de cada loja
# para isso iremos usar a biblioteca pandas
#I will make a copy of this code with the comments in english in the future
import pandas as pd

# importar a base de dados (em anexo no git, aqui irei importar direto do meu drive)
from google.colab import drive
drive.mount('/content/drive')

# iremos atribuir uma variável para ler o arquivo
df = pd.read_excel(r'/content/drive/MyDrive/python automação/Vendas.xlsx')

# executando a variável
display(df)

# 1 iremos calcular o faturamento das lojas
faturamento = df[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()
faturamento = faturamento.sort_values(by='Valor Final', ascending=False)
display(faturamento)

# 2 agora iremos calcular a quantidade vendida
quantidade = df[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
quantidade = quantidade.sort_values(by='ID Loja', ascending=False)
display(quantidade)

# 3 cálculo do ticket médio
ticket_medio = (faturamento['Valor Final'] / quantidade['Quantidade']).to_frame()
ticket_medio = ticket_medio.rename(columns={0: 'Ticket Medio'})
ticket_medio = ticket_medio.sort_values(by='Ticket Medio', ascending=False)
display(ticket_medio)

# criando a função para enviar e-mails usando as bibliotecas smtplib e email.message (e-mails fictícios)
import smtplib
import email.message

def enviar_email(resumo_loja, loja):

  server = smtplib.SMTP('smtp.gmail.com:587')  
  email_content = f'''
  <p>Coe Lira,</p>
  {resumo_loja.to_html()}
  <p>Tmj</p>'''
  
  msg = email.message.Message()
  msg['Subject'] = f'Luiz - Loja: {loja}'
  
  
  msg['From'] = 'luiz@gmail.com'
  msg['To'] = 'loja@gmail.com'
  password = senha
  msg.add_header('Content-Type', 'text/html')
  msg.set_payload(email_content)
  
  s = smtplib.SMTP('smtp.gmail.com: 587')
  s.starttls()
  # as linhas abaixo são para preencher as informações de login
  s.login(msg['From'], password)
  s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

# cálculo dos indicadores por loja
lojas = df['ID Loja'].unique()

for loja in lojas:
  tabela_loja = df.loc[df['ID Loja'] == loja, ['ID Loja', 'Quantidade', 'Valor Final']]
  resumo_loja = tabela_loja.groupby('ID Loja').sum()
  resumo_loja['Ticket Médio'] = resumo_loja['Valor Final'] / resumo_loja['Quantidade']
  display(resumo_loja)

# envio do e-mail, esse código irá dar erro pois os e-mails são fictícios
enviar_email(resumo_loja, loja)
