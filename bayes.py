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
    for line in current:
      (sections, value) = line.split('=')
      section_names = sections.split("|")
      name = section_names[0]
      names = []
      if len(section_names) > 1:
        names = section_names[1].split(",")
        names.sort(key=lambda x: x[1:])
      aux = name + "|"
      for given in names:
        if given[1:] != node:
          aux = aux + given
        else:
          aux = aux + node
        aux += ','
      true_name = '+' + aux[1:-1]
      false_name = '-' + aux[1:-1]
      p_table[true_name] = float(value)
      p_table[false_name] = 1 - float(value)
    #print("p_t",p_table)
    return p_table
    
def bayes_net(nodes, probabilities):
  bayes_network = {}
  
  for node in nodes:
    current = list(filter(lambda x: (x[0:x.find('|')]).count(node) > 0, probabilities))

    parents = generateParents(current,nodes,node)
    p_table = generateProbTable(current,node)
    
    bayes_network[node] = BayesNode(node, parents, p_table)

  return bayes_network


def enumerate_all(evidence, bayes_network):
  prob = 1.0

  for ev in evidence:
    node = bayes_network[ev[1:]]
    name = ""
    if len(node.parents) == 0:
      name = ev
    else:
      given = []
      for parent in node.parents:
        if ('+' + parent) in evidence:
          given.append('+' + parent)
        else:
          given.append('-' + parent)
      given.sort(key=lambda x: x[1:])
      given = ",".join(given)
      name = ev + "|" + given
    prob = prob * node.p_table[name]

  return prob
  
def getAllCombinations(comb, i):
  all = []
  
  for aux in range(0, len(comb)):
    if i % 2 == 1:
      all.append('+' + comb[aux])
    else:
      all.append('-' + comb[aux])
    i //= 2

  return all
  
def enumeration(evidence, bayes_network):
  #print("ev",evidence)
  variables = [aux[1:] for aux in evidence]
  #To get the nodes and parents
  for node in variables:
    parents = bayes_network[node].parents
    for parent in parents:
      if parent not in variables:
        variables.append(parent)
  
  comb = []
  for v in variables:
    if not (('+' + v) in evidence or ('-' + v) in evidence):
      comb.append(v)

  n_combinations = pow(2, len(comb))

  sum = 0
  for i in range(n_combinations):
    all = getAllCombinations(comb, i)
    #print(genVariables)
    sum = sum + enumerate_all(evidence + all, bayes_network)
    #print("sum",sum)
  return sum
        
def getResult(queries,bayes_network):
    #print(len(queries))
    if len(queries) == 1:
      prob = enumeration(queries[0].split(","), bayes_network)
    else:
      prob =  enumeration(queries[0].split(",") + queries[1].split(","), bayes_network) / enumeration(queries[1].split(","), bayes_network)
    
    return prob
    
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
      queries[i] = queries[i].replace(' ', '').split('|')
  
    for i in range(len(queries)):
      prob = getResult(queries[i],bayes_network)
      print(round(prob, 7))
    
if __name__ == '__main__':
  main()
  
