from flask import Flask,render_template,request
import pandas as pd
import mysql.connector
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import BaggingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import ExtraTreeRegressor




mydb = mysql.connector.connect(host='localhost',user='root',password='',port='3306',database='Crop_yield')
cur = mydb.cursor()


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        psw = request.form['psw']
        sql = "SELECT * FROM crop WHERE Email=%s and Password=%s"
        val = (email, psw)
        cur = mydb.cursor()
        cur.execute(sql, val)
        results = cur.fetchall()
        mydb.commit()
        if len(results) >= 1:
            return render_template('loginhome.html', msg='login succesful')
        else:
            return render_template('login.html', msg='Invalid Credentials')

    return render_template('login.html')

@app.route('/loginhome')
def loginhome():
    return render_template('loginhome.html')






@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method == "POST":
        print('a')
        name = request.form['name']
        print(name)
        email = request.form['email']
        pws = request.form['psw']
        print(pws)
        cpws = request.form['cpsw']
        if pws == cpws:
            sql = "select * from crop"
            print('abcccccccccc')
            cur = mydb.cursor()
            cur.execute(sql)
            all_emails = cur.fetchall()
            mydb.commit()
            all_emails = [i[2] for i in all_emails]
            if email in all_emails:
                return render_template('registration.html', msg='success')
            else:
                sql = "INSERT INTO crop(name,email,password) values(%s,%s,%s)"
                values = (name, email, pws)
                cur.execute(sql, values)
                mydb.commit()
                cur.close()
                return render_template('login.html', msg='success')
        else:
            return render_template('login.html', msg='password not matched')

    return render_template('registration.html')


@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == "POST":
        file = request.files['file']
        print(file)
        global df
        df = pd.read_csv(file)
        print(df)
        return render_template('upload.html', columns=df.columns.values, rows=df.values.tolist(),msg='Dataset uploaded')
    return render_template('upload.html')
@app.route('/viewdata')
def viewdata():
    print(df.columns)
    df_sample = df.head(50)
    return render_template('viewdata.html', columns=df_sample.columns.values, rows=df_sample.values.tolist())

df=None
x_train=None
@app.route('/preprocessing',methods=['POST','GET'])
def preprocessing():
    global x, y, x_train, x_test, y_train, y_test
    if request.method == "POST":
        size = int(request.form['split'])
        size = size / 100
        print(size)
        

        df.fillna(df['Production'].median(), inplace=True)
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        State = le.fit_transform(df.State)
        crop = le.fit_transform(df.Crop)
        Season = le.fit_transform(df.Season)
        df['State'] = State
        df['Crop'] = crop
        df['Season'] = Season

        x = df.iloc[:, [1, 2, 3, 4, 5, 7]]
        y = df.iloc[:, 6]

        x_train, x_test, y_train, y_test = train_test_split(x.values, y.values, test_size=size, random_state=0)

        return render_template('preprocessing.html', msg='Data Preprocessed and It Splits Succesfully')

    return render_template('preprocessing.html')



@app.route('/model',methods=['POST','GET'])
def model():
    if request.method=='POST':
        models = int(request.form['algo'])
        if models==1:
            print("==")
            bg = BaggingRegressor()
            bg.fit(x_train,y_train)
            y_pred =bg.predict(x_test)


            import numpy as np
            
            import matplotlib.pyplot as plt
            from scipy import stats

            slope, intercept, r_value, p_value, std_err = stats.linregress(y_test, y_pred)

            def linefitline(b):
                return intercept + slope * b

            line1 = linefitline(y_test)
            line2 = np.full(y_pred.shape, [y_pred.mean()])

            differences_line1 = linefitline(y_test) - y_pred
            line1sum = 0
            for i in differences_line1:
                line1sum = line1sum + (i * i)
            line1sum
            differences_line2 = line2 - y_pred
            line2sum = 0
            for i in differences_line2:
                line2sum = line2sum + (i * i)
            line2sum
            li = line2sum - line1sum
            bg_score = li / line2sum

            acc = bg_score *100
            msg = 'R2_score  for Bagging Regressor model is ' + str(acc) + str('%')

        elif models== 2:
            print("======")
            sv = SVR()
            sv.fit(x_train[:10000],y_train[:10000])
            svp = sv.predict(x_test)
            import numpy as np
            import matplotlib.pyplot as plt
            from scipy import stats

            slope, intercept, r_value, p_value, std_err = stats.linregress(y_test, svp)

            def linefitline(b):
                return intercept + slope * b

            line1 = linefitline(y_test)
            line2 = np.full(14995, [svp.mean()])
            differences_line1 = linefitline(y_test) - svp
            line1sum = 0
            for i in differences_line1:
                line1sum = line1sum + (i * i)
            line1sum
            differences_line2 = line2 - svp
            line2sum = 0
            for i in differences_line2:
                line2sum = line2sum + (i * i)
            line2sum
            li = line2sum - line1sum
            sv_score = li / line2sum

            acc = sv_score * 100
            msg = 'R2_score  for SVR model is ' + str(acc) + str('%')

        elif models==3:
            print("===============")
            knn = KNeighborsRegressor(n_neighbors=5)
            knn.fit(x_train,y_train)
            knnp = knn.predict(x_test)
            import numpy as np
            import matplotlib.pyplot as plt
            from scipy import stats

            slope, intercept, r_value, p_value, std_err = stats.linregress(y_test, knnp)

            def linefitline(b):
                return intercept + slope * b

            line1 = linefitline(y_test)
            line2 = np.full(14995, [knnp.mean()])
            differences_line1 = linefitline(y_test) - knnp
            line1sum = 0
            for i in differences_line1:
                line1sum = line1sum + (i * i)
            line1sum
            differences_line2 = line2 - knnp
            line2sum = 0
            for i in differences_line2:
                line2sum = line2sum + (i * i)
            line2sum
            li = line2sum - line1sum
            knn_score = li / line2sum

            acc = knn_score*100
            msg = 'R2_score  for KNN model is ' + str(acc) + str('%')
        elif models == 4:
            print("===============")
            gp = ExtraTreeRegressor()
            gp.fit(x_train, y_train)
            etr = gp.predict(x_test)
            import numpy as np
            import matplotlib.pyplot as plt
            from scipy import stats

            slope, intercept, r_value, p_value, std_err = stats.linregress(y_test, etr)

            def linefitline(b):
                return intercept + slope * b

            line1 = linefitline(y_test)
            line2 = np.full(14995, [etr.mean()])
            differences_line1 = linefitline(y_test) - etr
            line1sum = 0
            for i in differences_line1:
                line1sum = line1sum + (i * i)
            line1sum
            differences_line2 = line2 - etr
            line2sum = 0
            for i in differences_line2:
                line2sum = line2sum + (i * i)
            line2sum
            li = line2sum - line1sum
            gb_score = li / line2sum

            acc = gb_score * 100
            msg = 'R2_score  for Extra Tree Regressor model is ' + str(acc) + str('%')

        return render_template('model.html',msg=msg)

    return render_template('model.html')
@app.route('/prediction',methods=['POST','GET'])
def prediction():
    print('111111')
    if  request.method == 'POST':
        models = int(request.form['algo'])
        print('2222')
        State = request.form['State']
        print(State)
        Year =request.form['Year']
        print(Year)
        Season=request.form['Season']
        print(Season)
        Crop =request.form['Crop']
        print(Crop)
        Area = request.form['Area']
        print(Area)
        Rainfall = request.form['Rainfall']
        print(Rainfall)
        m = [State, Year, Season, Crop, Area, Rainfall]
        if models==1:
            print("==")
            model = BaggingRegressor()
            model.fit(x_train, y_train)
            result = model.predict([m])
            print(result)
            msg = 'The prediction value of Bagging Model is ' + str(result)
            return render_template('prediction.html', msg=msg)
        elif models== 2:
            print("======")
            model = SVR()
            model.fit(x_train[:10000],y_train[:10000])
            result = model.predict([m])
            print(result)
            msg = 'The prediction value of Support Vector model is ' + str(result)
            return render_template('prediction.html', msg=msg)
        elif models==3:
            print("======")
            model = KNeighborsRegressor(n_neighbors=5)
            model.fit(x_train, y_train)
            result = model.predict([m])
            print(result)
            msg = 'The prediction value of KNN model is ' + str(result)
            return render_template('prediction.html', msg=msg)
        elif models==4:
            print("======")
            model = ExtraTreeRegressor()
            model.fit(x_train, y_train)
            result = model.predict([m])
            print(result)
            msg = 'The prediction value of ExtraTree model is ' + str(result)
            return render_template('prediction.html', msg=msg)


    return render_template('prediction.html')

@app.route("/graph",methods=['GET','POST'])
def graph():
    if request.method=="POST":
        modelname=request.form['modelgraph']
        print(modelname)
        if modelname=="r2score":
            return render_template("graph.html",modelname="r2score")
        elif modelname=='time':
            return render_template("graph.html",modelname='time')

            pass
    return render_template('graph.html')


if __name__=="__main__":
    app.run(debug=True)

