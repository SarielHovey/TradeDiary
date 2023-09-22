# TradeLog
A trading logging tool
## 描述
个人自用的交易日志工具, 收盘后用于记录复盘的想法和对下个交易日的计划<br>
没有多少技术含量, 过于落后, 方便开源<br>
### 为什么不掏本笔记本直接写?
21世纪了, 纸笔的读取和输出带宽低到无法容忍, 1秒顶天写2个字<br>
数字化存储便于日后索引查找, 也不用浪费时间手写, 时代变了大人<br>
## 免责声明
由于你赚了钱也不会分我, 所以本工具造成的任何问题, 本人概不负责<br>
## 使用环境要求
首先, 需要`Python ver >= 3.9`<br>
其次, 本工具完全基于Python内置包`json`和`pprint`; 如果`import`发生错误, 建议反思一下Python安装是否正确<br>
## 数据结构
本工具最终会输出并管理存放在本地的`json`文件, 文件结构为
```python
dict[str, list[dict[str, str]]]
```
这对应了一级索引 -> 日志 -> 日志内容的三层结构
具体示例如下:
```python
{
    "豆油": [
        {
            "dt": "2023-07-28 11:30:00+08:00",
            "ticker": "DCE.y2309",
            "desc": "XXXXXXXX"
        },
        {
            "dt": "2023-07-28 15:00:00+08:00",
            "ticker": "DCE.y2309",
            "desc": "XXXXXXXXX"
        }
    ],
    "工商银行A股": [
        {
            "dt": "2023-07-28 11:30:00+08:00",
            "ticker": "SH.601398",
            "desc": "XXXXXXXX"
        }
    ]
}
```
很显然的, 一个日志包括3个必须的元素作为内容:
```
dt: 收盘时间戳, 在同一个日志文件内务必保持同样的格式
ticker: 证券代码
desc: 你写的东西
```
### 效能问题
本工具会使用Python的`open()`函数将json文件整个读入内存<br>
考虑到txt格式的网络小说连载多年也是20MB顶天的大小, 难以想象会有逆天用户写出超过100MB的交易日志<br>
如果发生, 建议你不要做单了, 改行去写网文吧<br>
每年可以单独建立一个json日志, 加快索引速度<br>
## 使用方法
1. 读取Log文件<br>
`tl = TradeLog("D:/sampleLog.json")`
2. 查阅某标的最近的几条Log<br>
`tl.tail("工商银行A股", 6)`
3. 插入Log<br>
```python
dt = "2023-07-28 11:30:00+08:00"
ticker = "SH.601398"
desc = "我不炒股, 你看着办"
tl.gen_log("工商银行A股", dt, ticker, desc)
```
4. 修改Log<br>
```python
tl.modify_log("工商银行A股", -1, dt, ticker, desc)
```
5. 保存Log<br>
必须调用此方法才能最终写入文件. 建议在修改完确认后, 在结束工作前一次性写入<br>
```python
tl.dump_log()
```
6. 查看某一级索引最早的7条Log<br>
```python
tl.head("工商银行A股", 7)
```
7. 查看某一级索引最近的7条Log<br>
```python
tl.tail("工商银行A股", 7)
```
* 值得留意的是, `v1.1.0`版本增加了以下新的功能, 便于快速翻阅日志(比手写在纸上爽多了有没有)<br>
8. 重新按照时间戳`dt`排序Log<br>
```python
# 如果出于各种原因, 你弄乱了工商银行A股的日志, 使用以下方法从过去到现在重新排序日志
tl.sort("工商银行A股", reverse=False)
```
9. 获取所有的一级索引<br>
```python
tl.list_symbol()
```
10. 获取一级索引下所有的ticker<br>
```python
tl.list_ticker("豆油")
```
11. 获取一级索引下, 从某时间点到某时间点的Log<br>
```python
tl.find_log("豆油", "2023-07-25 11:30:00+08:00", "2023-08-31 23:00:00+08:00")
```
12. 获取一级索引下, 含有特定词语的Log<br>
```python
# 举例, 搜索工商银行A股所有含有"变成韭菜亏死了"这句话的Log
tl.find_log("工商银行A股", "变成韭菜亏死了")
```
