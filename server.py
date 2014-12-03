#!/usr/bin/python
from gevent import monkey
monkey.patch_all()

import gevent
import pika

from flask import Flask, render_template, request
from flask.ext.socketio import SocketIO, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


###################################
##### RabbitMQ specific codes #####
###################################
# This has to done here because we are
# mostly emitting using the socketio object

def consumer():
    '''
    RabbitMQ consumer.
    This is spawned in a greenlet using gevent.spawn in __init__
    '''
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    print "Connection to rabbitmq established"
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)

    queue = "internet_usage"

    channel.queue_declare(queue=queue, durable=True)
    print "queue: %s" % (queue)
    channel.basic_consume(callback, queue=queue)
    channel.start_consuming()


def callback(ch, method, properties, payload):
    '''
    callback() is called during message consumption.
    '''
    socketio.emit('internet_usage', payload)
    ch.basic_ack(delivery_tag=method.delivery_tag)


###################################
########### Flask views ###########
###################################

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')


###################################
#### Socket io specific codes #####
###################################


# Connection established with a new client
@socketio.on('connect')
def connect():
    print 'Client connected'


# Connection to a client lost
@socketio.on('disconnect')
def disconnect():
    print 'Client disconnected'


def make_ready():
    '''
    Prepares external components to work with the server
    '''
    try:
        # spawn rabbitmq consumer gevent greenlet
        gevent.spawn(consumer)
        return "Fire!"
    except Exception, e:
        print e

if __name__ == '__main__':
    ready_to_fire = make_ready()

    if ready_to_fire == "Fire!":
        app.debug = True
        socketio.run(app, host='0.0.0.0', port=3000)
