from flask import Flask, request, render_template,url_for,redirect
import os
import sys
sys.path.append(r"C:\Users\vials\Desktop\毕业设计\MyPHPScan")
from parser1 import parser_code

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'tests'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('report', file_path=file.filename))
    else:
        return '文件上传失败'

@app.route('/report/<file_path>',methods=['GET'])
def report(file_path):
    res=parser_code(file_path)
    return render_template('vul.html', vulnerabilities=res)



if __name__ == '__main__':
    app.run(debug=True)

