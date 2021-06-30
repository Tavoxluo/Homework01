"""
General catchall for functions that don't make sense as methods.
"""
import hashlib
import operator
import asyncio


async def gather_dict(dic):
    """
    异步执行一个任务字典中的所有任务，并将执行得到的结果与key对应，返回一个（key，任务结果的字典）
    """
    # 将任务字典中的任务全部取出
    cors = list(dic.values())
    # gather函数可以用来执行一组任务 执行传入的任务字典中的所有任务
    results = await asyncio.gather(*cors)
    # zip可以将iterable对象中的元素一一取出，组成元组 将任务结果与任务的key对应
    return dict(zip(dic.keys(), results))


def digest(string):
    """
    将一个字符串（byte类型）转化为这个字符串的sha1哈希码
    """
    if not isinstance(string, bytes):
        # 若这个字符串不是byte类型的字符串，则将这个字符串转化为utf-8编码的byte类型的字符串
        string = str(string).encode('utf8')
        # 返回这个byte类型字符串的sha1哈希值
    return hashlib.sha1(string).digest()


def shared_prefix(args):
    """
    Find the shared prefix between the strings.
    找到一组字符串（list类型）中的最长前缀
    For instance:

        sharedPrefix(['blahblah', 'blahwhat'])

    returns 'blah'.
    """
    i = 0
    # 确定这组字符串中最短的字符串长度
    while i < min(map(len, args)):
        # operator.itemgetter(int) 返回一个函数，用于取出这个函数的参数（一个iterable对象）中的第int个量
        # 一个巧妙的比较方法：上面的步骤后可以取出n个字母（n为args中字符串数量，这n个字母为这些字符串在
        # 第i个位置上的字母），将这些字母放入一个集合中，若集合的长度不为1，则说明在这个位置上，字符串
        # 出现了不同。
        if len(set(map(operator.itemgetter(i), args))) != 1:
            break
        i += 1
        # 返回最长前缀
    return args[0][:i]


def bytes_to_bit_string(bites):
    """
    将bites中所有字符串的二进制形式从第三位开始分割开，
    若得到的二进制形式不满8位则补0右对齐，若满8位则直接返回
    """
    bits = [bin(bite)[2:].rjust(8, '0') for bite in bites]
    return "".join(bits)
