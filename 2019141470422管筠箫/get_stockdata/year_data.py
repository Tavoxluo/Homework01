import pandas as pd
import matplotlib.pyplot as plt


gafataDict = {'谷歌': 'GOOG', '亚马逊': 'AMZN', 'Facebook': 'FB', '苹果': 'AAPL', '阿里巴巴': 'BABA'}
start_date = ' 2020-01-01'
end_date = '2021-01-01'

# data = get_data_yahoo('BABA', start='7/20/2018', end='7/20/2019')

# googleDf = data.DataReader(gafataDict['谷歌'], 'yahoo', start_date, end_date)
# googleDf.info()
# googleDf.to_csv('pufa.csv')


plt.rcParams['font.sans-serif'] = ['KaiTi']
google_csv_data = pd.read_csv('BABA.csv', low_memory=False)
googleDf = pd.DataFrame(google_csv_data)
googleDf.plot(x='Date', y='Close', color='b', label='price')
plt.xlabel("时间")
plt.ylabel("股价")
plt.title("2020年首创股份股价走势")
plt.grid(True)
plt.legend(loc='best')
plt.show()


# 本机matplotlib用的是QtAgg后端 故采用下面语句
# 可根据matplotlib.get_backend()来查询后端
# manager = plt.get_current_fig_manager()
# manager.window.showMaximized()

