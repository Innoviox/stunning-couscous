import cpu
import cProfile
import pstats
def time(f, n):
    print(cpu.timeit.timeit(f, number=n))
    #for i in range(n):
        #print(cpu.timeit.timeit(f, number=1))
def fight():
    
##    c = CPU()
##    c2 = CPU()
##    m=[]
##    while distribution: #(c.rack and c2.rack) or 
##        m.append(c._run())
##        print(m)
##        c2.board = c.board
##        m.append(c2._run())
##        print(m)
##        c.board = c2.board
##        print(c.score, c2.score)
    c = cpu.CPU()
##    def a():
##        c.board.getWords(c.board.board)
##    def d():
##        c.board.checkBoard(c.board.board)
##    def e():
##        for i in c.generate():pass
##    def f():
##        b.getScore()
##    def g():
##        pass
##        #b.getEvaluation(c.rack)

    m=[]
    while c.distribution:
        print(len(c.distribution))
        c = cpu.CPU()
        b = c._run()
        m.append(b)
        print(m)

##        time(a, 1000)
##        time(d, 1000)
##        time(f, 1000)
##        time(g, 1000)
        #time(e, 5)
        
    
if __name__ == "__main__":

    c = cpu.CPU()
    while c.distribution:
        cProfile.run('c._run()', 'run.profile')
        stats = pstats.Stats('run.profile')
        stats.strip_dirs().sort_stats('time').print_stats(15)
        input()
##    from pycallgraph import PyCallGraph
##    from pycallgraph.output import GraphvizOutput
##
##    with PyCallGraph(output=GraphvizOutput()):
##        c._run()
    #fight()
