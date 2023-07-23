import pandas as pd
from time import time
from sp import StripPacking

def main():   
    data = pd.read_csv("rectangles.csv", header=None)
    elements = list(data.itertuples(index=False, name=None))
    width, n = elements[0][0], elements[0][1]
    elements.pop(0)
    sp = StripPacking(width, elements)
    start_time = time()
    height, packing = sp.getoptimalsolution()
    print("The execution time is: {} seconds".format(time() - start_time))
    print("The strip width is: {} ".format(width))
    print("The optimal packing height is: {}".format(height))
    sp.visualize()

if __name__ == "__main__":
    main()