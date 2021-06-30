from collections import Counter
import logging

from kademlia.node import Node, NodeHeap
from kademlia.utils import gather_dict

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

'''
这个协议的实现将整个核心的node lookup的过程封装成了一个类
'''


# pylint: disable=too-few-public-methods
class SpiderCrawl:
    """
    Crawl the network and look for given 160-bit keys.
    """

    def __init__(self, protocol, node, peers, ksize, alpha):
        """
        Create a new C{SpiderCrawl}er.

        Args:
            protocol: A :class:`~kademlia.protocol.KademliaProtocol` instance.
            node: A :class:`~kademlia.node.Node` representing the key we're
                  looking for
            peers: A list of :class:`~kademlia.node.Node` instances that
                   provide the entry point for the network
            ksize: The value for k based on the paper
            alpha: The value for alpha based on the paper
        """
        self.protocol = protocol
        self.ksize = ksize
        self.alpha = alpha  # 论文中的alpha值
        self.node = node  # 自己
        self.nearest = NodeHeap(self.node, self.ksize)  # k个最近的节点
        self.last_ids_crawled = []  # 上次递归询问的节点
        log.info("creating spider with peers: %s", peers)
        self.nearest.push(peers)

    async def _find(self, rpcmethod):
        """
        Get either a value or list of nodes.

        Args:
            rpcmethod: The protocol's call_find_Value or call_find_node.

        The process:
          1. calls find_* to current ALPHA nearest not already queried nodes,
             adding results to current nearest list of k nodes.
          2. current nearest list needs to keep track of who has been queried
             already sort by nearest, keep KSIZE
          3. if list is same as last time, next call should be to everyone not
             yet queried
          4. repeat, unless nearest list has all been queried, then ur done
        """
        log.info("crawling network with nearest: %s", str(tuple(self.nearest)))
        # 从k个距离自己最近的节点中选出alpha个节点来询问，若最近的k个节点中
        # 没有比最近的还要近的（即最近一次的询问并没有刷新最近节点），则直接
        # 全部询问
        count = self.alpha
        if self.nearest.get_ids() == self.last_ids_crawled:
            count = len(self.nearest)
        self.last_ids_crawled = self.nearest.get_ids()

        dicts = {}
        # "await func()"是一个协程对象，这个函数返回的是协程
        for peer in self.nearest.get_uncontacted()[:count]:
            # 将即将被查询的节点与查询这个节点的异步过程放入一个dict中
            # 并将其标记为已经看到过的节点
            dicts[peer.id] = rpcmethod(peer, self.node)
            self.nearest.mark_contacted(peer)
        # 使用gather_dict函数异步执行对所有节点的询问，并将每个节点的询问
        # 结果对应地放入字典中
        found = await gather_dict(dicts)
        # 处理find_node与find_value得到的节点
        return await self._nodes_found(found)

    async def _nodes_found(self, responses):
        raise NotImplementedError


class ValueSpiderCrawl(SpiderCrawl):
    """
    这个类用来处理find_value调用时所返回的节点
    """

    def __init__(self, protocol, node, peers, ksize, alpha):
        SpiderCrawl.__init__(self, protocol, node, peers, ksize, alpha)
        # keep track of the single nearest node without value - per
        # section 2.3 so we can set the key there if found
        self.nearest_without_value = NodeHeap(self.node, 1)

    async def find(self):
        """
        Find either the closest nodes or the value requested.
        """
        return await self._find(self.protocol.call_find_value)

    async def _nodes_found(self, responses):
        """
        Handle the result of an iteration in _find.
        """
        toremove = []
        found_values = []
        for peerid, response in responses.items():
            response = RPCFindResponse(response)
            if not response.happened():
                # 若某个节点没有即使应答，则将其加入即将被移除的列表中
                toremove.append(peerid)
            elif response.has_value():
                # 若这个节点返回了一个有被查询的值的应答，则将这个应答的
                # 值加入列表中
                found_values.append(response.get_value())
            else:
                # 若有应答但没有查询到值，则将被查询的节点放入无值的列表中
                # 将返回的所有的节点信息存入最近节点中
                peer = self.nearest.get_node(peerid)
                self.nearest_without_value.push(peer)
                self.nearest.push(response.get_node_list())
        self.nearest.remove(toremove)

        if found_values:
            # 处理已查询到的值
            return await self._handle_found_values(found_values)
        if self.nearest.have_contacted_all():
            # not found!
            return None
        return await self.find()

    async def _handle_found_values(self, values):
        """
        We got some values!  Exciting.  But let's make sure
        they're all the same or freak out a little bit.  Also,
        make sure we tell the nearest node that *didn't* have
        the value to store it.
        检查一个得到的值是否正确
        告诉没有这个值的节点存储这个值
        """
        value_counts = Counter(values)
        # 若获得了多个值，则在这多个值中获取最普遍存储的
        if len(value_counts) != 1:
            log.warning("Got multiple values for key %i: %s",
                        self.node.long_id, str(values))
        value = value_counts.most_common(1)[0][0]
        # 若在最近的节点中有没存储这个值的节点，则将这个值存入他们的存储中
        peer = self.nearest_without_value.popleft()
        if peer:
            await self.protocol.call_store(peer, self.node.id, value)
        return value


class NodeSpiderCrawl(SpiderCrawl):
    """
    用于爬取在网络上的节点
    """

    async def find(self):
        """
        Find the closest nodes.
        """
        return await self._find(self.protocol.call_find_node)

    async def _nodes_found(self, responses):
        """
        Handle the result of an iteration in _find.
        """
        toremove = []
        for peerid, response in responses.items():
            response = RPCFindResponse(response)
            # 如果在发送find_node请求后没有回复，则说明这个节点已经不在线，需要从最近的节点中删除
            if not response.happened():
                toremove.append(peerid)
            else:
                self.nearest.push(response.get_node_list())
        self.nearest.remove(toremove)

        # 若在最近的节点中所有的节点都被询问过了，则递归结束
        if self.nearest.have_contacted_all():
            return list(self.nearest)
        return await self.find()


class RPCFindResponse:
    """
    处理RPC在收到回复后回复的内容
    """

    def __init__(self, response):
        """
        A wrapper for the result of a RPC find.

        Args:
            response: This will be a tuple of (<response received>, <value>)
                      where <value> will be a list of tuples if not found or
                      a dictionary of {'value': v} where v is the value desired
        """
        self.response = response

    def happened(self):
        """
        Did the other host actually respond?
        检查被查询的节点是否响应
        """
        return self.response[0]

    def has_value(self):
        return isinstance(self.response[1], dict)

    def get_value(self):
        return self.response[1]['value']

    def get_node_list(self):
        """
        Get the node list in the response.  If there's no value, this should
        be set.
        """
        nodelist = self.response[1] or []
        return [Node(*nodeple) for nodeple in nodelist]
