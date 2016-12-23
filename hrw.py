import mmh3
import socket
import struct
import redis

r_server = redis.Redis("127.0.0.1")

def ip2long(ip):
    """Convert an IP string to long."""
    #packedIP = socket.inet_aton(ip)
    #return struct.unpack("!L", packedIP)[0]

    splitDots = ip.split(".")
    str_ip = ""
    for s in splitDots:
        str_ip += s
    splitColon = str_ip.split(":")
    final_strip = ""
    for s in splitColon:
        final_strip += s

    return int(final_strip)


def murmur(key):
    """Return murmur3 hash of the key as 32 bit signed int."""
    return mmh3.hash(key)


def weight(node, key):
    """Return the weight for the key on node.
    Uses the weighing algorithm as prescibed in the original HRW white paper.
    @params:
        node : 32 bit signed int representing IP of the node.
        key : string to be hashed.
    """
    a = 1103515245
    b = 12345
    hash = murmur(key)

    return (a * ((a * node + b) ^ hash) + b) % (2^31)


class Ring(object):
    """A ring of nodes supporting rendezvous hashing based node selection."""
    def __init__(self, nodes=None):

        self.ins = Instanes()
        nodes = self.ins.getInstances()

        nodes = nodes or {}
        self._nodes = set(nodes)


    def add(self, node):
        self._nodes.add(node)

    def nodes(self):
        return self._nodes

    def remove(self, node):
        self._nodes.remove(node)

    def hash(self, key):
        """Return the node to which the given key hashes to."""
        assert len(self._nodes) > 0
        weights = []
        for node in self._nodes:
            n = ip2long(node)

            w = weight(n, key)

            weights.append((w, node))

        _, node = max(weights)

        i= self.ins.getIndex(node)
        i+=1
        i%=self.ins.getLength()
        node2 = self.ins.getInstance(i)

        return node, node2


class Instanes:

    def __init__(self):

        self.instances = r_server.lrange("PORTS", 0, r_server.llen("PORTS"))
        print self.instances

        #tempInstances = set(self.instances)
        #self.instances = list(tempInstances)

    def getInstance(self,i):



        return self.instances[i]

    def getInstances(self):

        return self.instances

    def getLength(self):
        return len(self.instances)

    def getIndex(self, node):
        return self.instances.index(node)