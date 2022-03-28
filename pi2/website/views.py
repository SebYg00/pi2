from flask import Blueprint, render_template, request
import yahoo_fin.stock_info as yf
import pandas as pd
import numpy as np
from sklearn import preprocessing as pp


views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template('home.html')
  #return render_template('home.html', companies = CompAnalysis("restaurants"))