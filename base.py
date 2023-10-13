# [Checked, North, South, East, West, display=" ",extra1,extra2]
class maze:
    def __init__(self,height,width):
        self.width,self.height=width,height
        self.grid=[[[0,1,1,1,1," ",0,0] for _ in range(width)] for _ in range(height)]
    def __getitem__(self,index):
        x,y=index
        return self.grid[y][x]
    def __setitem__(self,key,value):
        x,y=key
        self.grid[y][x]=value
        
    @property
    def display(self):
        final="+"
        final+="-"*((self.width*3)-1)
        final+="+"
        final+="\n"
        for row in self.grid:
            curA="|"
            curB="+"
            for cell in row:
                curA+=cell[5]+" "
                curA+="|" if cell[3] == 1 else " "
                curB+="--" if cell[2] == 1 else "  "
                curB+="+"
            # curA+="|"
            # curB+="|"
            final+=curA+"\n"+curB+"\n"
        # final+="+"
        # final+="-"*(self.width*3)
        # final+="+"
        return final

def test_maze():
    cur=maze(10,10)
    cur[5,5]=[0,0,0,0,0]
    print(cur[0,0])
    print(cur[5,5])
    print(cur[9,9])
    print(cur.display)