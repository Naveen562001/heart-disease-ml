from flask import Flask, render_template, jsonify, request
import joblib
import numpy as np
import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from flask import send_file
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from flask import make_response
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Spacer


app = Flask(__name__, template_folder = 'templates')

def db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root",
        database="patient"
    )
    mycursor = mydb.cursor()
    return mydb, mycursor

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST','GET'])
def predict():
    #bp,ch,hr
    min = [75,100,60,70,0]
    max1=[140,240,100,90,4]
    
    disease = False
    mydb, cursor = db()

    data = request.form
    
    data_array = np.array([int(data['age']), int(data['sex']), int(data['ChestPainType']), int(data['RestingBP']), int(data['Cholesterol']), int(data['FastingBS']), int(data['RestingECG']), int(data['MaxHR']), int(data['ExerciseAngina']), int(data['oldpeak']), int(data['ST_Slope']),]).reshape(1,-1)
    
    model = joblib.load('naveen1.joblib')
    model1 = joblib.load('random.joblib')
    model2 = joblib.load('SVC.joblib')
    model3 = joblib.load('KNN.joblib')
    model4 = joblib.load('decision.joblib')
    #model5 = joblib.load('XGB.joblib')

    prediction = model.predict(data_array)
    prediction1 = model1.predict(data_array)
    prediction2 = model2.predict(data_array)
    prediction3 = model3.predict(data_array)
    prediction4 = model4.predict(data_array)
    #prediction5 = model5.predict(data_array)
    #random
    confidence1 = model1.predict_proba(data_array)
    #KNN
    confidence3 = model3.predict_proba(data_array)
    #decision treee
    confidence4 = model4.predict_proba(data_array)
    #svm
    #confidence2 =model2.predict_proba(data_array)
    prob=0
    result =int(prediction[0])
    if(result == 0):

        prob = (max(confidence1[0]))
        print(prob)
    else:
        prob = (max(1-confidence1[0]))
        print(prob)


    #retrieve
    
    
    if int(data['RestingBP']) < min[0] or int(data['RestingBP']) > max1[0] or int(data['systolic']) < min[3] or int(data['systolic']) > max1[3]or int(data['Cholesterol']) < min[1] or int(data['Cholesterol']) > max1[1] or int(data['MaxHR']) < min[2] or int(data['MaxHR']) > max1[2] or int(data['oldpeak']) < min[4] or int(data['oldpeak']) > max1[4]:
        disease = True
    if (disease ==True):
        if (result == 0):
            result1 = 'Heart Disease predicted'
            mod_name = 'Random Forest Classifier'
            con = 'confidence of prediction probablity'
            con1 =prob
            desc1 = "Based on the input was given by you.The model Predicted that you may have a chance of getting affected by Heart disease."
            img1 = "https://tse2.mm.bing.net/th?id=OIP.odUUUrdGaxRdDRp0CSKg6wHaHa&pid=Api&P=0"
            diet1 ="Please consult doctor"
            sql = "INSERT INTO patient1 (age, gender, chestpain, systolic, diastolic, cholestrol, fasting_BS, ECG, MAX_HR, EIA, ST, SLOPE,Name,Result,email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
            val = (int(data['age']), int(data['sex']), int(data['ChestPainType']), int(data['RestingBP']),int(data['systolic']), int(data['Cholesterol']), int(data['FastingBS']), data['RestingECG'], int(data['MaxHR']), data['ExerciseAngina'], float(data['oldpeak']), data['ST_Slope'],data['name'],result1,data['email'])
            cursor.execute(sql, val)
            mydb.commit()
            return render_template('result.html',result3 =result1,desc=desc1,img=img1,diet=diet1,mod_name=mod_name,con=con,con1=con1)
        if  (result ==1):
            result6 = 'Heart Disease predicted'
            mod_name = 'Random Forest Classifier'
            con = 'confidence of prediction probablity for(1)'
            con1=prob
            desc6 = "Based on the input was given by you.The model Predicted that you may have a chance of getting affected by Heart disease."
            img6 = "https://tse2.mm.bing.net/th?id=OIP.odUUUrdGaxRdDRp0CSKg6wHaHa&pid=Api&P=0"
            diet7 ="Please consult doctor"
            sql = "INSERT INTO patient1 (age, gender, chestpain, systolic, diastolic, cholestrol, fasting_BS, ECG, MAX_HR, EIA, ST, SLOPE,Name,Result,email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
            val = (int(data['age']), int(data['sex']), int(data['ChestPainType']), int(data['RestingBP']),int(data['systolic']), int(data['Cholesterol']), int(data['FastingBS']), data['RestingECG'], int(data['MaxHR']), data['ExerciseAngina'], float(data['oldpeak']), data['ST_Slope'],data['name'],result6,data['email'])
            cursor.execute(sql, val)
            mydb.commit()
            return render_template('result.html',result3 =result6,desc=desc6,img=img6,diet=diet7,mod_name=mod_name,con=con,con1=con1)
    else:
        result5 = 'Normal Healthy'
        mod_name = 'Random Forest Classifier Model'
        con = 'confidence of prediction probablity for(1)'
        con1=prob
        desc2 = "Based on the input was given by you.The model Predicted that you are Healthy.By analysing the normal level criteria"
        img2 = "https://thumbs.dreamstime.com/b/strong-healthy-heart-cartoon-character-isolated-white-background-happy-heart-icon-vector-flat-design-healthy-organ-concept-114559130.jpg"
        diet2=""
        sql = "INSERT INTO patient1 (age, gender, chestpain, systolic, diastolic, cholestrol, fasting_BS, ECG, MAX_HR, EIA, ST, SLOPE,Name,Result,email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
        val = (int(data['age']), int(data['sex']), int(data['ChestPainType']), int(data['RestingBP']),int(data['systolic']), int(data['Cholesterol']), int(data['FastingBS']), data['RestingECG'], int(data['MaxHR']), data['ExerciseAngina'], float(data['oldpeak']), data['ST_Slope'],data['name'],result5,data['email'])
        cursor.execute(sql, val)
        mydb.commit()
        return render_template('result.html',result3 =result5,desc=desc2,img=img2,diet=diet2,mod_name=mod_name,con=con,con1=con1)
    
    #sql query
    
    
        

    

        
      
    
    
    

@app.route('/predict/diet')
def Diet():
    mydb, cursor = db()

    cursor.execute("SELECT * FROM patient1 ORDER BY id DESC LIMIT 1")

    last_row = cursor.fetchone()



    return render_template('diet.html',last_row=last_row)
@app.route('/predict/download')
def download():
    descrp = ""
    mydb, cursor = db()

    cursor.execute("SELECT * FROM patient1 ORDER BY id DESC LIMIT 1")

    last_row = cursor.fetchone()
    #names:
    gender = ''
    ctype =''
    Rrecg =''
    eia =''
    slp=''
    if (last_row[3]=='0'):
        gender = 'female'
    else:
        gender = 'male'  

    if (last_row[4]=='0'):
        ctype = 'Typical Angina'
    if(last_row[4]=='1'):
        ctype = 'atypical angina'  
    if(last_row[4]=='2'):
        ctype = 'non anginal pain'
    else:
        ctype ='Asysmtomatic'         
    if (last_row[9]=='0'):
        recg = 'Normal'
    if(last_row[9]=='1'):
        recg = 'ST_WAVE abnormality' 
    else:
        recg= 'left verticular hypertrophy'
    if(last_row[11]=='0'):
        eia = 'No'
    else:
        eia ='Yes'
    if (last_row[13]=='0'):
        slp = 'Downsloping'
    if(last_row[13]=='1'):
        slp = 'Flat' 
    else:
        slp= 'Upsloping'    



    title_style = ParagraphStyle(
    name='Title',
    fontName='Helvetica-Bold',
    fontSize=24,
    leading=30,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#008080'),
)

    title = Paragraph("DREAM Hospital", style=title_style)
                    
    title1 = Paragraph("MEDICAL REPORT", style=title_style)
    # define the labels and values to display
    labels = ['Result','Name', 'Patient_ID', 'Age', 'Sex (0-Female 1-male)', 'Chest Pain Type', 
              'Resting Blood Pressure(diastolic)normal(110-120hg)','Resting Blood Pressure(systolic)normal (70-80hg)', 'Cholesterol(normal:170-200mg/dl)', 
              'Fasting Blood Sugar', 'Resting Electrocardiographic Results', 
              'Maximum Heart Rate Achieved(normal:60-100bpm)', 'Exercise Induced Angina', 
              'ST Depression Induced by Exercise Relative to Rest', 
              'Slope of the Peak Exercise ST Segment']
    
    values = [last_row[14],last_row[1], last_row[0], last_row[2], gender, ctype, 
              last_row[5], last_row[6], last_row[7], last_row[8], recg, 
              last_row[10], eia, last_row[12], slp]

    # set up the table style
    styles = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#008080')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#474747')),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    # build the table data
    table_data = [[label, value] for label, value in zip(labels, values)]
    content_str = '<b>chest pain description</b><br/>' \
              '<p>Typical Angina - chest pain precipitated by physical exertion or emotional stress<br/>' \
              'Atypical angina - back pain or pain that is described as burning, stabbing<br/>' \
              'non anginal pain - heart pain after a reasonable workup has excluded a cardiac cause<br/>' \
              'Asysmtomatic - a transient alteration in myocardial perfusion in the absence of chest pain<br/>' \
              '<b>ECG </b><br/>'\
              'Normal<br/>'\
              'ST_WAVE abnormality - ST segment abnormality (elevation or depression) is infraction<br/>' \
              'left verticular hypertrophy - thickening of heart wall result in elevation of pressure within the heart<br/>' \
              '<br/>'\
              '<b>SLOPE OF ST SEGMENT</b><br/>'\
              'upsloping - normal<br/>' \
              'flat,Downsloping - reduced blood flow to heart<br/>' \
              'Excercise induced angina-chest pain due to Excercise</p>' \
              

    # create the PDF document
    doc = SimpleDocTemplate('./static/'+str(last_row[0]) + '.pdf', pagesize=letter)
    
    # create the table and apply the style
    table = Table(table_data)
    table.setStyle(styles)

    name_style = ParagraphStyle(
    name='Name',
    fontName='Helvetica',
    fontSize=14,
    leading=16,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#008080'),
)

    content_style = ParagraphStyle(
    name='Content',
    fontName='Helvetica',
    fontSize=10,
    leading=12,
    leftIndent=inch,
    rightIndent=inch,
    spaceAfter=12,
)
    content_styles = ParagraphStyle(
    name='Content',
      fontName='Helvetica',
      fontSize=20,
      leading=12,
      leftIndent=inch,
      rightIndent=inch,
      spaceAfter=12,
    )

   
    name = Paragraph("Dr. John Doe", style=name_style)
    # add the table to the document and save it
    elements = [
    title1,
    Spacer(1, 0.15*inch),    
    title,
    Spacer(1, 0.35*inch),
    name,
    Spacer(1, 0.15*inch),
    table,
    Spacer(1, 0.5*inch),
    Paragraph(content_str, style=content_style)
]

    doc.build(elements)
    
    sender_email = "mobsterhel@gmail.com"
    sender_password = "zgkajockcqzagvez"

    # Recipient email address and subject
    recipient_email = last_row[15]
    subject = "Report PDF"

    # Create a multipart message
    message = MIMEMultipart()

    # Add the message body
    body = "Please find attached the report PDF"
    message.attach(MIMEText(body, "plain"))

    # Add the PDF attachment
    filename = './static/'+str(last_row[0]) + ".pdf"
    with open(filename, "rb") as f:
        attach = MIMEApplication(f.read(),_subtype="pdf")
        attach.add_header('Content-Disposition','attachment',filename=str(filename))
        message.attach(attach)

    # Setup the email parameters
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Create a SMTP session
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(sender_email, sender_password)

    # Send the email
    smtp_server.sendmail(sender_email, recipient_email, message.as_string())
    smtp_server.quit()

    print("Email sent!")
    
    # send the PDF file to the user for download
    filename = str(last_row[0])+".pdf"
    path = os.path.join(app.root_path, 'static', filename)
    response = make_response(send_file(path, as_attachment=True, mimetype='application/pdf'))
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return response

    


if __name__ == "__main__":
    app.run(debug=True)

