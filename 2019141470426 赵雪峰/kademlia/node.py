from operator import itemgetter
import heapq


class Node:
    """
    Simple object to encapsulate the concept of a Node (minimally an ID, but
    also possibly an IP and port if this represents a node on the network).
    This class should generally not be instantiated directly, as it is a low
    level construct mostly used by the router.
    节点的底层实现，仅从数据与基本的操作上表示一个节点，在实际中不会单独进行实例化。
    """

    def __init__(self, node_id, ip=None, port=None):
        """
        Create a Node instance.

        Args:
            node_id (int): A value between 0 and 2^160
            ip (string): Optional IP address where this Node lives
            port (int): Optional port for this Node (set when IP is set)
        """
        self.id = node_id  # pylint: disable=invalid-name
        self.ip = ip  # pylint: disable=invalid-name
        self.port = port
        self.long_id = int(node_id.hex(), 16)

    def same_home_as(self, node):
        """
        检测一个节点是否跟自己是同一个主机
        """
        return self.ip == node.ip and self.port == node.port

    def distance_to(self, node):
        """
        Get the distance between this node and another.
        获得一个节点与自己的异或距离
        """
        return self.long_id ^ node.long_id

    def __iter__(self):
        """
        Enables use of Node as a tuple - i.e., tuple(node) works.
        在迭代时返回的元组格式
        """
        return iter([self.id, self.ip, self.port])

    def __repr__(self):
        return repr([self.long_id, self.ip, self.port])

    def __str__(self):
        return "%s:%s" % (self.ip, str(self.port))


class NodeHeap:
    """
    A heap of nodes ordered by distance to a given node.
    一个根据距离排列节点的堆
    """

    def __init__(self, node, maxsize):
        """
        Constructor.

        @param node: The node to measure all distnaces from.拥有这个堆的节点
        @param maxsize: The maximum size that this heap can grow to.堆中节点数最大值
        """
        self.node = node
        self.heap = []
        self.contacted = set()
        self.maxsize = maxsize

    def remove(self, peers):
        """
        Remove a list of peer ids from this heap.  Note that while this
        heap retains a constant visible size (based on the iterator), it's
        actual size may be quite a bit larger than what's exposed.  Therefore,
        removal of nodes may not change the visible size as previously added
        nodes suddenly become visible.
        """
        # 这里的peers参数应为一个节点id的元组
        peers = set(peers)
        if not peers:
            return
        nheap = []
        for distance, node in self.heap:
            # 选出那些不在需要删除的节点数组中的节点，将它们加入到nheap中
            # 再用nheap代替heap，以此达到删除peers中节点的目的
            if node.id not in peers:
                heapq.heappush(nheap, (distance, node))
        self.heap = nheap

    def get_node(self, node_id):
        """
        通过节点的id在这个节点堆中获取到一个节点，若在这个堆中无要查询的节点，则返回None
        """
        for _, node in self.heap:
            if node.id == node_id:
                return node
        return None

    def have_contacted_all(self):
        """
        检查这个堆中的节点是否都已联系过，即是否可以连接通
        """
        return len(self.get_uncontacted()) == 0

    def get_ids(self):
        return [n.id for n in self]

    def mark_contacted(self, node):
        """
        通过id将一个节点标记为已连接过的，即将已连接过的节点加入到已连接过的节点的数组中
        """
        self.contacted.add(node.id)

    def popleft(self):
        """
        若自己保存的节点数不为空，则返回最早联系过的节点
        """
        return heapq.heappop(self.heap)[1] if self else None

    def push(self, nodes):
        """
        Push nodes onto heap.

        @param nodes: This can be a single item or a C{list}.
        """
        if not isinstance(nodes, list):
            # 如果不是一个list则将它转化为list存储的形式
            nodes = [nodes]

        for node in nodes:
            # 将在nodes中的所有节点存入自己的节点堆中
            if node not in self:
                distance = self.node.distance_to(node)
                # 这里可以保证节点堆有序
                heapq.heappush(self.heap, (distance, node))

    def __len__(self):
        return min(len(self.heap), self.maxsize)

    def __iter__(self):
        """
        迭代函数返回在保存的节点堆中距离自己最近的节点
        """
        nodes = heapq.nsmallest(self.maxsize, self.heap)
        return iter(map(itemgetter(1), nodes))

    def __contains__(self, node):
        """
        检测一个节点是否在自己保存的节点堆中
        """
        for _, other in self.heap:
            if node.id == other.id:
                return True
        return False

    def get_uncontacted(self):
        """
        获得没有连接过的节点，即从所有自己保存的节点中不在已连接过的节点数组中的节点
        """
        return [n for n in self if n.id not in self.contacted]
