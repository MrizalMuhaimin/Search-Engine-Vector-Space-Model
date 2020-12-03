import os
from flask import render_template, flash, request, redirect
from werkzeug.utils import secure_filename
from app import app
import pandas as pd
import app.makeFinalSql as fsql
import app.getURLfromGoogle as gurl
import app.readdataUpload as rup
import app.saveDatatoSql as ssql
import app.makeSastra as ms
import app.rank as rank


app.secret_key = "secret key"

app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024

path = 'app/'
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'static/uploads')
# Make directory if "uploads" folder not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'html'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        Query = request.form['query']
        if Query == '':
            return redirect(request.url)
        # Mengambil data dari masukan form HTML
        searchQuery = Query
        Query = ms.Makesastra(Query)
        corpusQ = [Query]
        corpusD = fsql.ReturnListSastra()
        corpus = corpusQ + corpusD

        # Menyimpan Jumlah Dokumen dan Namanya
        columns_length = len(corpus)
        columns_name = rank.colRename(columns_length)

        # Transform Dokumen menjadi Matrix
        vocab = rank.fit(corpus)
        X = rank.transform(vocab,corpus)

        # Membuat DataFrame
        df = (pd.DataFrame(X.T, index=list(vocab.keys()), columns=columns_name))
        df_show = df.loc[df['Query'] == 1]

        # Menghitung Cosine Similarity
        dfT = df.T
        cosine_sim_array=rank.cosine_sim(dfT,columns_length)

        # menyimpan hasil perhitungan ke finaldatabase.sqlite
        fsql.SavePersen(cosine_sim_array)

        # menyimpan data rank descending
        list_rank = fsql.ReturnRank()

        show = True
        return render_template('index.html', tables=[df_show.to_html(classes='vector_table')], dict=list_rank, show=show, query=searchQuery)
        # return redirect('/index')
    else:
        show = False
        # Render
        return render_template('index.html',  show=show)


@app.route('/perihal')
def perihal():
    return render_template('perihal.html')


@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/adddatabase')
def adddata():
    return render_template('adddata.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No File Chosen')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        accepted = True
        for file in files:
            if file and not(allowed_file(file.filename)):
                accepted = False
        if accepted:
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], filename))

            flash('File(s) successfully uploaded')
            # save data base from new file upload
            rup.readDataUpload()
            fsql.SaveFinalSql()

        else:
            flash('Uploaded Failed! Only accept .txt and .html files')
        return redirect('/upload')

    else:

        return render_template('upload.html')

@app.route('/googling', methods=['GET', 'POST'])
def googling():
    if request.method == 'POST':
        Query = request.form['query']
        flash('Search URL')
        URL_From_Google = gurl.UrlFromGoogle(Query)
        flash('Search File HTML')
        URL_In_Google = gurl.UrlInGoogle(URL_From_Google)
        flash('Clean Data')
        ssql.urltoSQL(URL_In_Google)
        flash('Save To Database')
        fsql.SaveFinalSql()
        flash('Data....... Ready to Use')
        return render_template('googling.html')

    else:
        return render_template('googling.html')