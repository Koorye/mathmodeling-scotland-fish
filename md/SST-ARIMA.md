# SST - ARIMA

画出趋势序列 T[t] 的变化情况如下图：

![trend series of sst changes in scotland](https://gitee.com/koorye/picgo/raw/master/trend%20series%20of%20sst%20changes%20in%20scotland.png)

观察认为，苏格兰附近海域的 SST 变化如下：

- 在 1900 ~ 1933 和 1979 ~ 1999 年间，SST 呈下降趋势
- 在 1933 ~ 1979 和 1999 至今，SST 呈上升趋势

因此，我们取 1999 年以后的数据进行分析。

使用 ARIMA 模型对数据进行拟合。

ARIMA 模型的结构：
$$
y_t^{(d)}=\mu_t+\sum_{i=1}^p\phi_iy_{t-i}^{(d)}+\epsilon_t+\sum_{j=1}^q\theta_j\epsilon_{t-j}
$$
ARIMA 由以下几个部分组成：

- AR (Auto Regression) 模型
  $$
  y_t=\mu_t+\sum_{i=1}^p\phi_iy_{t-i}
  $$
  AR 模型利用前期若干时刻的随机变量的线性组合描述以后某时刻的随机变量

- MA (Moving Average) 模型
  $$
  y_t=\epsilon_t+\sum_{j=1}^q\theta_j\epsilon_{t-j}
  $$
  MA 模型利用前期若干时刻的随机扰动描述以后某时刻的随机变量
  
- I 表示差分法
  

观察到 T[t] 不平稳，需要对 T[t] 进行差分，以达到最佳的平稳效果：
![trend under diff](https://gitee.com/koorye/picgo/raw/master/trend%20under%20diff.png)

T[t] 进行 0~5 次差分后的方差分别为

```
[0.04099963664215694,
 0.0004600730162189924,
 2.112886720630772e-05,
 4.110007096544802e-06,
 2.9149267711679735e-06,
 5.2963089093346e-06]
```

T[t] 在 4 次差分后取到最小方差，然而差分过多会导致序列失去自相关性。

通过观察上图，我们认为二阶差分时模型足够平稳，故取 d=2.

使用 ACF 和 PACF 图确定 ARIMA 中的阶数 p 和 q：

![acf and pacf of trend](https://gitee.com/koorye/picgo/raw/master/acf%20and%20pacf%20of%20trend.png)
$$
ACF(k)=\rho_k=\frac{Cov(y_t,y_{t-k})}{Var(y_t)}
$$
ACF 反映了同一序列在不同时序的取值之间的相关性。

PACF 则反映了剔除随机变量干扰后的相关程度。

ACF 为 1，PACF 为 1 时均截尾，初步判定 p=1, q=1.

p 取 0~3，q 取 0~1，d 取 2，根据 BIC (Bayesian Information Crierion) 衡量最佳的 p 和 q 值。
$$
BIC=-2\ln(L)+ln(n)\cdot k
$$
其中 L 表示该模型的极大似然函数，n 是数据量，k 是模型的变量个数，选取 BIC 最小时的 p 和 q 作为最终模型的阶数。

```
Performing stepwise search to minimize bic
 ARIMA(1,2,1)(0,0,0)[0] intercept   : BIC=-2273.488, Time=0.76 sec
 ARIMA(0,2,0)(0,0,0)[0] intercept   : BIC=-1788.578, Time=0.04 sec
 ARIMA(1,2,0)(0,0,0)[0] intercept   : BIC=-2164.991, Time=0.04 sec
 ARIMA(0,2,1)(0,0,0)[0] intercept   : BIC=-2039.354, Time=0.29 sec
 ARIMA(0,2,0)(0,0,0)[0]             : BIC=-1793.999, Time=0.02 sec
 ARIMA(2,2,1)(0,0,0)[0] intercept   : BIC=-2327.749, Time=0.21 sec
 ARIMA(2,2,0)(0,0,0)[0] intercept   : BIC=-2330.842, Time=0.18 sec
 ARIMA(3,2,0)(0,0,0)[0] intercept   : BIC=-2328.962, Time=0.21 sec
 ARIMA(3,2,1)(0,0,0)[0] intercept   : BIC=-2318.646, Time=0.17 sec
 ARIMA(2,2,0)(0,0,0)[0]             : BIC=-2336.270, Time=0.08 sec
 ARIMA(1,2,0)(0,0,0)[0]             : BIC=-2170.414, Time=0.03 sec
 ARIMA(3,2,0)(0,0,0)[0]             : BIC=-2334.389, Time=0.10 sec
 ARIMA(2,2,1)(0,0,0)[0]             : BIC=-2333.176, Time=0.10 sec
 ARIMA(1,2,1)(0,0,0)[0]             : BIC=-2245.227, Time=0.09 sec
 ARIMA(3,2,1)(0,0,0)[0]             : BIC=-2324.085, Time=0.30 sec

Best model:  ARIMA(2,2,0)(0,0,0)[0]          
Total fit time: 2.641 seconds
```

最终得到 p、q 与 BIC 的关系如下图所示：

![bic2](https://gitee.com/koorye/picgo/raw/master/bic2.png)

故 p=2, q=0 时，BIC 最小，取最终模型 ARIMA(2,2,0)，表示 p=2，d=2，q=0.

通过 OLS 计算得到 $\phi_1=\phi_2=1.0740$，故
$$
y_t^{(2)}=\mu_t+1.0740\sum_{i=1}^2y_{t-i}^{(2)}+\epsilon_t
$$
记为
$$
y_t=ARIMA(y_{t-i}),i=1,2,\dots,t-1
$$
在对未来数据拟合时，只需假设 $\epsilon_t=0$ 即可。

模型的预测结果如下：

![the sst trend forecast value of arima](https://gitee.com/koorye/picgo/raw/master/the%20sst%20trend%20forecast%20value%20of%20arima.png)

粉色表示置信区间。

使用该模型预测未来 50 年，结果如下图所示：

![the sst trend forecast value of arima over the next 50 years](https://gitee.com/koorye/picgo/raw/master/the%20sst%20trend%20forecast%20value%20of%20arima%20over%20the%20next%2050%20years.png)

50 年间 SST 上升约 1.2 ℃.

考察 50°N ~ 60°N 的北大西洋海区，取不同的月份，SST 呈现如下的变化趋势：

![the relationship between sst and latitude in different months2](https://gitee.com/koorye/picgo/raw/master/the%20relationship%20between%20sst%20and%20latitude%20in%20different%20months2.png)

在 50°N~60°N 的范围内，SST和纬度的关系可用一元线性回归进行估计：
$$
SST=45.297-0.735Lat
$$
故通过上面的预测模型，我们认为未来 50 年 SST 将上升 1.2℃，这将使得鱼群北移 1.63°N.

查询资料，鲱鱼最适合生存的 SST 在 5℃ 左右，大致位于 53°N；

而鲭鱼最适合生存的 SST 在 9℃ 左右，大致位于 50°N.

故可得出两种鱼分布纬度随时间的变化如下图：

![the relation of latitude of fish distribution with time2](https://gitee.com/koorye/picgo/raw/master/the%20relation%20of%20latitude%20of%20fish%20distribution%20with%20time2.png)

得
$$
y_t=ARIMA(y_{t-i}),i=1,2,\dots,t-1
$$

$$
Lat_t=Lat_0+1.36\cdot y_t-\hat{y_0}+S[t]=Lat_0+1.36\cdot y_t-6.399+S[t]
$$

其中 $\hat{y_0}$ 表示第一个预测的 SST 值。

对于鲭鱼
$$
Lat_0=50
$$
对于鲱鱼
$$
Lat_0=53
$$
