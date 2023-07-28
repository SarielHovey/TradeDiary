import os
import pathlib
import json
from pprint import pprint

class TradeLog:
    def __init__(self, filepath:str="D:/TradeLog_2023.json") -> None:
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
        assert symbol in self.__data, f"一级索引{symbol}不存在, 请使用gen_symbol方法创建!"
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
        assert symbol not in self.__data, f"一级索引{symbol}已存在!"
        self.__data[symbol] = []

        return

    def gen_log(self, symbol:str="NULL", dt:str="NULL", ticker:str="NULL", desc:str="NULL") -> None:
        """
        Used to create trade log.
        symbol: string for ticker parent, e.g. 豆油, 工商银行A股
        dt: ISO string for datetime with timezone, e.g. 2023-07-28 11:30:00+08:00
        ticker: string of ticker, e.g. DCE.y2309, SH.600388
        desc: string of comment for trade log, e.g. I WAKE UP 8AM TODAY
        """
        log:dict[str, str] = self.__create_single_log(dt, ticker, desc)
        print(f"Trade Log create with SUCCESS:\ndt: {dt}\nticker: {ticker}\ndesc: {desc}\n-------------------------")

        assert symbol in self.__data, f"一级索引{symbol}不存在, 请使用gen_symbol方法创建!"
        self.__data[symbol].append(log)

        return

    def modify_log(self, symbol:str, index:int=-1, dt:str="NULL", ticker:str="NULL", desc:str="NULL") -> None:
        """
        Modify log if necessary
        symbol: 1st class indexing for log to be modified
        index: standard python list index, this method will use sample_list[index] to locate log, default as -1
        """
        assert symbol in self.__data, f"一级索引{symbol}不存在, 请使用gen_symbol方法创建!"
        assert type(index) is int, "param:index MUST BE INT!"

        self.__data[symbol][index] = self.__create_single_log(dt, ticker, desc)

        return

    def dump_log(self) -> None:
        file = open(self.__filepath, encoding="utf-8", mode="w")
        json.dump(self.__data, file, ensure_ascii=False, indent=4, allow_nan=True)
        file.close()
        print("Trade Log extract with SUCCESS!")

        return
