import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlitのページ設定
st.set_page_config(page_title="Market Analysis", layout="wide")

# タイトルと説明を表示
st.title("Market Analysis with Streamlit")
st.write("This is a sample Streamlit app to demonstrate market analysis.")

# ファイルアップロード機能
uploaded_file = st.file_uploader("Choose a file", type=["csv"])

if uploaded_file is not None:
    # ヒストリカルデータを読み込み
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded data:", data.head())

    # 'datetime'カラムをインデックスに設定
    data['datetime'] = pd.to_datetime(data['datetime'], format='%Y-%m-%d %H:%M:%S')
    data.set_index('datetime', inplace=True)

    # 無効な値を削除
    data = data.dropna()

    # 時間帯ごとにデータを分割する関数
    def filter_by_time(data, start_time, end_time):
        return data.between_time(start_time, end_time)

    # 高値と安値の間の平均バー本数を計算する関数
    def calculate_average_bar_count(data, period=14):
        data['High'] = data['High'].rolling(window=period).max()
        data['Low'] = data['Low'].rolling(window=period).min()

        bar_counts = []
        current_high = None
        current_low = None
        count = 0

        for i in range(1, len(data)):
            if data['High'].iloc[i] != data['High'].iloc[i-1]:  # 高値が変わった場合
                if current_low is not None:
                    bar_counts.append(count)
                current_high = data['High'].iloc[i]
                current_low = None
                count = 1
            elif data['Low'].iloc[i] != data['Low'].iloc[i-1]:  # 安値が変わった場合
                if current_high is not None:
                    bar_counts.append(count)
                current_low = data['Low'].iloc[i]
                current_high = None
                count = 1
            else:
                count += 1

        # バー本数の平均を計算
        average_bar_count = sum(bar_counts) / len(bar_counts) if bar_counts else 0
        return average_bar_count

    # 各市場の時間帯を設定
    tokyo_time = filter_by_time(data, '08:30', '15:00')
    europe_time = filter_by_time(data, '15:00', '21:00')
    ny_time = filter_by_time(data, '21:00', '02:00')

    # 各市場ごとの平均バー本数を計算
    average_bar_count_tokyo = calculate_average_bar_count(tokyo_time)
    average_bar_count_europe = calculate_average_bar_count(europe_time)
    average_bar_count_ny = calculate_average_bar_count(ny_time)

    st.write("東京時間の平均バー本数:", average_bar_count_tokyo)
    st.write("欧州市場の平均バー本数:", average_bar_count_europe)
    st.write("NY市場の平均バー本数:", average_bar_count_ny)

    # 各時間帯の平均値幅を計算する関数
    def calculate_average_range(data):
        data['Range'] = data['High'] - data['Low']
        average_range = data['Range'].mean() * 10000  # ピップスに変換（通常の為替レートは小数点以下4桁）
        return average_range

    # 各市場ごとの平均値幅を計算
    average_range_tokyo = calculate_average_range(tokyo_time)
    average_range_europe = calculate_average_range(europe_time)
    average_range_ny = calculate_average_range(ny_time)

    st.write("東京時間の平均値幅（pips）:", average_range_tokyo)
    st.write("欧州市場の平均値幅（pips）:", average_range_europe)
    st.write("NY市場の平均値幅（pips）:", average_range_ny)

    # フィボナッチレベルを計算する関数
    def calculate_fibonacci_levels(data):
        highest = data['High'].rolling(window=14).max()
        lowest = data['Low'].rolling(window=14).min()

        fibo_236 = lowest + (highest - lowest) * 0.236
        fibo_382 = lowest + (highest - lowest) * 0.382
        fibo_500 = lowest + (highest - lowest) * 0.50
        fibo_618 = lowest + (highest - lowest) * 0.618
        fibo_100 = lowest + (highest - lowest)

        return fibo_236, fibo_382, fibo_500, fibo_618, fibo_100

    fibo_236, fibo_382, fibo_500, fibo_618, fibo_100 = calculate_fibonacci_levels(data)

    st.write("フィボナッチレベル（東京時間）:")
    st.line_chart(pd.DataFrame({
        "Fibo 23.6%": fibo_236,
        "Fibo 38.2%": fibo_382,
        "Fibo 50.0%": fibo_500,
        "Fibo 61.8%": fibo_618,
        "Fibo 100%": fibo_100
    }))




