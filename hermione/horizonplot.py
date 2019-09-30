import matplotlib.pyplot as plt
import seaborn as sns


KDEPLOT_KWS = dict(clip_on=False, shade=True, alpha=1, lw=1.5, bw=.2)
FACET_KWS = dict(aspect=8, height=0.5)
HLINE_KWS = dict(y=0, lw=1, clip_on=False)


def _set_defaults(given_kws, DEFAULT_KWS):
    """Set defaults but ignore overlapping keywords"""
    for key, value in DEFAULT_KWS.items():
        if key not in given_kws:
            given_kws[key] = value
    return given_kws

# Define a function to add n=## to show the number of cells per cluster
def _show_size(x, color, label=None):
    ax = plt.gca()
    n = len(x)
    ax.text(1, 0.2, 'n={n}'.format(n=n), color=color, ha='left',
            va='center',
            transform=ax.transAxes)


# Define and use a simple function to label the plot in axes
# coordinates
def _label(x, color, label=None):
    if label is None:
        return
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color,
            ha="right", va="center", transform=ax.transAxes)


def horizonplot(data, x, row, row_order=None, palette=None,
            xlabel_suffix=None, facet_kws=None, kdeplot_kws=None,
                hline_kws=None, hue=None,
                label_n_per_group=False):
    facet_kws = FACET_KWS if facet_kws is None else _set_defaults(facet_kws, FACET_KWS)
    kdeplot_kws = KDEPLOT_KWS if kdeplot_kws is None else _set_defaults(kdeplot_kws, KDEPLOT_KWS)
    hline_kws = hline_kws if hline_kws is None else _set_defaults(hline_kws, HLINE_KWS)

    # Pad xlabel suffix with spaces
    xlabel_suffix = ' ' + xlabel_suffix if xlabel_suffix is not None else ''

    # If the row is set, use the row as the hue color
    hue = row if hue is None else hue

    # Label the y-axis based on the row
    label_by_row = True
    if hue is not None:
        label_by_row = False
    with sns.axes_style("white", rc={"axes.facecolor": (0, 0, 0, 0)}):
        g = sns.FacetGrid(data, row=row, hue=hue,
                          palette=palette,
                          row_order=row_order, **facet_kws)
        # Draw the densities in a few steps
        g.map(sns.kdeplot, x, **kdeplot_kws)
        # Plot a fake line for spacing
        g.map(sns.kdeplot, x, **kdeplot_kws)
        # Plot the 0-value on the y axis
        g.map(plt.axhline, **hline_kws)

        if label_n_per_group:
            g.map(_show_size, x)

        if label_by_row:
            g.map(_label, x)
        g.set_xlabels('{x}{xlabel_suffix}'.format(
            x=x, xlabel_suffix=xlabel_suffix))

        # Set the subplots to overlap
        g.fig.subplots_adjust(hspace=-.25)

        # Remove axes details that don't play will with overlap
        g.set_titles("")
        g.set(yticks=[])
        g.despine(bottom=True, left=True)

        return g