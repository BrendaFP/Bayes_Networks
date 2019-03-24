class BayesNode:
  def __init__(self, name, parents, p_table):
    self.name = name
    self.parents = parents
    self.p_table = p_table

def generateParents(current, nodes, node):
    parents = []
    if len(current) > 1:
      for current_node in current:
        for aux in nodes:
          if aux in current_node and aux != node and aux not in parents:
            parents.append(aux)
    return parents
    
def generateProbTable(current,node):
    p_table = {}
    for nodes in current:
      (sections, value) = nodes.split('=')
      section_names = sections.split("|")
      
      name = section_names[0]
      names = []
      if len(section_names) > 1:
        names = section_names[1].split(",")
        names.sort(key=lambda x: x[1:])
        aux = name + "|"
      else:
          aux = name
      for given in names:
        if given[1:] != node:
          aux = aux + given
        else:
          aux = aux + node
          
      true_name = '+' + aux[1:]
      false_name = '-' + aux[1:]
      p_table[true_name] = float(value)
      p_table[false_name] = 1 - float(value)
    #print("p_t",p_table)
    return p_table
    
def bayes_net(nodes, probabilities):
  network = {}
  
  for node in nodes:
    current = list(filter(lambda x: (x[0:x.find('|')]).count(node) > 0, probabilities))

    parents = generateParents(current,nodes,node)
    p_table = generateProbTable(current,node)
    
    network[node] = BayesNode(node, parents, p_table)

  return network
  
def main():

    sections = input()

    nodes=sections.replace(' ', '').split(',')
    
    numProb = int(input())

    probabilities = []

    for i in range(numProb):
        probabilities.append(input())
        #print(probabilities[i])
        
    bayes_network = bayes_net(nodes, probabilities)
    
    numQueries = int(input())
    
    queries = []
    
    for i in range(numQueries):
        queries.append(input())
        queries[i] = queries[i].replace(' ', '').replace('|', ',').split(',')

if __name__ == '__main__':
  main()
  