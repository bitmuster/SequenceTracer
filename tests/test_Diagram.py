
import sys
import unittest
sys.path.append('./')
from sequencetracer import Diagram


d1=[
"""seqdiag {""",
"""    edge_length = 140;""",
"""    span_height = 5;""",
"""    None -> None [label = "_find_and_load"];""",
"""     Non""",
"""     Fini""",
"""    None <-- None;""",
"""}""",
""""""
]

d1_exp=[
"""seqdiag {""",
"""    edge_length = 140;""",
"""    span_height = 5;""",
"""}""",
""""""
]

d2=[
"""seqdiag {""",
"""    edge_length = 140;""",
"""    span_height = 5;""",
"""    None -> None [label = "_find_and_load"];""",
"""     None -> None [label = "print_stuff"];""",
"""      Non""",
"""      Fini""",
"""     None <-- None;""",
"""    None <-- None;""",
"""}""",
""""""
]

d2_exp=[
"""seqdiag {""",
"""    edge_length = 140;""",
"""    span_height = 5;""",
"""}""",
""""""
]

class TestDiagram(unittest.TestCase):

    def test_filter_find_and_load_1(self):
        d=Diagram()
        for f in d1:
            d.append(f)

        d.filter_find_and_load()
        self.assertEqual( d.getcontent(), d1_exp)

    def test_filter_find_and_load_2(self):
        d=Diagram()
        for f in d2:
            d.append(f)

        d.filter_find_and_load()
        self.assertEqual( d.getcontent(), d2_exp)

    def test_get_call_depth_0(self):
        d=Diagram()
        de=d.get_call_depth("""    None -> None [label = "_find_and_load"];""")
        self.assertEqual(de, 0)

    def test_get_call_depth_4(self):
        d=Diagram()
        de=d.get_call_depth("""        None -> None [label = "_find_and_load"];""")
        self.assertEqual(de, 4)
