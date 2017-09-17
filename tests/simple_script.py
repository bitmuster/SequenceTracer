
expected_diagram="""seqdiag {
    edge_length = 140;
    span_height = 5;
    None;None_do_stuff;None_do_more_stuff;
    None -> None_do_stuff [label = "do_stuff"];
    None_do_stuff -> None_do_more_stuff [label = "do_more_stuff"];
    None_do_stuff <-- None_do_more_stuff;
    None <-- None_do_stuff;
}
"""

def do_more_stuff():
    pass

def do_stuff():
    do_more_stuff()

if __name__ == '__main__':

    do_stuff()
