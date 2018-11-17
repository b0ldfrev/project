import angr

def main():
    p = angr.Project("martricks")
    simgr = p.factory.simulation_manager(p.factory.full_init_state())
    simgr.explore(find=0x400A84, avoid=0x400A90)

    return simgr.found[0].posix.dumps(0).strip('\0\n')

if __name__ == '__main__':
   print main()
