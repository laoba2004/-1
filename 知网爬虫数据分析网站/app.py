import json
from analyze import  bar_graph
from flask import Flask,render_template,request,jsonify,redirect,url_for,g,send_file
from cnspider import cnspider
import redis
app = Flask(__name__)
r=redis.Redis(host='localhost',port=6379,db=0)
articles=[]
@app.route('/',methods=['GET','POST'])
def hello_world():  # put application's code here
    if request.method=='GET':
        return render_template('an_form.html')
    else:
        title=request.form.get('title')
        author=request.form.get('author')
        keyword=request.form.get('keyword')
        page=request.form.get('page')
        print(title)
        return 'ok'
@app.route('/method',methods=['POST','GET'])
def get_form():
    if request.method=='GET':
        return render_template('an_form.html')
    else:
        theme=request.form.get('theme')
        title=request.form.get('title')
        author=request.form.get('author')
        keyword=request.form.get('keyword')
        page=request.form.get('page') or 1
        print(page)
        articles=cnspider(theme=theme,title=title,author=author,kwd=keyword,page=int(page) or 1)
        print(articles)
        print(len(articles))
        r.set('articles',json.dumps(articles))
        return redirect(url_for('show_data',page=1))
@app.route('/shower/<int:page>')
def show_data(page=1):
    data_str=r.get('articles')
    if data_str:
        articles=json.loads(data_str.decode())
    print(len(articles))
    perpage=20
    start=(page-1)*perpage
    end=start+perpage
    paginated_data=articles[start:end]
    total_page=len(articles)//perpage
    if len(articles)%total_page>0:
        total_page+=1
    data_length = len(paginated_data) if paginated_data else 0
    return render_template('shower.html',data_length=data_length,per_page=perpage,page=page,total_page=total_page,data=paginated_data)
@app.route('/analyze')
def analyze_data():
    data_str=r.get('articles')
    analyze_url=bar_graph(data_str)
    print(analyze_url)
    response=send_file(analyze_url,mimetype='image/svg')

    return response
if __name__ == '__main__':
    app.run()
