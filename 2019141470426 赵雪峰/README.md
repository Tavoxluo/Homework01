## 如何使用FileSharer

- 运行`/examples/file_sharer.py`中的`__main__`
- ！ 必须在同一局域网内
- 首先，在一台电脑上使用`conn`对一个节点进行初始化
- 然后，用`conn port`对另一台进行初始化
- 接着在前面那台使用`join ip port`连接至另一台主机
- 使用`upload filename`上传一个文件，此时会产生一个`.seed`文件，为种子文件
- 使用`retr seedfile.seed`将文件下载回文件夹内