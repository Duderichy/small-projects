# Coverage Calculations on Next Generation Sequencing data

To calculate coverage for the given sequencing data, I first investigated a few things. I look at the maximum and minimum value of columns. From looking at the first column I saw that there was a large maximum value, and a small minimum value. This meant that using an array to store lookups would be expensive in terms of memory, because I would need to cover from the beginning to the end. For simplicity, I decided to go with a defaultdict, which allowed me to also pass in an array without changing the code if I wanted to, to see performance differences. The somewhat small maximum value of the second column with the read lengths encouraged me to try brute forcing calculating all the read depths into one massive lookup table (the final solution uses a defaultdict). This allowed me to do all computation for determining read depth ahead of time, so that each lookup would be constant with respect to time.

## Time Complexity Considerations

The time complexity of the solution I have included is O(n * k) where n is the number of reads, and k is the length of the maximum read for the creation of the lookup table. This is essentially O(n^2), which is slow from a theoretical perspective, and can easily become dangerous for large inputs (especially if average read length grows significantly in this case). Doing all the computations up front means that lookups are O(1) time, so doing n lookups for coverage is O(n). This is O(n) on memory usage.

A different solution could involve sorting the data, and checking if a lookup is included in certain reads. By knowing the maximum value of column two, we know we ony need to check up to that maximum below the desired read, because anything less than that wouldn't be long enough to reach the desired read location. Then we would count the number of reads from that minimum to the desired read that reach it. This would be O(n log n) for initial calculation and then O(log n) for the binary search, + O(n) for the maximum length of column two. So the time complexity for all of the lookup calculations in the table would be O(n ^ 2). This solution would also be O(n) on memory usage, assuming we keep the whole file sorted in memory, and don't check it from disk.

Something that gives us better time complexity would be to count the number of starts in one array, and the number of ends in another array. As you step through the array you increase the number of coverage at a certain point every time you hit the start of a new read, and decriment it every time you hit the end of a read, since that read is no longer covering the current position. The time complexity of this would be linear on the input. Once you go through to add the start to start array, and end to end array. Then you go through and count up the starts and end to get coverage at each position. This allows you to get the lookup table in O(n) with O(n) memory, and allows you to do lookups in O(1), so doing n lookups takes O(n). This solution would have been vastly more efficient, but I ran out of time to code it up.
