# MPL_selector
A tool to select data in matplotlib figures

![](readme.gif)

### Usage

```
from mpl_selections import Selector 
import matplotlib.pyplot as plt
import numpy as np

#create some data
x = np.random.normal(100)
y = np.random.normal(100)

#plot the data
fig, ax = plt.subplots()
ax.scatter(x,y)

#create a selector object and pass the axes to do selections on
selector = Selector(ax)

```

To get the selection:

```
selection = selector.get_selection()
```
`selection` is a boolean array.

### connect functions

Whenever the mouse is released, a function can be called
