#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 09:39:07 2020

@author: daniel
"""

import matplotlib.pyplot as plt
import numpy as np


class Selector(object):
    def __init__(self, ax, update_resolution = 20):
        self.ax  = ax
        self.scatter = self.ax.get_children()[0]
        self.connect()
        self.rect = plt.Rectangle([0,0],0,0, facecolor = "blue", alpha = 0.1)
        self.ax.add_artist(self.rect)
        self.start = np.zeros(shape = 2)
        self.end = np.zeros(shape = 2)
        self.dragged = False
        self.on_release_func = None
        self.update_resolution = update_resolution
        self.moved = 0
    def connect(self):
        self.mouse_move = self.ax.figure.canvas.mpl_connect("motion_notify_event", self.mouse_move)
        self.mouse_press = self.ax.figure.canvas.mpl_connect("button_press_event", self.button_press)
        self.mouse_release = self.ax.figure.canvas.mpl_connect("button_release_event", self.button_release)
        
    def on_release(self):
        if self.on_release_func != None:
            self.on_release_func()
        
    def mouse_move(self, event):
        if not event.inaxes:
            return    
        if event.button == 1:
            self.dragged = True
            self.end = np.array([event.xdata, event.ydata])
            self.moved += 1
            if self.moved > self.update_resolution:
                self.update_rect()
                self.moved = 0
            
#        self.ax.figure.canvas.draw()
        
        
    def button_press(self, event):
        if event.dblclick:
            self.start = np.array([0,0])
            self.end = np.array([0,0])
            self.update_selection()
            self.update_rect()
        else:
            self.start = np.array([event.xdata, event.ydata])
            
            
    def button_release(self, event):
        if self.dragged == True:
            self.dragged = False
            self.update_selection()
        self.on_release()
            
    def update_selection(self):
        self.update_rect()
        data = self.scatter.get_offsets().data
        xmin = np.min([self.start[0], self.end[0]])
        xmax = np.max([self.start[0], self.end[0]])
        ymin = np.min([self.start[1], self.end[1]])
        ymax = np.max([self.start[1], self.end[1]])        
        mask = (data[:,0] > xmin) & (data[:,0] < xmax) & (data[:,1] > ymin) & (data[:,1] <ymax)
        self.scatter.set_array(mask)
        self.selection = mask
        self.scatter.set_array(self.selection)
        self.ax.figure.canvas.draw()
    
        
    def update_rect(self):
        self.rect.set_bounds(self.start[0],  self.start[1], self.end[0]-self.start[0], self.end[1]-self.start[1])
        self.ax.figure.canvas.draw()
        
    def get_selection(self):
        if hasattr(self, "selection"):
            return self.selection
        
if __name__ == "__main__":
    
    x = np.hstack([np.random.normal(10,0.5, 100), np.random.normal(5,0.2, 100)])
    y = np.hstack([np.random.normal(10,1, 100), np.random.normal(8,0.1, 100)])
    fig, ax = plt.subplots()
    scatter = ax.scatter(x,y)
    s = Selector(ax)
