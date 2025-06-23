from flask import Flask,request,render_template
import joblib
import pandas as pd
import numpy as np

encoder=joblib.load('pavmentencoder.pkl')
norm=joblib.load('pavementnorm.pkl')
model=joblib.load('pavementmodel.pkl')

app=Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return render_template('home.html')
@app.route("/predict",methods=["GET","POST"])
def pred():
    pci=float(request.form.get('PCI'))
    rt=request.form.get('Road Type')
    aadt=float(request.form.get("AADT"))
    at=request.form.get('Asphalt Type')
    lm=int(request.form.get('Last Maintenance'))
    ar=float(request.form.get('Average Rainfall'))
    rut=float(request.form.get('Rutting'))
    iri=float(request.form.get("IRI"))
    if pci<10:
        pcil='failed'
    if pci>=10:
        pcil='very poor'
    if pci>24:
        pcil='poor'
    if pci>39:
        pcil='fair'
    if pci>54:
        pcil='good'
    if pci>=69:
        pcil='very good'
    if pci>=84:
        pcil='excellent'
    if ar<=40:
        arl='low'
    if ar>=40:
        arl='medium'
    if ar>=81:
        arl='high'
    if rut<=5:
        rutl='good'
    if rut>=5:
        rutl='mid'
    if rut>=10:
        rutl='severe'
    if rut>20:
        rutl='very severe'
    if aadt<=1000:
        aadtl='very low'
    if aadt>=1001:
        aadtl='low'
    if aadt>=5001:
        aadtl='medium'
    if aadt>10000:
        aadtl='high'
    if aadt>25000:
        aadtl='very high'
    if aadt>50000:
        aadtl='extremely high'
    if iri<1.6:
        iril='very good'
    if iri>=1.6:
        iril='good'
    if iri>=2.6:
        iril='Fair'
    if iri>3.5:
        iril='poor'
    if iri>4.5:
        iril='very poor'
    if lm<2021:
        lml='Preventive Maintenance'
    if lm>=2021:
        lml='Routine Maintenance'
    enc=encoder.transform([[rt,at,pcil,arl,rutl,aadtl,iril,lml]])
    nor=norm.transform([[pci,aadt,lm,ar,rut,iri]])
    df1=pd.DataFrame(enc,columns=['Road Type', 'Asphalt Type', 'PCI level', 'AR level', 'Rutting level',
       'AADT level', 'IRI level', 'Maintenance prevention'])
    df2=pd.DataFrame(nor,columns=['PCI', 'AADT','Last Maintenance', 'Average Rainfall', 'Rutting', 'IRI'])
    df=pd.concat([df1,df2],axis=1)
    ['Road Type', 'Asphalt Type', 'PCI level', 'AR level', 'Rutting level',
       'AADT level', 'IRI level', 'Maintenance prevention', 'PCI', 'AADT',
       'Last Maintenance', 'Average Rainfall', 'Rutting', 'IRI',
       'Needs Maintenance']
    ans=model.predict(df)
    return f"{ans}"

if __name__=="__main__":
    app.run(debug=True)