import time
from itertools import takewhile
import operator
from collections import OrderedDict
from abc import abstractmethod, ABC


class IStorage(ABC):
    """
    Local storage for this node.
    IStorage implementations of get must return the same type as put in by set
    """

    @abstractmethod
    def __setitem__(self, key, value):
        """
        Set a key to the given value.
        """

    @abstractmethod
    def __getitem__(self, key):
        """
        Get the given key.  If item doesn't exist, raises C{KeyError}
        """

    @abstractmethod
    def get(self, key, default=None):
        """
        Get given key.  If not found, return default.
        """

    @abstractmethod
    def iter_older_than(self, seconds_old):
        """
        Return the an iterator over (key, value) tuples for items older
        than the given secondsOld.
        """

    @abstractmethod
    def __iter__(self):
        """
        Get the iterator for this storage, should yield tuple of (key, value)
        """


class ForgetfulStorage(IStorage):
    """
    这个类用来存储节点中的文件，节点中一些文件需要定期被刷新，默认这个过期时间为一周
    """
    def __init__(self, ttl=604800):
        """
        By default, max age is a week.
        """
        self.data = OrderedDict()
        self.ttl = ttl

    def __setitem__(self, key, value):
        if key in self.data:
            del self.data[key]
        self.data[key] = (time.monotonic(), value)
        self.refresh()

    def refresh(self):
        # 将过期的key/value重新放入
        for _, _ in self.iter_older_than(self.ttl):
            item = self.data.popitem(last=False)
            self.data[item[0]] = (time.monotonic(), item[1])

    def get(self, key, default=None):
        # 每次获取时都要进行刷新，会将过期的删除
        self.refresh()
        if key in self.data:
            return self[key]
        return default

    def __getitem__(self, key):
        self.refresh()
        return self.data[key][1]

    def __repr__(self):
        self.refresh()
        return repr(self.data)

    def iter_older_than(self, seconds_old):
        """
        用于返回未刷新时长比seconds_old还要晚的key/value
        """
        # 先计算出second_old以前的时间
        min_birthday = time.monotonic() - seconds_old
        zipped = self._triple_iter()
        # 比这个刷新时间比这个时间早的即为符合条件的
        matches = takewhile(lambda r: min_birthday >= r[1], zipped)
        return list(map(operator.itemgetter(0, 2), matches))

    def _triple_iter(self):
        ikeys = self.data.keys()
        ibirthday = map(operator.itemgetter(0), self.data.values())
        ivalues = map(operator.itemgetter(1), self.data.values())
        return zip(ikeys, ibirthday, ivalues)

    def __iter__(self):
        self.refresh()
        ikeys = self.data.keys()
        ivalues = map(operator.itemgetter(1), self.data.values())
        return zip(ikeys, ivalues)
