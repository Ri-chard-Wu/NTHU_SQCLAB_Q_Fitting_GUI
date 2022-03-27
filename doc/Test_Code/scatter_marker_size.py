from matplotlib import pyplot as plt
# doubling the width of markers
x = [0,2,4,6,8,10]
y = [0]*len(x)
s = [4 for n in range(len(x))]
plt.scatter(x,y, s=s)
plt.show()
