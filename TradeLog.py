import json
import os
import pathlib
from pprint import pprint

class TradeLog:
    def __init__(self, filepath:str="./交易日志.json") -> None:
        self.__filepath:str = filepath

        if os.path.exists(self.__filepath):
            pass
        else:
            pathlib.Path(self.__filepath).touch(exist_ok=True)

        file = open(self.__filepath, encoding="utf-8", mode="r")
        self.__data:dict[str, list[dict[str, str]]] = json.load(file)
        file.close()
        print("DATA load SUCCESS!")

        return

    def __create_single_log(self, dt:str="NULL", ticker:str="NULL", desc:str="NULL") -> dict[str, str]:
        tmp:dict[str, str] = {
            "dt":dt,
            "ticker":ticker,
            "desc":desc
        }
        for it in tmp:
            assert type(it) is str, "Log必须为字符串!"

        return tmp

    def head(self, symbol:str, index:int=6) -> None:
        """
        Print 1st-N records for symbol. Index better be <= 20
        """
        assert symbol in self.__data.keys(), f"一级索引{symbol}不存在, 请使用gen_symbol方法创建!"
        for it in self.__data[symbol][:index]:
            pprint(it, indent=4, width=80, compact=False, sort_dicts=False)

        return

    def tail(self, symbol:str, index:int=6) -> None:
        """
        Print LAST 1st-N records for symbol. Index better be <= 20
        """
        assert symbol in self.__data, f"一级索引{symbol}不存在, 请使用gen_symbol方法创建!"
        for it in self.__data[symbol][-index:]:
            pprint(it, indent=4, width=80, compact=False, sort_dicts=False)

        return

    def gen_symbol(self, symbol:str) -> None:
        """
        Create symbol as 1st class index
        """
        assert type(symbol) is str, f"{symbol}必须为字符串!"
        assert symbol not in self.__data.keys(), f"一级索引{symbol}已存在!"
        self.__data[symbol] = []

        return

    def gen_log(self, symbol:str="NULL", dt:str="NULL", ticker:str="NULL", desc:str="NULL") -> None:
        """
        Used to create trade log.
        param->symbol: string for ticker parent, e.g. 豆油, 工商银行A股
        param->dt: ISO string for datetime with timezone, e.g. 2023-07-28 11:30:00+08:00
        param->ticker: string of ticker, e.g. DCE.y2309, SH.600388
        param->desc: string of comment for trade log, e.g. I WAKE UP 8AM TODAY
        """
        log:dict[str, str] = self.__create_single_log(dt, ticker, desc)
        print(f"Trade Log create with SUCCESS:\ndt: {dt}\nticker: {ticker}\ndesc: {desc}\n-------------------------")

        assert symbol in self.__data.keys(), f"一级索引{symbol}不存在, 请使用gen_symbol方法创建!"
        self.__data[symbol].append(log)

        return

    def modify_log(self, symbol:str, index:int=-1, dt:str="NULL", ticker:str="NULL", desc:str="NULL") -> None:
        """
        Modify log if necessary
        param->symbol: 1st class indexing for log to be modified
        param->index: standard python list index, this method will use sample_list[index] to locate log, default as -1
        """
        assert symbol in self.__data.keys(), f"一级索引{symbol}不存在, 请使用gen_symbol方法创建!"
        assert type(index) is int, "param->index MUST BE INT!"

        self.__data[symbol][index] = self.__create_single_log(dt, ticker, desc)

        return

    def dump_log(self) -> None:
        file = open(self.__filepath, encoding="utf-8", mode="w")
        json.dump(self.__data, file, ensure_ascii=False, indent=4, allow_nan=True)
        print("Trade Log extract with SUCCESS!")

        file.close()
        print("File connection closed!")

        return

    def sort(self, symbol:str, reverse:bool=False) -> None:
        """
        Sort from past to now for logs under given 1st class
        param->symbol: str for 1st class index
        param->reverse: sort ASC(False) or DESC(True)
        """
        assert symbol in self.__data.keys(), f"一级索引{symbol}不存在, 请使用gen_symbol方法创建!"
        tmp:list[dict[str, str]] = self.__data[symbol]

        tmp.sort(key=lambda x: x["dt"], reverse=reverse)
        self.__data[symbol] = tmp

        return

    def list_symbol(self, n:int=0) -> list[str]:
        """
        List 1st class index for current log
        param->n: number of 1st class index to show. If 0 then show all
        """
        assert type(n) is int, "param->n MUST BE INT!"
        assert n >= 0, "Error, param->n MUST >= 0!"

        otpt:list[str] = []

        for k, _ in self.__data.items():
            otpt.append(k)

        if n == 0:
            return otpt
        else:
            return otpt[:n]

    def list_ticker(self, symbol:str, n:int=0) -> list[str]:
        """
        List ticker under 1st class index
        param->symbol: 1st class index name
        param->n: number of tickers to show
        """
        assert type(symbol) is str, "Error, param->symbol MUST BE str!"
        assert type(n) is int, "Error, param->n MUST BE int!"
        assert n >= 0, "Error, param->n MUST >= 0!"
        assert symbol in self.__data.keys(), f"一级索引{symbol}不存在, 请使用gen_symbol方法创建!"

        tmp:set[str] = set([x["ticker"] for x in self.__data[symbol]])
        otpt:list[str] = list(tmp)

        if n == 0:
            return otpt
        else:
            return otpt[:n]

    def find_log(self, symbol:str, start:str, end:str, sort:bool=False) -> list[dict[str, str]]:
        """
        Find log under 1st class index, during time interval [start, end], including both side
        Complexity is O(n-m), enough for a typical log file
        param->symbol: 1st class index name
        param->start: start time, should be in format like 2023-08-15 09:00:00+08:00
        param->end: end time, should be in format like 2023-08-15 09:00:00+08:00
        param->sort: if need to sort log before searching. As normal log file is born to be sorted, default as False
        """
        assert start <= end, "Error, start timestamp MUST <= end timestamp!"
        assert symbol in self.__data.keys(), f"一级索引{symbol}不存在, 请使用gen_symbol方法创建!"
        otpt:list[dict[str, str]] = []
        if sort == True:
            self.sort(symbol, False)

        tmp:list[dict[str, str]] = self.__data[symbol]
        for it in tmp:
            if it["dt"] < start:
                pass
            elif it["dt"] >= start and it["dt"] <= end:
                otpt.append(it)
            else:
                break

        return otpt

    def find_log_desc(self, symbol:str, pattern:str) -> list[dict[str, str]]:
        """
        Find log with certain words in desc, under 1st class index
        Complexity is O(n)
        param->symbol: 1st class index name
        param->pattern: words need to be included in desc
        """
        assert type(symbol) is str
        assert type(pattern) is str
        assert len(pattern) > 0, "Error, search with empty str is not allowed!"
        assert symbol in self.__data.keys(), f"一级索引{symbol}不存在, 请使用gen_symbol方法创建!"
        otpt:list[dict[str, str]] = []

        for it in self.__data[symbol]:
            if it["desc"].__contains__(pattern):
                otpt.append(it)
            else:
                pass

        return otpt
