def smoothstep(start: float, end: float, weight: float) -> float:
    """
    Uses smoothstep to interpolate between two floats ∈ [start, end].

        Parameters:
            start (float): start of the interpolation range.
            end (float): end of the interpolation range.
            weight (float): the weight of the interpolation in the range [0, 1].

        Returns:
            float: the interpolated value in the range [start, end].
    """
    return (end-start)*(3-weight*2)*(weight**2)+start

def scaleHeight(height: float, lower: float, upper: float) -> float:
    """
    Scales a value, height ∈ [-1, 1], to a range [lower, upper].

        Parameters:
            height (float): a value in the range [-1, 1].
            lower (float): the lower bound of the target range.
            upper (float): the upper bound of the target range.

        Returns:
            float: the scaled value in the range [lower, upper].
    """
    return (height+1)/2*(upper-lower) + lower


def lerp(start: float, end:float, weight:float) -> float:
    """
    Uses linear interpolation to interpolate between two floats ∈ [start, end].
    
    Parameters:
        start (float): start of the interpolation range.
        end (float): end of the interpolation range.
        weight (float): the weight of the interpolation in the range [0, 1].
    
    Returns:
        float: the interpolated value in the range [start, end].
    """
    return (end-start)*weight+start

def dotGradient(candidate: tuple[int, int], pt: tuple[float, float], gradients: list[list[tuple[float, float]]]) -> float:
    # offset vector
    diff = (pt[0]-candidate[0], pt[1]-candidate[1])
    # use candidate to grab gradient
    gradient = gradients[candidate[1]][candidate[0]]
    return diff[0]*gradient[0] + diff[1]*gradient[1]