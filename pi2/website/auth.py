from crypt import methods
from flask import Blueprint, render_template, request, send_file
from soupsieve import match
import yahoo_fin.stock_info as yf
import pandas as pd
import numpy as np
from sklearn import preprocessing as pp
auth = Blueprint('auth', __name__)
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import datetime as dt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas



def ImportData(ticker,nbYear):
    dateNow=dt.datetime.now().date()
    past_date = dateNow - dt.timedelta(days=nbYear*365)
    past_date=past_date.strftime('%d/%m/%Y')   
    weekly_data = yf.get_data(ticker,index_as_date=False,start_date = str(past_date))
    weekly_data["close"]= (weekly_data["close"]-weekly_data["close"].mean())/(weekly_data["close"].max() - weekly_data["close"].min())#normalization of the stock value
    return weekly_data

def RecupDatas(tab,nbYear): # tab de tickers de compagnies
    res=[]
    tabPd=[]
    for i in tab:
        tabPd.append(ImportData(i,nbYear))
    for j in range(len(tabPd[0]["close"])):
        temp=0
        for k in range(len(tabPd)):
            temp+=tabPd[k]["close"].loc[j]
        res.append(temp/len(tabPd))
    return res,tabPd[0]["date"]


def Tendency(y,date):
    y=np.array(y).reshape(-1, 1) 
    x=range(0,len(y))
    x=np.array(x).reshape(-1,1)
    model=LinearRegression()
    model.fit(x,y)
    return model.predict(x),y,date,model.coef_[0]

def Display(ypred,y,date):
    plt.plot(date,y)
    plt.plot(date,ypred)



@auth.route('/about')
def about():
    return render_template('about.html')

@auth.route('/code', methods=['GET', 'POST'])
def code():
    return render_template('code.html', boolean=True)


@auth.route("/info" , methods=['GET', 'POST'])
def info():
    select = str(request.form.get('selector'))
    df = pd.read_csv("/Users/sebastienyung/Documents/A4 ESILV/pi2/website/templates/sector.csv")
    df = df[df['Sector'] == select]
    
    return render_template('info.html', companies = df)

@auth.route("/company/<name>" , methods=['GET', 'POST'])
def infoCompany(name):
    companies = pd.read_csv('/Users/sebastienyung/Documents/A4 ESILV/pi2/website/templates/method.csv')
    company = companies[companies['Ticker']==name]
    return render_template('company.html', company=company)