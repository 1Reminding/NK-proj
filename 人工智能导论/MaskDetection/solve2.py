import angr
import claripy
def hook demo(state):(
	state.regs.eax)=0
p= angr.Project("./issue",load_options={"auto load libs": False})
p.hook(addr=0x08048485,hook=hook demo,length=2)
state = p.factory.blank state(addr=0x0804846B,
							  add options={"SYMBOLIC WRITE ADDRESSES"})
u= claripy.BVs("u",8)
state.memory.store(0x804A021，u)
sm= p.factory.simulation manager(state)
sm.explore(find=8x980484DB)
st = sm.found[e]
print(repr(st.solver.eval(u)))