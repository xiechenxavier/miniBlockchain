#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 07:16:24 2022

@author: xiechen
"""

class Node:

    def __init__(self, name, value, left_sub, right_sub):
        
        self.name = name
        self.value = value
        self.left_sub = left_sub
        self.right_sub = right_sub
        
    def printPrincipal(self):
        
        print('Name: ',self.name,'Value: ',self.value)
        if not(self.left_sub is None):
            print('Left node: ')
            self.left_sub.printPrincipal()
        if not(self.right_sub is None):
            print('Right node: ')
            self.right_sub.printPrincipal()
    
    # def check_A_value(self,h):
        
    #     if h == self.value:
    #         return True
            
        
    def getANodeByHash(self, h):
        
        if self.value == h:
            
            return Node(self.name, self.value, self.left_sub, self.right_sub)
        
        else:
            
            if self.left_sub is None and self.right_sub is None:
                return None
            
            if (self.left_sub.getANodeByHash(h) is None):
                
                return self.right_sub.getANodeByHash(h)
            
            if (self.right_sub.getANodeByHash(h) is None):
                
                return self.left_sub.getANodeByHash(h)

            
    def findFather(self,node):
        
        if not node is None:
            
            if self.left_sub is None and self.right_sub is None:
                
                return None
            
            if self.left_sub.name == node.name or self.right_sub.name == node.name:
                
                return Node(self.name,self.value,self.left_sub,self.right_sub)
            else:
                
                if (self.left_sub.findFather(node) is None):
                
                    return self.right_sub.findFather(node)
                
                elif(self.right_sub.findFather(node) is None):
                    
                    return self.left_sub.findFather(node)
        else:
            
            return None
        
        
    def findBrother(self,node):
        
        if not((node is None) or 
               self.left_sub is None or 
               self.right_sub is None) :
            if node.value == self.value:
                return None
            elif node.value == self.left_sub.value:
                return self.right_sub
            elif node.value == self.right_sub.value:
                return self.left_sub
            else:
                
                if self.left_sub.findBrother(node) is None:
                    return self.right_sub.findBrother(node)
                elif self.right_sub.findBrother(node) is None:
                    return self.left_sub.findBrother(node)
        else:
            return None
        
        
    def __str__(self):
        return str(self.__dict__)
    

# Node1 = Node('v0',14,None,None)
# print(Node1)
        
class Arbre_Merkle:
    
    def __init__(self,List_hash):
        
        self.root = self.Create_Arbre_Merkle(List_hash)
        
        
    def Create_Arbre_Merkle(self, List_hash):
        
        list_length = len(List_hash)
        if list_length > 0:
            
            if list_length == 1: # there is one single hash, arbre is a signle node(leave/root)
                
                return Node('v0', List_hash[0], None, None)
            
            else: # create the tree by following two steps
                
                List_nodes = [] # 1.create all leaves nodes
                
                for i in range(0,list_length):
                    
                    node_i = Node('v'+str(i),List_hash[i],None, None)
                    List_nodes.append(node_i)
                    
                return self.repetitive_action(List_nodes)
                
        else:
            return None
        
        
    def repetitive_action(self, List_nodes):
        
        len_nodes = len(List_nodes)
        
        if len_nodes == 1:
            
            return List_nodes[0]
        
        elif len_nodes % 2 == 0:
            
            fathers = []
            
            for i in range(0,len_nodes,2):
                
                # dealing with the name of father node
                Node_i = List_nodes[i]
                Node_j = List_nodes[i+1]
                daddy_name = 'v' + (Node_i.name + Node_j.name).replace('v','')
                
                father = Node(daddy_name, 
                              Node_i.value + Node_j.value,
                              Node_i,
                              Node_j)
                fathers.append(father)
                
            return self.repetitive_action(fathers)
        
        elif len_nodes % 2 == 1:
            
            fathers = []
            
            for i in range(0,len_nodes-1,2):
                
                # dealing with the name of father node
                Node_i = List_nodes[i]
                Node_j = List_nodes[i+1]
                daddy_name = 'v' + (Node_i.name + Node_j.name).replace('v','')
                
                father = Node(daddy_name, 
                              Node_i.value + Node_j.value,
                              Node_i,
                              Node_j)
                
                fathers.append(father)
            
            fathers.append(List_nodes[len_nodes-1])
                
            return self.repetitive_action(fathers)
        
    def printTree(self):
        
        self.root.printPrincipal()
        
    
    def getANodeByHash(self, h):
        
        return self.root.getANodeByHash(h)
    
        
    def Check_node_Normal(self, node):
        
        if node is None:
            return False
        
        found_tree_node = self.getANodeByHash(node.value) # the correct node found from tree
        
        if not found_tree_node is None:   
            
            return (found_tree_node.name == node.name and 
                    found_tree_node.value == node.value and
                    found_tree_node.left_sub == node.left_sub and
                    found_tree_node.right_sub == node.right_sub)
        else:
            return False
    
        
    def findFatherofaNode(self, node):
        
        if node is self.root:
        
            return None
        
        else:
            
            return self.root.findFather(node)
        
        
        
    def findBrother(self,node):
        
        return self.root.findBrother(node)
    
    
    def find_valid_frere_path(self, node, path):
        '''
        这个方法要把整条要用到的frere都找出来

        Parameters
        ----------
        node : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        
        if not node is None and self.Check_node_Normal(node):
            
            node_bro = self.findBrother(node) # first find its brother node
            if not node_bro is None:
                path.append(node_bro) # add its brother in path
                node_daddy = self.findFatherofaNode(node)
                if not node_daddy is self.root:
                    return path + self.find_valid_frere_path(node_daddy,[])
                else:
                    return path
        
        return path
    
    def simple_verification(self, node):
        
        return self.calcule_result_freres(node) == self.root.value
    
    def calcule_result_freres(self,node):
        
        if not(node is None) and self.Check_node_Normal(node):
        
            path_freres = self.find_valid_frere_path(node, [])
            
            return node.value+sum([frere.value for frere in path_freres])
        
        else:
            raise ValueError("Node is None or not in the tree")
                    
        

List_hash = [1213,21,30,444,51]
tree = Arbre_Merkle(List_hash)


# print(tree)
# tree.printTree()
Node1 = Node('v4',51,None,None)
# print(tree.Check_node_Normal(Node1))
# print(tree.getANodeByHash(Node1.value))
print(tree.simple_verification(Node1))
# path = tree.find_valid_frere_path(Node1, [])

# for nod in path:   
#     print(nod)
# print(tree.findFatherofaNode(Node1))
# for i in List_hash:
#     Node0 = tree.getANodeByHash(i)
#     print(Node0)
# print(tree.findBrother(Node0))






        