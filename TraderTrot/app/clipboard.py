from bs4 import BeautifulSoup

import pandas as pd
import datetime
from requests import request
import requests
from requests.exceptions import ConnectionError
import urllib.request

def stock_prediction(req):
    if(req.session.is_empty()):
        
        req.session.set_expiry(0) 
        return render(req,'login.html') 
    else:
        if req.method == 'POST':
            symbol=f"{req.POST['symbol']}"
        else:
            symbol='TCS'
            
        import datetime 
        
        stock=stockdata()
        import math
        start=datetime.date(2020,1,1)
        end=datetime.date.today()
        st=stockdata.objects.filter(symbol=symbol)
        loc=f"analysis/stockdata/{symbol}.csv"
        
        if st.count()==1:
            for i in st:
                if i.date==datetime.date.today():
                    pass
                else:
                    df=pd.read_csv(loc)
                    lastdate=datetime.datetime.strptime(df['Date'].max(),"%Y-%m-%d")
                    print(type(lastdate))
                    start=lastdate.date()+datetime.timedelta(days = 1)
                    data=get_history(symbol=symbol, start=start , end=end)
                    data.to_csv(loc,mode='a',index=True,header=False)
                    i.date=datetime.date.today()
                    i.save()
                    
        else:
            data=get_history(symbol=symbol, start=start , end=end)
            data.to_csv(loc)
            stock.symbol=symbol
            stock.date=datetime.date.today()
            stock.save()
            
               
        df=pd.read_csv(loc)
        df=df.set_index('Date')
        data=df.filter(["Close"])
        dataset=data.values
        training_data_len=math.ceil(len(dataset)*0.8)
        scaler=MinMaxScaler(feature_range=(0,1))
        scaled_data=scaler.fit_transform(dataset)
        train_data=scaled_data[0:training_data_len,:]
        x_train = []
        y_train = []
        for i in range(60, len(train_data)):
            x_train.append(train_data[i-60:i, 0])
            y_train.append(train_data[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        model = Sequential()
        model.add(LSTM(50, return_sequences = True, input_shape = (x_train.shape[1], 1)))
        model.add(LSTM(50, return_sequences = False))
        model.add(Dense(25))
        model.add(Dense(1))
        model.compile(optimizer = 'adam', loss = 'mean_squared_error')
        model.fit(x_train, y_train, batch_size = 1, epochs = 1)
        test_data = scaled_data[training_data_len - 60: , :]
        x_test = []
        y_test = dataset[training_data_len:, :]
        for i in range (60, len(test_data)):
             x_test.append(test_data[i - 60:i, 0])

        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)
        train = data[:training_data_len]
        valid = data[training_data_len:]
        valid.insert(1,'predictions',predictions)
        last_60_days = data[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)
        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1], 1))
        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = train.index, y = train['Close'],
                            mode='lines',
                            name='Close',
                            marker_color = '#1F77B4'))
        fig.add_trace(go.Scatter(x = valid.index, y = valid['Close'],
                            mode='lines',
                            name='Val',
                            marker_color = '#FF7F0E'))
        fig.add_trace(go.Scatter(x = valid.index, y = valid.predictions,
                            mode='lines',
                            name='Predictions',
                            marker_color = '#2CA02C'))

        fig.update_layout(
            title=symbol,
            titlefont_size = 28,
            hovermode = 'x',
            xaxis = dict(
                title='Date',
                titlefont_size=16,
                tickfont_size=14),
            
            height = 800,
            
            yaxis=dict(
                title='Close price in INR (₹)',
                titlefont_size=16,
                tickfont_size=14),
            legend=dict(
                y=0,
                x=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'))

        div=opy.plot(fig,auto_open=False,output_type='div')
        nse_list=stocklist()
        context={'list':nse_list,'graph':div,'price':pred_price}
        return render(req,'analysis/graph.html',context)
