def printStar(width):

  if width % 2 == 0:
    print("Please input odd number!")
  else:
    x = 0
    spacelen = 0
    starlen = 0
    for i in range(width,0,-2):
      spacelen = x
      starlen = width - x * 2
      x = x + 1 
      print(' '*spacelen + '*'*starlen)
    
    x = x - 2
    for j in range(3,width+1,2):
      spacelen = x
      starlen = j
      x = x - 1
      print(' '*spacelen + '*'*starlen)

printStar(21)