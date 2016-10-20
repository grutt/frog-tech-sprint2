from flask import Flask
import time
import os
import urlparse


urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

db = DB(
    dbname=url.path[1:],
    user=url.username,
    passwd=url.password,
    host=url.hostname,
    port=url.port
)

app = Flask(__name__)


@app.route('/')
def unixTime():
    return str(int(time.time()))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
