"""
Python Coding Exercise: Warehouse
=================================

You should implement your code in this file. See `README.txt` for full
instructions and more information.
"""

from collections import OrderedDict

__author__ = "Richard Bibeault"
__email__  = "RichardMBibeault@gmail.com"
__date__   = "2019-09-28"

#==============================================================================
#
#==============================================================================

class Item:
    """ Example class for an item in the warehouse management system. You may
        modify or extend this in any way you need.
    """
    def __init__(self, size):
        self.size = size
        self.parent = None


#==============================================================================
#--- YOUR CODE GOES HERE.
#    At a minimum, you must define classes for Warehouse, Shelf, Bin, Box, and
#    Bag. You may define whatever else you may need as well.
#==============================================================================


class Container(Item):
    def __init__(self, size):
        super().__init__(size)
        self.capacity_left = size
        self.storage = OrderedDict()
        self.capacity_left = self.size

    def __len__(self):
        """
        Returns number of Items directly in container
        """
        return len(self.storage)

    def count(self):
        """
        Gets the total count of all items in container
        """
        total = 0
        for item in self.storage():
            if isinstance(item, Container):
                total += item.count()
            else:
                total += 1
        return total

    def contains(self, thing):
        """
        Using magic __contains__ checks if thing is in itself
        """
        return thing in self

    def __contains__(self, thing):
        """
        Checks if thing is in self directly or in a item in self
        """
        for stuff in self.storage:
            if stuff is thing:
                return True
            elif isinstance(stuff, Container):
                if thing in stuff:
                    return True
        return False

    def add(self, thing):
        """
        Attempts to put a given object in the Container, returns False if
        there is not enough room.
        """
        if thing.size <= self.capacity_left and \
            not isinstance(thing, type(self)):
            # adds thing to self
            self.storage[thing] = thing
            self.capacity_left -= thing.size
            # removes thing from previous parent
            if thing.parent:
                thing.parent.remove(thing)
            thing.parent = self # sets self to parent of thing
            return True
        elif thing.size < self.capacity_left and \
            isinstance(thing, type(self)):
            # adds thing to self
            self.storage[thing] = thing
            self.capacity_left -= thing.size
            # removes thing from previous parent
            if thing.parent:
                thing.parent.remove(thing)
            thing.parent = self # sets self to parent of thing
            return True
        return False

    def remove(self, *list_of_things):
        """
        removes a list of things from self
        """
        if not list_of_things:
            return self.storage.popitem()[0]
        for thing in list_of_things:
            if thing in self:
                if thing in self.storage:
                    self.capacity_left += thing.size
                    return self.storage.pop(thing)

    def extract(self, thing):
        """
        Removes thing from self or any subcontainer of self
        """
        if thing in self:
            if thing in self.storage:
                self.capacity_left += thing.size
                return self.storage.pop(thing)
            else:
                # checks all containers in self
                for stuff in self.storage:
                    if isinstance(stuff, Container) and thing in stuff:
                        stuff.capacity_left += thing.size
                        return stuff.extract(thing)

    def pack(self, thing):
        """
        Adds thing to self, and if there is no room in self directly, finds a
        sub container with room for thing
        """
        if not self.add(thing):
            for stuff in self.storage:
                if stuff.add(thing):
                    return True
        return False


class Warehouse(Container):
    """
    Container with infinite size
    """
    def __init__(self):
        super().__init__(float("inf"))


class Shelf(Container):
    """
    Container with size 100
    """
    def __init__(self):
        super().__init__(100)
        self.min_item_size = 7

    def add(self, thing):
        # makes sure that Items have size greater than min_item_size
        if type(thing) is Item:
            if thing.size <= self.min_item_size:
                return False
        if thing.size <= self.capacity_left and \
            not isinstance(thing, type(self)):
            self.storage[thing] = thing
            self.capacity_left -= thing.size
            return True
        elif thing.size < self.capacity_left and \
            isinstance(thing, type(self)):
            self.storage[thing] = thing
            self.capacity_left -= thing.size
            return True
        else:
            return False


class Bin(Container):
    """
    Container with size 10
    """
    def __init__(self):
        super().__init__(10)


class Box(Container):
    """
    Container with size 5
    """
    def __init__(self):
        super().__init__(5)


class Bag(Container):
    """
    Container with size 2
    """
    def __init__(self):
        super().__init__(2)


if __name__ == "__main__":
    print("foo")
    # foo = Shelf()
    # bar = Bin()

    # bar.add(foo)
    # bar.add(foo)
    # bar.add(foo)
    # print(bar.contains(foo))
