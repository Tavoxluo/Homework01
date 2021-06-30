import heapq
import time
import operator
import asyncio

from itertools import chain
from collections import OrderedDict
from kademlia.utils import shared_prefix, bytes_to_bit_string


class KBucket:
    def __init__(self, rangeLower, rangeUpper, ksize, replacementNodeFactor=5):
        self.range = (rangeLower, rangeUpper)
        self.nodes = OrderedDict()
        self.replacement_nodes = OrderedDict()
        self.touch_last_updated()
        self.ksize = ksize
        self.max_replacement_nodes = self.ksize * replacementNodeFactor

    def touch_last_updated(self):
        self.last_updated = time.monotonic()

    def get_nodes(self):
        return list(self.nodes.values())

    '''
    将自己的KBucket分裂为两个，以KBucket的中间点为分割点，并将自己所记录的节点与临时节点
    串起来一起分类放入两个分裂得到的KBucket中
    返回这两个KBucket
    （数组套数组型二叉树）
    '''

    def split(self):
        midpoint = (self.range[0] + self.range[1]) // 2
        one = KBucket(self.range[0], midpoint, self.ksize)
        two = KBucket(midpoint + 1, self.range[1], self.ksize)
        nodes = chain(self.nodes.values(), self.replacement_nodes.values())
        for node in nodes:
            bucket = one if node.long_id <= midpoint else two
            bucket.add_node(node)

        return (one, two)

    '''
    移除一个节点：
    如果节点在临时替换节点表中，则直接从临时表中删除
    删除一个节点后从临时替换节点表中得到一个最早的节点加入bucket
    '''

    def remove_node(self, node):
        if node.id in self.replacement_nodes:
            del self.replacement_nodes[node.id]

        if node.id in self.nodes:
            del self.nodes[node.id]

            if self.replacement_nodes:
                newnode_id, newnode = self.replacement_nodes.popitem()
                self.nodes[newnode_id] = newnode

    '''
    检查一个节点是否在这个bucket的范围内
    '''

    def has_in_range(self, node):
        return self.range[0] <= node.long_id <= self.range[1]

    '''
    判断一个节点是否为新的节点
    通过判断它在不在节点列表中
    '''

    def is_new_node(self, node):
        return node.id not in self.nodes

    '''
    添加节点
    '''

    def add_node(self, node):
        """
        Add a C{Node} to the C{KBucket}.  Return True if successful,
        False if the bucket is full.

        If the bucket is full, keep track of node in a replacement list,
        per section 4.1 of the paper.
        """
        # 如果要添加的节点在kbucket中，则将这个节点移动至队尾
        if node.id in self.nodes:
            del self.nodes[node.id]
            self.nodes[node.id] = node
            # 如果这个bucket没满，则直接加入
        elif len(self) < self.ksize:
            self.nodes[node.id] = node
        else:
            """
            OrderedDict.popitem()
            OrderedDict.popitem()有一个可选参数last（默认为True）
            当last为True时它从OrderedDict中删除最后一个键值对并返回该键值对
            当last为False时它从OrderedDict中删除第一个键值对并返回该键值对。
            不指定last（即为True）
            """
            '''
            如果bucket满或者无要添加的节点，则将新发现的节点加入临时的替换节点中
            总是将  最新  的临时替换节点加入
            如果临时替换节点已满，则将最早加入的临时替换节点弹出
            若放入临时替换节点栏则算作加入失败
            '''
            if node.id in self.replacement_nodes:
                del self.replacement_nodes[node.id]
            self.replacement_nodes[node.id] = node
            while len(self.replacement_nodes) > self.max_replacement_nodes:
                self.replacement_nodes.popitem(last=False)
            return False
        return True

    '''
    计算搜索深度？
    '''

    def depth(self):
        vals = self.nodes.values()
        sprefix = shared_prefix([bytes_to_bit_string(n.id) for n in vals])
        return len(sprefix)

    '''
    返回最早节点的信息
    '''

    def head(self):
        return list(self.nodes.values())[0]

    def __getitem__(self, node_id):
        return self.nodes.get(node_id, None)

    def __len__(self):
        return len(self.nodes)


'''
这个类用来遍历一个路由表
'''


class TableTraverser:
    def __init__(self, table, startNode):
        index = table.get_bucket_for(startNode)
        table.buckets[index].touch_last_updated()
        self.current_nodes = table.buckets[index].get_nodes()
        self.left_buckets = table.buckets[:index]
        self.right_buckets = table.buckets[(index + 1):]
        self.left = True

    def __iter__(self):
        return self

    def __next__(self):
        """
        Pop an item from the left subtree, then right, then left, etc.
        """
        # left成员变量用来控制先左后右的遍历顺序
        # 先判断一个Bucket中节点数是否为0，若不为0则弹出这个Bucket中的节点
        # 若为0，则进行先左Bucket再右Bucket的遍历顺序
        if self.current_nodes:
            return self.current_nodes.pop()

        if self.left and self.left_buckets:
            self.current_nodes = self.left_buckets.pop().get_nodes()
            self.left = False
            return next(self)

        if self.right_buckets:
            self.current_nodes = self.right_buckets.pop(0).get_nodes()
            self.left = True
            return next(self)

        raise StopIteration


'''
路由表类
'''


class RoutingTable:
    def __init__(self, protocol, ksize, node):
        """
        @param node: The node that represents this server.  It won't
        be added to the routing table, but will be needed later to
        determine which buckets to split or not.
        """
        self.node = node                                                # 这个代表的是 此路由表由哪个节点掌管
        self.protocol = protocol                                        # 路由表所使用的协议
        self.ksize = ksize                                              # 每个KBucket的最大长度
        self.flush()                                                    # 初始化一个最初的大KBucket

    '''
    初始化时仅有一个大的KBucket，没有被分裂过
    '''

    def flush(self):
        self.buckets = [KBucket(0, 2 ** 160, self.ksize)]

    '''
    分裂一个KBucket
    '''

    def split_bucket(self, index):
        one, two = self.buckets[index].split()
        self.buckets[index] = one
        self.buckets.insert(index + 1, two)

    '''
    获取所有一个小时以上都没有更新过的Bucket
    '''

    def lonely_buckets(self):
        """
        Get all of the buckets that haven't been updated in over
        an hour.
        """
        hrago = time.monotonic() - 3600
        return [b for b in self.buckets if b.last_updated < hrago]

    '''
    很明显这个函数是用来移除一个节点的
    '''

    def remove_contact(self, node):
        index = self.get_bucket_for(node)
        self.buckets[index].remove_node(node)

    '''
    很明显是用来判断一个节点是不是新节点用的
    '''

    def is_new_node(self, node):
        index = self.get_bucket_for(node)
        return self.buckets[index].is_new_node(node)

    '''
    添加一个节点
    '''

    def add_contact(self, node):
        index = self.get_bucket_for(node)
        bucket = self.buckets[index]

        # this will succeed unless the bucket is full
        if bucket.add_node(node):
            return

        '''
        在论文中的4.2节有提到，为了平衡树，二叉树的实现需要进行一些优化，只有在
        特定的情况下才会进行分裂，不会直接分裂，直接分裂导致二叉树过度不平衡，会导致
        算法性能下降，退化为Chrod算法
        '''
        # Per section 4.2 of paper, split if the bucket has the node
        # in its range or if the depth is not congruent to 0 mod 5
        if bucket.has_in_range(self.node) or bucket.depth() % 5 != 0:
            self.split_bucket(index)
            self.add_contact(node)
        else:
            # 节点加入失败会直接ping最早看到的节点
            asyncio.ensure_future(self.protocol.call_ping(bucket.head()))

    '''
    获得一个节点会落到的范围内
    '''

    def get_bucket_for(self, node):
        """
        Get the index of the bucket that the given node would fall into.
        """
        for index, bucket in enumerate(self.buckets):
            if node.long_id < bucket.range[1]:
                return index
        # we should never be here, but make linter happy(sure python is just like my rigid mother)
        return None

    def find_neighbors(self, node, k=None, exclude=None):
        k = k or self.ksize
        nodes = []
        for neighbor in TableTraverser(self, node):
            # 除了与自己为同一台主机与规定了被忽略的节点外
            notexcluded = exclude is None or not neighbor.same_home_as(exclude)
            if neighbor.id != node.id and notexcluded:
                heapq.heappush(nodes, (node.distance_to(neighbor), neighbor))
            # 找到k个最近的邻居节点后结束循环
            if len(nodes) == k:
                break
        # 返回在k个节点中距离最小的那个节点
        return list(map(operator.itemgetter(1), heapq.nsmallest(k, nodes)))
