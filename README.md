## AI FOR THE ANALYSIS AND CREATION OF A CROWDFUNDING

### API created with FLASK API to validate the parameters to create a crownfunding in app HelpPot

... wait to see the news ...

### Routes

- POST - /validate/crowdfunding
### Body (JSON):
Example:
```json
{
	"title": "Meu pet esta doente",
	"content": "Preciso de ajuda para pagar meu pc gamer",
	"cash": "5000"
}
```
return:
```json
{
	"MOTIVE": "Conteúdo não condiz com as causas aceitas pela plataforma (saúde, urgências ou similares)",
	"VALIDATE": "N"
}
```

### To install the project

Requirements: 
- Python

 To clone the project:

```shell
git clone 
```

To create a virtual environment

```shell
python -m venv env
```

Start the virtual environment

```shell
.\env\Scripts\activate
```

To install dependencies

```shell
pip install -r requirements.txt  
```

Start the project
```
python server.py
```