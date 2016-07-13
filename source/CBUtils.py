import multiprocessing


def _apply_df(args):
    df, func, kwargs = args
    return df.apply(func, **kwargs)

def apply_by_multiprocessing(df, func, workers=multiprocessing.cpu_count(), **kwargs):
    """

    Parameters
    ----------
    df: pandas.DataFrame
        column names will form dictionary keys
    func:
        a function taking a dictionary of parameters, and other keyword arguments
    workers: int
        how many cores to use? default is the total number available
    kwargs: arguments
        keyword arguments passed to pd.DataFrame.apply or to `func`

    Returns
    -------
    df: pandas.DataFrame

    """
    pool = multiprocessing.Pool(processes=workers)
    result = pool.map(_apply_df, [(d, func, kwargs) for d in np.array_split(df, workers)])
    pool.close()
    return pd.concat(list(result))
