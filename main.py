import models
import requests
import json
from database import SessionLocal, engine
from fastapi import FastAPI, Request, Depends, BackgroundTasks, HTTPException
from fastapi.templating import Jinja2Templates
from keys import coin_market_cap_key
from models import Crypto
from pydantic import BaseModel
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

coin_market_cap_url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'

class CryptoRequest(BaseModel):
    """Class forces input to be str"""
    name: str

def get_db():
    """Used to test db connection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def crypto_fetcher(crypto_name):
    """Retrieves crypto details using the coin market cap API"""
    
    parameters = {
        'slug': crypto_name,
        'convert': 'USD'
    }
    
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': coin_market_cap_key,
    }
    session = requests.Session()
    session.headers.update(headers)

    response = session.get(coin_market_cap_url, params=parameters)
    return response 

def crypto_load_var_create(response_obj):
    """Loads coin market cap response obj"""
    return json.loads(response_obj.text)

def crypto_id_extractor(crytpo_json: json):
    """Extracts unique crytpo id from coin market cap crytpo json"""
    return list(crytpo_json['data'].keys())[0]

def crypto_load_tester(crytpo_json: json):
    """Tests crypto json has been correctly loaded"""
    if crytpo_json['status']['error_code'] == 0:
        return True
    else:
        return False

def delete_entry(id: int):
    """Deletes specifed crypto entry from db"""
    db = SessionLocal()
    crypto = db.query(Crypto).filter(Crypto.id == id).first()

    db.delete(crypto)
    db.commit()

def coin_feature_adder(crypto_obj: Crypto, crypto_name: str):
    """Takes a crypto obj with name and adds other features"""
    coin_json_data = json.loads(crypto_fetcher(crypto_name).text)
    crypto_id = crypto_id_extractor(coin_json_data)

    crypto_obj.symbol = coin_json_data['data'][crypto_id]['symbol']
    crypto_obj.price = coin_json_data['data'][crypto_id]['quote']['USD']['price']
    crypto_obj.max_supply = coin_json_data['data'][crypto_id]['max_supply']
    crypto_obj.market_cap = coin_json_data['data'][crypto_id]['quote']['USD']['market_cap']
    crypto_obj.total_supply = coin_json_data['data'][crypto_id]['total_supply']

    return None

def fetch_crypto_data(id: int):
    """Populates crypto in db"""
    db = SessionLocal()

    crypto = db.query(Crypto).filter(Crypto.id == id).first()
    crypto_name_str = str(crypto.name)
    coin_feature_adder(crypto, crypto_name_str)

    db.add(crypto)
    db.commit()

@app.get("/")
def get_dashboard(request: Request, price = None, market_cap = None, db: Session = Depends(get_db)):
    """
    Displays the crypto price dashbaord homepage
    """
    cryptos = db.query(Crypto)

    if price:
        cryptos = cryptos.filter(Crypto.price > price)

    if market_cap:
        cryptos = cryptos.filter(Crypto.market_cap > market_cap)    

    return templates.TemplateResponse("crypto_dash.html", {
        "request": request,
        "cryptos": cryptos,
        "price": price,
        "market_cap": market_cap
    })

@app.post("/crypto")
async def add_crypto(crypto_request: CryptoRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Adds a crypto to the database 
    """
    crypto = Crypto()
    crypto.name = crypto_request.name
    crypto_name_str = str(crypto_request.name)

    db.add(crypto)
    db.commit()

    crypto_file_json = crypto_load_var_create(crypto_fetcher(crypto_name_str))
    
    if crypto_load_tester(crypto_file_json):
        background_tasks.add_task(fetch_crypto_data, crypto.id)
        return {"success": f"{crypto_name_str} added"}

    else:
        background_tasks.add_task(delete_entry, crypto.id)
        return {"failure": f" cannot add {crypto_name_str}, it is not available in the coin market cap db"}


