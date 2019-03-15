

def main():

    sections = input()

    sections.replace(' ', '').split(',')

    #for i in range(len(nodes)):
        #create a node with the last input
    
    numProb = int(input())

    probabilities = []

    for i in range(numProb):
        probabilities.append(input())
        probabilities[i] = probabilities[i].replace(' ', '').replace('=', ',').replace('|', ',').split(',')
        print(probabilities[i])
        
    numQueries = int(input())
    
    queries = []
    
    for i in range(numQueries):
        queries.append(input())
        queries[i] = queries[i].replace(' ', '').replace('|', ',').split(',')

if __name__ == '__main__':
  main()
  