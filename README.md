# hermione

Joyplots and more for single cells

## Examples

```python
import hermione as hm
import numpy as np
import pandas as pd

%matplotlib inline

# Create the data
rs = np.random.RandomState(1979)
x = rs.randn(500)
g = np.tile(list("ABCDEFGHIJ"), 50)
df = pd.DataFrame(dict(x=x, g=g))
m = df.g.map(ord)
df["x"] += m


hm.joyplot(data=df, x='x', row='g', xlabel_suffix='log2(UMI + 1)')
```

![](figures/joyplot_default.png)

### Change the colors

Change the color palette with the `palette` keyword as with `seaborn.FacetGrid`:

```python
hm.joyplot(data=df, x='x', row='g', xlabel_suffix='log2(UMI + 1)', palette='Paired')
```
![](figures/joyplot_palette.png)


### Change the row order

Change the row order with the `row_order` keyword as with `seaborn.FacetGrid`:


```python
hm.joyplot(data=df, x='x', row='g', xlabel_suffix='log2(UMI + 1)', palette='Paired', 
           row_order=list('ABCJIHDEFG'))
```

![](figures/joyplot_palette_row_order.png)
