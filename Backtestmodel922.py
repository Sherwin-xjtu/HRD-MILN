import os
import datetime
import numpy as np
import pandas as pd
from multiprocessing import Pool, Manager
import traceback

# useFeatures = []
# with open("E:/stock_predict/stock_data/20200922/config/use_feature.txt", "r") as fin:
#     for line in fin:
#         useFeatures.append(line.strip("\n"))


def formatOrderTime(orderTime):
    return int(orderTime.strftime("%H%M%S") + "000")


def initOrderDetails():
    orderDetails = pd.DataFrame(pd.date_range("9:31", "14:56", freq="60S"), columns=['orderTime'])
    orderDetails["orderTime"] = orderDetails["orderTime"].apply(lambda item: formatOrderTime(item))
    am = (orderDetails["orderTime"] >= 93000000) & (orderDetails["orderTime"] < 113000000)
    pm = (orderDetails["orderTime"] >= 130000000) & (orderDetails["orderTime"] < 150000000)
    orderDetails = orderDetails[am | pm]
    orderDetails.reset_index(inplace=True, drop=True)
    return orderDetails


def getRealRatio(tick, orderTime):
    tickUse = tick[tick["MDTime"] >= orderTime]
    ratio = 0
    if len(tickUse) >= 21:
        tickUsing = tickUse.iloc[0: 21, :]
        tickUsing.reset_index(drop=True, inplace=True)
        lastPXs = tickUsing["Sell1Price"].tolist()
        firstLastPx = lastPXs[0]
        ratio = (lastPXs[-1] - firstLastPx) / firstLastPx
    return ratio


def runModel(info):
    try:
        code, date, commonBp, marketPrice, period, res = info
        symbol = code.split(".")[0]
        predValue = pd.read_csv(f"./pred/rnn_2_3264/{code}/pred_{date}_{symbol}.csv", encoding="gb2312")
        predValue["orderTime"] = predValue["orderTime"].astype(int)
        orderTimeIndexs = predValue["orderTime"].tolist()
        predValue.set_index("orderTime", inplace=True)
        tick = pd.read_csv(f"./stock_predict/data/{code}/{date}_{symbol}.csv", encoding="gb2312")
        tick = tick[((tick["MDTime"] >= 93000000) & (tick["MDTime"] <= 113000000)) | (
                (tick["MDTime"] >= 130000000) & (tick["MDTime"] <= 145700000))]
        tick["tickVolume"] = tick["TotalVolumeTrade"].diff(1)
        tick.dropna(inplace=True)
        tick.reset_index(drop=True, inplace=True)
        orderDetails = initOrderDetails()

        orderPxs = []
        orderQtys = [2000 for i in range(len(orderDetails))]
        switch = [True for i in range(len(orderDetails))]
        correct = 0
        sumNum = 0
        cnt = 0
        deltaQty = 2000
        for key, row in orderDetails.iterrows():
            partTick = tick[tick["MDTime"] <= row["orderTime"]]
            orderPx = partTick.at[partTick.index[-1], "Sell1Price"]
            orderPxs.append(orderPx)

            if switch[cnt] and cnt + (period + 1) <= len(orderDetails):
                predictValue = 0
                if row["orderTime"] in orderTimeIndexs:
                    predictValue = predValue.at[row["orderTime"], "proba"]

                if predictValue > 0.5:
                    orderQtys[cnt] = orderQtys[cnt] + deltaQty
                    if orderQtys[cnt + period] >= deltaQty:
                        orderQtys[cnt + period] = orderQtys[cnt + period] - deltaQty
                    realRatio = getRealRatio(tick, row["orderTime"])
                    if realRatio > 0:
                        correct += 1
                    if realRatio != 0:
                        sumNum += 1
                elif predictValue < 0.5:
                    if orderQtys[cnt] >= deltaQty:
                        orderQtys[cnt] = orderQtys[cnt] - deltaQty
                        orderQtys[cnt + period] = orderQtys[cnt + period] + deltaQty
                    realRatio = getRealRatio(tick, row["orderTime"])
                    if realRatio < 0:
                        correct += 1
                    if realRatio != 0:
                        sumNum += 1
            cnt += 1

        orderPriceDf = pd.DataFrame(np.array(orderPxs), columns=["orderPrice"])
        orderQtyDf = pd.DataFrame(np.array(orderQtys), columns=["orderQty"])
        orderDetails = pd.concat([orderDetails, orderPriceDf, orderQtyDf], axis=1)
        orderError = orderDetails[orderDetails["orderPrice"] == 0]
        if len(orderError) == 0:
            # orderDetails.to_csv(f"order/{date}_{symbol}.csv", index=False, encoding="gb2312")
            modelPx = (orderDetails["orderPrice"] * orderDetails["orderQty"]).sum() / orderDetails["orderQty"].sum()
            modelBp = (marketPrice - modelPx) / marketPrice * 10000

            acc = 0
            if sumNum > 0:
                acc = correct / sumNum

            res.append([code, date, commonBp, modelBp, modelBp - commonBp, correct, sumNum, acc, period])
            print(code, date)

    except Exception as e:
        # print(str(e))
        traceback.print_exc()


if __name__ == "__main__":
    p = Pool()
    tasks = []
    res = Manager().list()

    benchmark = pd.read_excel("benchmark.xlsx")
    benchmark = benchmark[benchmark["Date"] >= 20200610]
    benchmark.reset_index(inplace=True, drop=True)

    result = []
    for key, row in benchmark.iterrows():
        for period in [1]:
            code = row["symbol"]
            date = row["Date"]
            marketPrice = row["marketPx"]
            commonBp = row["bp"]
            if os.path.exists(f"./pred/rnn_2_3264/{code}/pred_{date}_{code.split('.')[0]}.csv"):
                tasks.append((code, date, commonBp, marketPrice, period, res))
    p.map(runModel, tasks)

    resultDf = pd.DataFrame(np.array(list(res)), columns=["code", "date", "commonBp", "modelBp", "bpdiff", "correct", "sumNum", "Acc", "Period"])
    resultDf.to_csv("./result/rnn_2_3264.csv", encoding="gb2312", index=False)
