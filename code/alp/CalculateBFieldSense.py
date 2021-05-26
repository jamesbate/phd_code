import numpy as np
import matplotlib.pyplot as plt

# def df_MHZ(mS, mD, B):
#     gS = 2
#     gD = 1.2
#     return 1.4*B*(-gS*mS + gD*mD)

def df_MHZ(mS, mD, B):
    gS = 2
    gD = 1.2
    return 1e-6*(-gS*mS + gD*mD)*9.27e-24*B/6.63e-34


print(df_MHZ(0.5, 2.5, 8.93e-8))

B = np.linspace(1, 10, 10)*1e-8
#B = np.linspace(0,4, 10)*1e-4
BPlot = B*1e10

plt.plot(BPlot, df_MHZ(-0.5, -2.5, B)*1e3, label = '-0.5 -> -2.5')
plt.plot(BPlot, df_MHZ(-0.5, -1.5, B)*1e3, label = '-0.5 -> -1.5')
plt.plot(BPlot, df_MHZ(-0.5, -0.5, B)*1e3, label = '-0.5 -> -0.5')
plt.plot(BPlot, df_MHZ(-0.5, 0.5, B)*1e3, label = '-0.5 -> 0.5')
plt.plot(BPlot, df_MHZ(-0.5, 1.5, B)*1e3, label = '-0.5 -> 1.5')
plt.plot(BPlot, df_MHZ(-0.5, 2.5, B)*1e3, label = '-0.5 -> 2.5')

plt.plot(BPlot, df_MHZ(0.5, -2.5, B)*1e3, label = '0.5 -> -2.5')
plt.plot(BPlot, df_MHZ(0.5, -1.5, B)*1e3, label = '0.5 -> -1.5')
plt.plot(BPlot, df_MHZ(0.5, -0.5, B)*1e3, label = '0.5 -> -0.5')
plt.plot(BPlot, df_MHZ(0.5, 0.5, B)*1e3, label = '0.5 -> 0.5')
plt.plot(BPlot, df_MHZ(0.5, 1.5, B)*1e3, label = '0.5 -> 1.5')
plt.plot(BPlot, df_MHZ(0.5, 2.5, B)*1e3, label = '0.5 -> 2.5')

# plt.plot(B*1e4, df_MHZ(-0.5, -2.5, B), label = '-0.5 -> -2.5')
# plt.plot(B*1e4, df_MHZ(-0.5, -1.5, B), label = '-0.5 -> -1.5')
# plt.plot(B*1e4, df_MHZ(-0.5, -0.5, B), label = '-0.5 -> -0.5')
# plt.plot(B*1e4, df_MHZ(-0.5, 0.5, B), label = '-0.5 -> 0.5')
# plt.plot(B*1e4, df_MHZ(-0.5, 1.5, B), label = '-0.5 -> 1.5')
# plt.plot(B*1e4, df_MHZ(-0.5, 2.5, B), label = '-0.5 -> 2.5')

# plt.plot(B*1e4, df_MHZ(0.5, -2.5, B), label = '0.5 -> -2.5')
# plt.plot(B*1e4, df_MHZ(0.5, -1.5, B), label = '0.5 -> -1.5')
# plt.plot(B*1e4, df_MHZ(0.5, -0.5, B), label = '0.5 -> -0.5')
# plt.plot(B*1e4, df_MHZ(0.5, 0.5, B), label = '0.5 -> 0.5')
# plt.plot(B*1e4, df_MHZ(0.5, 1.5, B), label = '0.5 -> 1.5')
# plt.plot(B*1e4, df_MHZ(0.5, 2.5, B), label = '0.5 -> 2.5')

plt.axhline(0.5, linestyle = ':', c = 'k')
plt.axhline(-0.5, linestyle = ':', c = 'k')
plt.legend()
plt.xlabel('B field (uG)')
plt.ylabel('Frequency (KHz)')
plt.show()