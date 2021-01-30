# SST - 时间序列分解

>  数据集 NOAA Extended Reconstructed Sea Surface Temperature (SST) V5
>
> 来自 https://www.esrl.noaa.gov/psd/data/gridded/data.noaa.ersst.v5.html
>
> 记录 1854 ~ 2018 年各海域的 sst 情况。

通过上述数据集，我们挑选了全球部分海域画出 sst 的变化曲线：

![global sea surface temperature change2](https://gitee.com/koorye/picgo/raw/master/global%20sea%20surface%20temperature%20change2.png)

我们发现：

- 全球变暖在不同海区的表现不同
- 经过计算，1950 年到现在，上述海区 SST 分别变化：

  - 南太平洋 0.409
  - 北大西洋 1.326
  - 北海 0.481
  - 日本海 -0.788
  - 南印度洋 0.955
  - 地中海 1.014
- 值得一提的是，许多海区都呈现出一个现象，在 1980 ~ 1990 前的一段时间，SST 上升相对缓慢，这之后 SST 上升相对快速，我们认为有必要将这个时间段作为两个周期的分界点

接下来我们分析苏格兰附近海域的 SST 变化情况：

![sea surface temperature change of Scotland2](https://gitee.com/koorye/picgo/raw/master/sea%20surface%20temperature%20change%20of%20Scotland2.png)

通过观察图像，我们认为该时间序列呈现季节性波动与上升趋势。

通过放大图像的横坐标，我们自然发现由于季度的变化，SST 呈现稳定的波动，我们有必要将季度变化序列从原序列中分离出来。

我们认为时间序列由以下因素组成加性模型：
$$
Y[t]=T[t]+S[t]+R[t]
$$
其中：

- Y[t] 表示分离前的原序列
- T[t] 表示趋势序列
- S[t] 表示季度序列
- R[t] 表示误差序列

我们需要对 Y[t] 计算移动平均趋势值 CMA。

k 阶移动平均 (k-MA) 是指：
$$
\hat{T}[t+k]=\frac1k\sum_{i=0}^kY[t+i]
$$
对于原序列 Y[t]，先进行 12-MA，消除月度波动的影响，再进行 2-MA，从而对序列再进行中心化处理，使得移动平均后的序列与原序列对称，处理后的序列称为 CMA (Central Moving Average).

示例：

| Y        | Y after 12-MA                                 | 12-MA after 2-MA                                  | CMA (12-MA after Aligning) |
| -------- | --------------------------------------------- | ------------------------------------------------- | -------------------------- |
| y1       | -                                             | -                                                 | -                          |
| y2       | -                                             | -                                                 | -                          |
| $\vdots$ | $\vdots$                                      | $\vdots$                                          | $\vdots$                   |
| y8       | -                                             | -                                                 | $cma_{8}=y_{14}^{(2)}$     |
| y9       | -                                             | -                                                 | $cma_{9}=y_{15}^{(2)}$     |
| $\vdots$ | $\vdots$                                      | $\vdots$                                          | $\vdots$                   |
| y19      | $y_{19}^{(1)}=\frac{1}{12}\sum_{i=8}^{19}y_i$ | -                                                 | -                          |
| y20      | $y_{20}^{(1)}=\frac{1}{12}\sum_{i=9}^{20}y_i$ | $y_{20}^{(2)}=\frac12(y_{19}^{(1)}+y_{20}^{(1)})$ | -                          |

得到 CMA 后，将对应月份的 Y/CMA 求和，就可以得到每个月份的权重 wi：
$$
w_i=\sum_j\frac{y_{i+12j}}{cma_{i+12j}}, i=1,2,\dots,12
$$
对 W 进行归一化处理，使其和为 12：
$$
\hat{w_i}=12\frac{w_i}{\sum_{i=1}^{12}w_i}
$$
将原序列乘以对应的权重 wi，就可以得到分离出的趋势序列 T[t]：
$$
T[i+12j]=Y[i+12j]\cdot\hat{w_i},i=1,2,\dots,12
$$
记
$$
D[t]=S[t]+R[t]
$$
则有
$$
D[t]=Y[t]-T[t]
$$
对 D[t] 中每个月 i 分别求和：
$$
\sum_jD[i+12j]=\sum_j(Y[i+12j]-T[i+12j])
$$
记对应月份 i 的偏置值 $\epsilon_i$：
$$
\epsilon_i=-\sum_jD[i+12j]
$$
则
$$
S[i+12j]=D[i+12j]+\epsilon_i
$$
得到修正后的 D[t]，即季节序列 S[t].

于是有残差序列：
$$
R[t]=Y[t]-T[t]-S[t]
$$
从而完成时间序列的分解。

分离后的时间序列如下图所示：

![decomposed sst changes in scotland2](https://gitee.com/koorye/picgo/raw/master/decomposed%20sst%20changes%20in%20scotland2.png)