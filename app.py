import streamlit as st
import pandas as pd
import backtrader as bt
import matplotlib.pyplot as plt

# Streamlitのページ設定
st.set_page_config(page_title="Backtrader Strategy with Streamlit", layout="wide")

# タイトルと説明を表示
st.title("Backtrader Strategy with Streamlit")
st.write("This is a sample Streamlit app to demonstrate a Backtrader strategy.")

# ファイルアップロード機能
uploaded_file = st.file_uploader("Choose a file", type=["csv"])

if uploaded_file is not None:
    # ヒストリカルデータを読み込み
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded data:", data.head())

    # 正しいカラム名を設定
    data.columns = ['datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
    data['datetime'] = pd.to_datetime(data['datetime'])
    data.set_index('datetime', inplace=True)
    data = data.dropna()

    # データを表示
    st.write("Prepared data:", data.head())

    # Backtraderの戦略を定義
    class FibonacciStrategy(bt.Strategy):
        params = (('period', 14),)

        def __init__(self):
            self.highest = bt.indicators.Highest(self.data.high, period=self.params.period)
            self.lowest = bt.indicators.Lowest(self.data.low, period=self.params.period)
            self.fibo_236 = self.lowest + (self.highest - self.lowest) * 0.236
            self.fibo_382 = self.lowest + (self.highest - self.lowest) * 0.382
            self.fibo_500 = self.lowest + (self.highest - self.lowest) * 0.50
            self.fibo_618 = self.lowest + (self.highest - self.lowest) * 0.618
            self.fibo_100 = self.lowest + (self.highest - self.lowest)

        def next(self):
            if self.data.close[0] > self.fibo_236[0]:
                self.buy()
            elif self.data.close[0] < self.fibo_618[0]:
                self.sell()

    # データをBacktraderのフォーマットに変換
    data_feed = bt.feeds.PandasData(dataname=data)

    # Cerebroエンジンを初期化
    cerebro = bt.Cerebro()
    cerebro.addstrategy(FibonacciStrategy, period=14)
    cerebro.adddata(data_feed)
    cerebro.broker.set_cash(10000)
    cerebro.broker.setcommission(commission=0.001)

    # バックテストの実行
    st.write("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
    cerebro.run()
    st.write("Ending Portfolio Value: %.2f" % cerebro.broker.getvalue())

    # プロットの生成
    fig = cerebro.plot(style='line')[0][0]
    st.pyplot(fig)
