import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import random
from math import inf
from collections import namedtuple

Rectangle = namedtuple('Rectangle', ['x', 'y', 'w', 'h'])

class StripPacking:
    def __init__(self, width, rectangles):
        """
        Constructor for initializing an object of StripPacking.
    
        Parameters
        ----------
        width: int
            The width of the strip.
    
        rectangles: list
            List of tuples containing width and height of every rectangle, [(w_1, h_1), ..., (w_n, h_n)].
        """
        
        self.width = width
        self.rectangles = rectangles.copy()
        self.optimalheight = inf
        self.optimalpacking = []
        self.resultpaking = []
        
    def getoptimalsolution(self):
        """
        Method for determining the optimal packing.

        Parameters
        ----------
        None

        Returns
        -------
        int
            The optimal height of the strip needed to pack all the items.
        
        list 
            List of namedtuple ('Rectangle', ['x', 'y', 'w', 'h'])
            List of optinmal packed rectangles that contains bottom left x and y coordinate and the width and height.
        """
        remainedrectangles = self.rectangles.copy()
        self.generatesolutions(remainedrectangles, [(0,0)])
        return self.optimalheight, self.optimalpacking
                    
    def generatesolutions(self, remainedrectangles, corners):
        """
        Method for generating all possible solutions and identifying the optimal one for 2SP.  
        
        Parameters
        ----------
        remainedrectangles: list
            List of tuples containing width and height of every remaind rectangle, [(w_1, h_1), ..., (w_n, h_n)].
             
        corners: list
            List of tuples containing x and y of every corner, [(x_1, y_1), ..., (x_n, y_n)].
            
        Returns
        -------
        None
        """
        
        #The packing is constructed
        if len(remainedrectangles) == 0:

            #Determine the height of the packing
            maxr = max(self.resultpaking, key = lambda r: r.y + r.h)
            height = maxr.y + maxr.h
            
            #If the height ot the constructed packing is lower than the height achieved by the current best packing, 
            #then update the best packing
            if height < self.optimalheight:
                self.optimalheight = height
                self.optimalpacking = self.resultpaking.copy()
      
        #Continue construction of packings
        else:
            
            #For every rectangle and for every corner point  
            for r in remainedrectangles:
                for c in corners:
                    
                    #If the assignment of the rectangle r to the corner point c does not exceed the width of the strip,
                    #then we assign the rectangle to this position and call the procedure recursively 
                    if c[0] + r[0] <= self.width:
                        newr = Rectangle(c[0], c[1], r[0], r[1])
                        self.resultpaking.append(newr) 
                        self.resultpaking = sorted(self.resultpaking, key=lambda z:z.y+z.h, reverse=True)
                        height, newcorners = self.getcorners(self.resultpaking)
                                               
                        #If the height of the constructing packing is lower than the height achieved by the 
                        #current best packing, then we call the procedure recursively. Otherwise we backtrack
                        if height < self.optimalheight: 
                            newrectangles = remainedrectangles.copy()
                            newrectangles.remove(r)
                            self.generatesolutions(newrectangles, newcorners)
                        self.resultpaking.remove(newr)
    
    def getcorners(self, packing):
        """
        Method for determining the set of corners and the height of the paking.

        Parameters
        ----------
        packing: list
            List of namedtuple('Rectangle', ['x', 'y', 'w', 'h'])
            List of packed rectangles that contains bottom left x and y coordinate and the width and height.
 
        Returns
        -------
        int
            The height of the paking.
            
        list
            List of tuples containing x and y coordinate of every corner, [(x_1, y_1), ..., (x_n, y_h)].
        """
        
        if len(packing) == 0:
            return 0, [(0,0)]        
        else:
            
            #Phase 1  (identify the extreme items (e1,...,em)
            e = [None] * len(packing) 
            xlabeled, m = -1, -1
            for idx, r in enumerate(packing):
                if r.x + r.w > xlabeled:
                    m = m + 1
                    e[m] = idx
                    xlabeled = r.x + r.w
                
            #Phase 2 (determine the corner points)
            corners = {(0,packing[e[0]].y + packing[e[0]].h)}
            for ind in range(1,m + 1):
                corners = corners.union({(packing[e[ind - 1]].x + packing[e[ind - 1]].w,
                                          packing[e[ind]].y + packing[e[ind]].h)})
            corners = corners.union({(packing[e[m]].x + packing[e[m]].w, 0)})
            
            #Determine the height of the paking
            height = max(corners, key = lambda c: c[1])[1]
            
        return height, [*corners, ]

    def visualize(self):
        """
        Method for visualization the strip of size width x optimalheight with the layout of the rectangles.

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        
        fig = plt.figure()
        axes = fig.add_subplot(1, 1, 1)
        axes.add_patch(patches.Rectangle((0, 0), self.width, self.optimalheight, hatch='x', fill=False,))
        print("The optimal packing:")
        for idx, r in enumerate(self.optimalpacking):
            axes.add_patch(patches.Rectangle((r.x, r.y), r.w, r.h, color=(random(), random(), random()),))
            axes.text(r.x+0.5*r.w, r.y+0.5*r.h, str(idx+1))
            print("{}. rectangle of size ({}, {}) is packed at position ({}, {})".format(idx+1, r.w, r.h, r.x, r.y,))
        axes.set_xlim(0, self.width)
        axes.set_ylim(0, self.optimalheight)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()