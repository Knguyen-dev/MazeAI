class UnionFind:
  def __init__(self, size):
    # Create list of indices = [0, ..., size-1]
    self.parent = list(range(size))  

    # Create a list of ranks, all initialized to 0
    self.rank = [0] * size  # Rank used for union by rank

  def findRoot(self, node):
    """Finds the root of the given node with path compression.

    Args:
        node (int): The node whose root is to be found. Node is just an index position.

    Returns:
        int: The root of the node. Again corresponds to an index position
    """
    if (node == self.parent[node]):
      return node
    
    # Find the root of the parent node
    res = self.findRoot(self.parent[node])

    # At this point we find the root of the entire tree
    # Update the current node's parent to be the root of the entire tree
    self.parent[node] = res

    return res
  
  def unionByRank(self, x, y) -> None:
    """Unites two sets containing x and y using union by rank.
    Args:
        x (int): An element in the first set; 
        y (int): An element in the second set; 

    NOTE: x and y are both indices 
    """
    root_x = self.findRoot(x)
    root_y = self.findRoot(y)

    # If their roots are the same, then they belong to the same group; no need to merge
    if (root_x == root_y):
      return
    
    '''
    - If x's root has a lower rank than y's root:
      We'll need to make root_x a child of root_y
    - Else if y has a lower rank, make y a child of x.

    - Else, they're both equal, it doesn't matter how we merge, so we'll 
      make root_X a child of root_y. However you'll have to increase the rank of root_y's tree.
    '''
    if self.rank[root_x] < self.rank[root_y]:
      self.parent[root_x] = root_y
    elif self.rank[root_x] > self.rank[root_y]:
      self.parent[root_y] = root_x
    else:
      self.parent[root_x] = root_y
      self.rank[root_y] += 1

  def connected(self, x, y):
    """Checks if two elements are in the same set.

    Args:
        x (int): The first element.
        y (int): The second element; again x and y are indices.

    Returns:
        bool: True if x and y are in the same set, False otherwise.
    """
    return self.findRoot(x) == self.findRoot(y)    
    
