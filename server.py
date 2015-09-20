import bottle
from bottle import run, route, request
import os
import redis
import urlparse

url = urlparse.urlparse(os.getenv('REDIS_URL'))
mujredis = redis.Redis(host=url.hostname, port=url.port, password=url.password)

@route('/')
def index():
   return "Ziju !"

@route('/pozdrav')
def pozdrav():
   osloveni = os.getenv('OSLOVENI', 'Ahoj')
   jmeno = request.query.jmeno
   if jmeno: mujredis.append('lide', jmeno+', ')
   output = """<center><h1>%s %s !</h1><br>
            Dnes jsem uz pozdravil: %s<br>
            <form method="get" action="pozdrav">
              <input type="textbox" name="jmeno" />
              <button type="submit">Pozdrav me</button>
            </form>
            </center>
   """
   return output % (osloveni, jmeno, mujredis.get('lide'))

run(host='0.0.0.0', port=os.getenv('PORT', 8080))
