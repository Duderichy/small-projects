import pytest
from datetime import datetime
import numpy as np
import sys

# Your task is to write the group adjustment method below. There are some
# unimplemented unit_tests at the bottom which also need implementation.
# Your solution can be pure python, pure NumPy, pure Pandas
# or any combination of the three.  There are multiple ways of solving this
# problem, be creative, use comments to explain your code.

# Group Adjust Method
# The algorithm needs to do the following:
# 1.) For each group-list provided, calculate the means of the values for each
# unique group.
#
#   For example:
#   vals       = [  1  ,   2  ,   3  ]
#   ctry_grp   = ['USA', 'USA', 'USA']
#   state_grp  = ['MA' , 'MA' ,  'CT' ]
#
#   There is only 1 country in the ctry_grp list.  So to get the means:
#     USA_mean == mean(vals) == 2
#     ctry_means = [2, 2, 2]
#   There are 2 states, so to get the means for each state:
#     MA_mean == mean(vals[0], vals[1]) == 1.5
#     CT_mean == mean(vals[2]) == 3
#     state_means = [1.5, 1.5, 3]
#
# 2.) Using the weights, calculate a weighted average of those group means
#   Continuing from our example:
#   weights = [.35, .65]
#   35% weighted on country, 65% weighted on state
#   ctry_means  = [2  , 2  , 2]
#   state_means = [1.5, 1.5, 3]
#   weighted_means = [2*.35 + .65*1.5, 2*.35 + .65*1.5, 2*.35 + .65*3]
#
# 3.) Subtract the weighted average group means from each original value
#   Continuing from our example:
#   val[0] = 1
#   ctry[0] = 'USA' --> 'USA' mean == 2, ctry weight = .35
#   state[0] = 'MA' --> 'MA'  mean == 1.5, state weight = .65
#   weighted_mean = 2*.35 + .65*1.5 = 1.675
#   demeaned = 1 - 1.675 = -0.675
#   Do this for all values in the original list.
#
# 4.) Return the demeaned values

# Hint: See the test cases below for how the calculation should work.

###############################################################################
# Notes:
# My approach was to do things mostly functional, so I ended up creating
# copies of lists, which results in a large amount of memory being
# allocated for the last test. However, I chose this approach in pure python
# to demonstrate clean and largely elegant code. I figure this would be easier
# in numpy, but I wanted to use pure python to take advantage of some of the 
# built in python features to create concise elegant code without relying on an
# external library. (Numpy is great, I just wanted to try this exercise without)
# The runtime complexity is O(n * m), where n is len(vals) and m is len(groups)
#
# tests can be run with pytest -q main.py
###############################################################################

def group_mean(vals, groups, weights):
    """
    Calculates the mean for an individual group
    """
    lookup = [dict() for _ in range(len(groups))]
    # populates lookup table with count and total
    for i, val in enumerate(vals):
        for j, group in enumerate(groups):
            group_id = group[i]
            if group_id not in lookup[j]:
                lookup[j][group_id] = [0, 0]
            if val:
                total_counter = lookup[j][group_id]
                total_counter[0] += val
                total_counter[1] += 1
    # calculates average from count and total in lookup table
    # for group_id, total_counter in lookup.items():
    #    lookup[group_id] = total_counter[0] / total_counter[1] * weight
    for i, group_lookup in enumerate(lookup):
        for group_lookup_name, lookup_val in group_lookup.items():
            group_lookup[group_lookup_name] = lookup_val[0] / lookup_val[1] * weights[i]

    for i in range(len(vals)):
        for j, group in enumerate(groups):
            if vals[i]:
                vals[i] -= lookup[j][group[i]]
    # returns list of means for each group id in proper order
    return lookup

def groups_means(vals, groups, weights):
    """
    Calculates the means for a list of groups
    """
    return group_mean(vals, groups, weights)

def group_adjust(vals, groups, weights):
    """
    Calculate a group adjustment (demean).

    Parameters
    ----------

    vals    : List of floats/ints

        The original values to adjust

    groups  : List of Lists

        A list of groups. Each group will be a list of ints

    weights : List of floats

        A list of weights for the groupings.

    Returns
    -------

    A list-like demeaned version of the input values
    """
    # raises error if length of groups and weights are not the same
    if len(groups) != len(weights):
        raise ValueError
    # raises error if the length of any of the groups is not the same length
    # as the vals list
    if not all(x == len(vals) for x in map(len, groups + [vals])):
        raise ValueError
    lookup_means = groups_means(vals, groups, weights)
    return vals

class TestClass:
    def test_three_groups(self):
        vals = [1, 2, 3, 8, 5]
        grps_1 = ['USA', 'USA', 'USA', 'USA', 'USA']
        grps_2 = ['MA', 'MA', 'MA', 'RI', 'RI']
        grps_3 = ['WEYMOUTH', 'BOSTON', 'BOSTON', 'PROVIDENCE', 'PROVIDENCE']
        weights = [.15, .35, .5]

        adj_vals = group_adjust(vals, [grps_1, grps_2, grps_3], weights)
        # 1 - (USA_mean*.15 + MA_mean * .35 + WEYMOUTH_mean * .5)
        # 2 - (USA_mean*.15 + MA_mean * .35 + BOSTON_mean * .5)
        # 3 - (USA_mean*.15 + MA_mean * .35 + BOSTON_mean * .5)
        # etc ...
        # Plug in the numbers ...
        # 1 - (.15 * 3.8 + .35 * 2.0 + .5 * 1.0) = -0.770
        # 2 - (.15 * 3.8 + .35 * 2.0 + .5 * 2.5) = -0.520
        # 3 - (.15 * 3.8 + .35 * 2.0 + .5 * 2.5) =  0.480
        # etc...

        answer = [-0.770, -0.520, 0.480, 1.905, -1.095]
        for ans, res in zip(answer, adj_vals):
            assert abs(ans - res) < 1e-5


    def test_two_groups(self):
        vals = [1, 2, 3, 8, 5]
        grps_1 = ['USA', 'USA', 'USA', 'USA', 'USA']
        grps_2 = ['MA', 'RI', 'CT', 'CT', 'CT']
        weights = [.65, .35]

        adj_vals = group_adjust(vals, [grps_1, grps_2], weights)
        # 1 - (.65 * 3.8 + .35 * 1.0) = -1.82
        # 2 - (.65 * 3.8 + .35 * 2.0) = -1.17
        # 3 - (.65 * 3.8 + .35 * 5.33333) = -1.33666
        answer = [-1.82, -1.17, -1.33666, 3.66333, 0.66333]
        for ans, res in zip(answer, adj_vals):
            assert abs(ans - res) < 1e-5


    def test_missing_vals(self):
        # If you're using NumPy or Pandas, use np.NaN
        # If you're writing pyton, use None
        # vals = [1, np.NaN, 3, 5, 8, 7]
        vals = [1, None, 3, 5, 8, 7]
        grps_1 = ['USA', 'USA', 'USA', 'USA', 'USA', 'USA']
        grps_2 = ['MA', 'RI', 'RI', 'CT', 'CT', 'CT']
        weights = [.65, .35]

        adj_vals = group_adjust(vals, [grps_1, grps_2], weights)

        # This should be None or np.NaN depending on your implementation
        # please feel free to change this line to match yours
        # answer = [-2.47, np.NaN, -1.170, -0.4533333, 2.54666666, 1.54666666]
        answer = [-2.47, None, -1.170, -0.4533333, 2.54666666, 1.54666666]

        for ans, res in zip(answer, adj_vals):
            if ans is None:
                assert res is None
            elif np.isnan(ans):
               assert np.isnan(res)
            else:
                assert abs(ans - res) < 1e-5


    def test_weights_len_equals_group_len(self):
        # Need to have 1 weight for each group

        # vals = [1, np.NaN, 3, 5, 8, 7]
        vals = [1, None, 3, 5, 8, 7]
        grps_1 = ['USA', 'USA', 'USA', 'USA', 'USA', 'USA']
        grps_2 = ['MA', 'RI', 'RI', 'CT', 'CT', 'CT']
        weights = [.65]

        with pytest.raises(ValueError):
            group_adjust(vals, [grps_1, grps_2], weights)


    def test_group_len_equals_vals_len(self):
        # The groups need to be same shape as vals
        vals = [1, None, 3, 5, 8, 7]
        grps_1 = ['USA']
        grps_2 = ['MA', 'RI', 'RI', 'CT', 'CT', 'CT']
        weights = [.65]

        with pytest.raises(ValueError):
            group_adjust(vals, [grps_1, grps_2], weights)


    def test_performance(self):
        vals = 1000000*[1, None, 3, 5, 8, 7]
        # If you're doing numpy, use the np.NaN instead
        # vals = 1000000 * [1, np.NaN, 3, 5, 8, 7]
        grps_1 = 1000000 * [1, 1, 1, 1, 1, 1]
        grps_2 = 1000000 * [1, 1, 1, 1, 2, 2]
        grps_3 = 1000000 * [1, 2, 2, 3, 4, 5]
        weights = [.20, .30, .50]

        start = datetime.now()
        group_adjust(vals, [grps_1, grps_2, grps_3], weights)
        end = datetime.now()
        diff = end - start
        sys.stdout.write("diff time here: {}\n".format(diff))
        print(diff)

# if __name__ == "__main__":
#     test_three_groups()
#     test_two_groups()
#     test_missing_vals()
#     test_weights_len_equals_group_len()
#     test_group_len_equals_vals_len()
#     test_performance()


if __name__ == "__main__":
    foo = TestClass()
    foo.test_performance()