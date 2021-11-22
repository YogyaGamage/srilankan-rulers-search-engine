from flask import Flask, render_template, request
from searchquerry import search
from elasticsearch_dsl import Index

app = Flask(__name__)


@app.route('/search', methods=['GET', 'POST'])
def search_engine():
    # return "hello world"
    if request.method == 'POST':
        print("hello")
        query = request.form['searchTerm']
        res = search(query)
        hits = res['hits']['hits']
        time = res['took']
        # aggs = res['aggregations']
        num_results =  res['hits']['total']['value']

        return render_template('index.html', query=query, hits=hits, num_results=num_results,time=time)

    if request.method == 'GET':
        if request.args:
            query = request.args['searchTerm']
            res = search(query)
            hits = res['hits']['hits']
            time = res['took']
            aggs=False
            try :
                aggs = res['aggregations']
            except:
                pass
            print(aggs)
            num_results =  res['hits']['total']['value']
            return render_template('index.html', query=query, hits=hits, num_results=num_results, time=time, aggs=aggs)
        return render_template('index.html', init='True')


if __name__ == '__main__':
    app.run()