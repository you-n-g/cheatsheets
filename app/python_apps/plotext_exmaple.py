"""
pip install plotext
"""


# import plotext as plt
# y = plt.sin()
# plt.plot(y)
# plt.title("Line Plot")
# plt.show()


# import plotext as plt
#
# l = 1000
# frames = 200
#
# plt.title("Streaming Data")
# # plt.clc()
#
# for i in range(frames):
#     plt.clt() # to clear the terminal
#     plt.cld() # to clear the data only
#
#     y = plt.sin(periods = 2, length = l, phase = 2 * i  / frames)
#     plt.scatter(y)
#
#     #plt.sleep(0.001) # to add
#     plt.show()


import plotext as plt
frames = 200
for i in range(frames):
    plt.clt()
    plt.cld()
    # y = plt.sin()
    plt.plot(range(20, i + 21), range(10, i + 11))
    plt.title("Line Plot")
    plt.sleep(0.01)
    plt.show()
