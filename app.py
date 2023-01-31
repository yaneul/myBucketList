from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb://test:sparta@ac-poz6shb-shard-00-00.2xrmcy8.mongodb.net:27017,ac-poz6shb-shard-00-01.2xrmcy8.mongodb.net:27017,ac-poz6shb-shard-00-02.2xrmcy8.mongodb.net:27017/Cluster0?ssl=true&replicaSet=atlas-opog1p-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list) + 1

    #db에 저장
    doc = {
        'num':count,
        'bucket':bucket_receive,
        'done':0
    }

    db.bucket.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    num_receive = request.form['num_give']
    #delete
    # 숫자를 클라이언트로부터 받아오면 문자로 바뀌기 때문에 숫자로 바꿔주는 과정이 필요함 int(num_receive)
    db.bucket.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료!'})


@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    #update
    # 숫자를 클라이언트로부터 받아오면 문자로 바뀌기 때문에 숫자로 바꿔주는 과정이 필요함 int(num_receive)
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '버킷 완료!'})


@app.route("/bucket/notdone", methods=["POST"])
def bucket_not_done():
    num_receive = request.form['num_give']
    #update
    # 숫자를 클라이언트로부터 받아오면 문자로 바뀌기 때문에 숫자로 바꿔주는 과정이 필요함 int(num_receive)
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})
    return jsonify({'msg': '완료 해제!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': bucket_list})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)