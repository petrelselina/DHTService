from tasks import *
from time import sleep
from threading import Thread
import Queue, json

RECEIVE_THREADS = 1
TORRENT_THREADS = 3


# using example
class Master(object):
    def __init__(self, queue):
        self.queue = queue

    def save(self, infohash, address=None):
        info_hash = infohash.encode('hex').upper();
        print ('%s from %s:%s' % (infohash.encode('hex').upper(), address[0], address[1]))
        self.queue.put(info_hash);


class DHTRunner(object):
    def __init__(self):
        self.threads = []
        self.queue = Queue.Queue()
        self.is_running = False;

    def parse_torrent(self):
        while self.is_running:
            if (self.queue.qsize() > 0):
                print 'Queue Size: %d' % self.queue.qsize();
                info_hash = self.queue.get();
                content = hash_to_torrent(info_hash, 10);
                if (content != None):
                    torrent = Parser(content)
                    print 'NAME: %S' % torrent.getName()
            sleep(1)

    def get_current_state(self):
        return self.queue.qsize();

    def stop(self):
        self.is_running = False
        for i in (0, len(self.threads)):
            self.threads[i].stop()

    def start(self):
        self.threads = []
        self.queue = Queue.Queue()
        self.is_running = True
        for i in xrange(RECEIVE_THREADS):
            port = i + 9500
            print "start thread %d" % port
            master = Master(self.queue)
            dht = DHT(master, "0.0.0.0", port, max_node_qsize=1000)
            dht.start()
            self.threads.append(dht)
            sleep(1)
        for i in xrange(TORRENT_THREADS):
            parse_thread = Thread(target=self.parse_torrent)
            parse_thread.start()


if __name__ == "__main__":
    DHTRunner().start()
