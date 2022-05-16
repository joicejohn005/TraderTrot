yf_returns = yf_returns.iloc[:, yf_returns.columns.get_level_values(1)=='Close']
# yf_returns.columns = yf_returns.columns.droplevel(1)  # multi-index
# yf_returns.tail(10)
# print('shape: ', yf_returns.shape)