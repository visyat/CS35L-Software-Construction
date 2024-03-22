import os
import sys
import zlib

#Used strace to check whether any commands were utilized.
#The output file contained no results, indicated that no git commands (or shell commands of any kind) were used in in my process.

#STEP 1: Discover the .git directory
def find_top_level ():
    #Find current working directory, since topo_order_commits.py doesn't need to be in the same dir
    curr_dir = os.getcwd()
    found = False
    reach_root = False

    while found == False and reach_root == False:
        if '.git' in os.listdir(curr_dir):
            #print (os.listdir(curr_dir))
            found = True

        #Finds immediate parent directory
        parent_dir = os.path.dirname(curr_dir)
        #Check if the current directory is the root -> write to standard error
        if curr_dir == parent_dir:
            sys.stderr.write('Not inside a Git repository') #Status of 1?
            reach_root = True

        #Bugfix: After finding the top-level directory, it was still incrementing the parent.
        if found == False:
            curr_dir = parent_dir

    if (found):
        return curr_dir

#STEP 3: Build the commit graph
class CommitNode:
    def __init__(self, commit_hash, head=''):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()
        self.branch_head = head

    #Used the __repr__ function to print out/test outputs of the nodes
    def __repr__ (self):
        output = self.commit_hash
        # output = "Node: " + self.commit_hash[:4]
        # if len(self.parents) > 0:
        #     output += " P: " + str([s.get_hash()[:4] for s in self.parents])
        # if len(self.children) > 0:
        #     output += " C: " + str([s.get_hash()[:4] for s in self.children])
        if len(self.branch_head) > 0:
            output += " " + str(self.branch_head)
        return output

    #Functions to set parent and child nodes, the commit hashes, and whetheer the node was a branch head or not
    def get_hash (self):
        return self.commit_hash
    def get_head(self):
        return self.branch_head
    def get_parents(self):
        return self.parents
    def get_children(self):
        return self.children

    def set_parent (self, p_commit):
        self.parents.add(p_commit)
    def set_child (self, c_commit):
        self.children.add(c_commit)
    def set_head(self, branch):
        self.branch_head = branch

def traverse_branch (top_level, node, root_commits):
    # Takes input hash and converts it to CommitNode object, adds to directory of nodes
    #c = CommitNode(node_hash)
    #print ()

    node_hash = node.get_hash()
    head = node.get_head()

    if node_hash in [s.get_hash() for s in root_commits]:
        node = root_commits[[s.get_hash() for s in root_commits].index(node_hash)]
        if len(head) > 0 and node.get_head().find(head) == -1:
            if len(node.get_head()) > 0:
                #print (node.get_head().split())
                node.set_head(node.get_head() + ' ' + head)
            else:
                node.set_head(head)
    else:
        root_commits.append(node)
    #This was needed because the function was returning ValueErrors; only process a new node if a hash can be successfully retrieved
    try:
        #print (os.path.join(top_level, '.git/objects', node_hash[:2], node_hash[2:]))
        comp_contents = open(os.path.join(top_level, '.git/objects', node_hash[:2], node_hash[2:]), 'rb').read()
        decomp_contents = zlib.decompress(comp_contents)
    except:
        return

    # if head == 'populate':
    #     find_tree = decomp_contents.find(b'tree ')
    #     tree = str(decomp_contents[find_tree+5: find_tree+45])[2:-1]
    #     node.set_head(tree)

    #Iteratively extract the parents from each decompressed git object file
    parents = []
    start_i = decomp_contents.find(b'parent ')
    while (start_i != -1):
        parents.append (decomp_contents[start_i+7:start_i+47])
        decomp_contents = decomp_contents[start_i+47:]
        start_i = decomp_contents.find(b'parent ')
    parents = [str(i)[2:-1] for i in parents]

    #Since this is not a binary tree, and nodes can have many possible parents, had to nest the recursive call inside a for loop. Likely leads to memory issues however.
    for p in parents:
        if p in [s.get_hash() for s in root_commits]:
            p_node = root_commits[[s.get_hash() for s in root_commits].index(p)]
        else:
            p_node = CommitNode (p)
        p_node.set_child(node) #p_node.set_child(node_hash)
        node.set_parent(p_node) #node.set_parent(p)

        traverse_branch (top_level, p_node, root_commits)

def depth_first_pop (top_level):
    branch_paths = []
    branch_names = []

    #Gets all the branch names and HEADs from .git/refs/heads
    for dirpath, _, files in os.walk(os.path.join(top_level, '.git/refs/heads')):
        for f in files:
            path = os.path.join(dirpath, f)
            branch_paths.append(path)
            branch_names.append(path.replace(os.path.join(top_level, '.git/refs/heads/'), ''))
    branch_heads = [open(b, 'r').read()[:-1] for b in branch_paths]
    root_commits = []

    #Traverses each branch from the HEAD and populates the list of commits
    for i in range(len(branch_heads)):#b in branch_heads:
        #print ('branch ' + branch_names[branch_heads.index(b)] + ' traversed')
        b_node = CommitNode (branch_heads[i], branch_names[i])
        traverse_branch(top_level, b_node, root_commits)
    return root_commits
    #return list(reversed(root_commits))

def get_node_height(node):
    #Helper function to get the height (distance from root) of a node, used for topological ordering
    if len(node.get_parents()) == 0:
        return 0
    else:
        return 1 + max([get_node_height(p) for p in node.get_parents()])
def print_node(node, printed_commits, sticky_end = False):
    #Function to print out nodes as well as sticy ends - had some challenges!
    if node in printed_commits:
        return
    elif (node.get_children() <= printed_commits) == False:
        if len(node.get_children()) == 1:
            print_node(list(node.get_children())[0], printed_commits, sticky_end)
        else:
            print(node.get_hash() + '=\n')
        #print(node.get_hash()[:4])
            for c in node.get_children():
                print_node(c, printed_commits, True)
    else:
        if sticky_end:
            print ('=' + ' '.join(list([s.get_hash() for s in node.get_children()])))

        print(node)
        printed_commits.add(node)
        for p in node.get_parents():
            print_node(p, printed_commits, False)

def print_topo_order(root_commits):
    #prints out the nodes in topological order, sorting by height
    heights = []
    for n in root_commits:
        h = get_node_height(n)
        heights.append(h)
    heights, root_commits = zip(*reversed(sorted(zip(heights, root_commits), key=lambda x: x[0])))
    print_node(root_commits[0], set())

def topo_order_commits():
    #Main Driver Function - runs all of the above methods; gets list of nodes and prints them out with necessary additions
    top_level = find_top_level()
    if top_level != None:
        #print (top_level)
        root_commits = depth_first_pop (top_level)
        print_topo_order(root_commits)

if __name__ == '__main__':
    topo_order_commits()
