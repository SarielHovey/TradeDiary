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
本工具最终会输出并管理存放在本地的`json`文件, 文件结构如下:
```
{
    "豆油": [
        {
            "dt": "2023-07-28 11:30:00+08:00",
            "symbol": "DCE.y2309",
            "desc": "XXXXXXXX"
        },
        {
            "dt": "2023-07-28 15:00:00+08:00",
            "symbol": "DCE.y2309",
            "desc": "XXXXXXXXX"
        }
    ],
    "工商银行A股": [
        {
            "dt": "2023-07-28 11:30:00+08:00",
            "symbol": "SH.601398",
            "desc": "XXXXXXXX"
        }
    ]
}
```
### 效能问题
本工具会使用Python的`open()`函数将json文件整个读入内存<br>
考虑到txt格式的网络小说连载多年也是20MB顶天的大小, 难以想象会有逆天用户写出超过100MB的交易日志<br>
如果发生, 建议你不要做单了, 改行去写网文吧<br>
每年可以单独建立一个json日志, 加快索引速度<br>
