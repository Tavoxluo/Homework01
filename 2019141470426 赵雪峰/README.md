## 如何使用FileSharer

- 运行`/examples/file_sharer.py`中的`__main__`
- ！ 必须在同一局域网内
- ！ 千万不要在同一个pycharm中开两个终端运行（血与泪的教训）
- 首先，在一台电脑上使用`conn`对一个节点进行初始化
- 然后，用`conn port`对另一台进行初始化
- 接着在前面那台使用`join ip port`连接至另一台主机
- 使用`upload filename`上传一个文件，此时会产生一个`.seed`文件，为种子文件
- 使用`retr seedfile.seed`将文件下载回文件夹内

可以使用文件“kademlia实现分析”进行测试。

经常连不上可以试试更改rpcudp的声明中的超时时长。

## 开发日志

[ ] 传回文件后文件失序，有bug
[+] 实现基本的传输
