# -*- coding: utf-8 -*-
#  Copyright 2011 Takeshi KOMIYA
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from __future__ import print_function

import unittest
from blockdiag.parser import parse_string, ParseException
from blockdiag.parser import Diagram, Group, Statements, Node, Edge


class TestParser(unittest.TestCase):
    def test_basic(self):
        # basic digram
        code = """
               diagram test {
                  A -> B -> C, D;
               }
               """

        tree = parse_string(code)
        self.assertIsInstance(tree, Diagram)

    def test_without_diagram_id(self):
        code = """
               diagram {
                  A -> B -> C, D;
               }
               """
        tree = parse_string(code)
        self.assertIsInstance(tree, Diagram)

        code = """
               {
                  A -> B -> C, D;
               }
               """
        tree = parse_string(code)
        self.assertIsInstance(tree, Diagram)

    def test_empty_diagram(self):
        code = """
               diagram {
               }
               """
        tree = parse_string(code)
        self.assertIsInstance(tree, Diagram)

        code = """
               {
               }
               """
        tree = parse_string(code)
        self.assertIsInstance(tree, Diagram)

    def test_diagram_includes_nodes(self):
        code = """
               diagram {
                 A;
                 B [label = "foobar"];
                 C [color = "red"];
               }
               """
        tree = parse_string(code)
        self.assertIsInstance(tree, Diagram)
        self.assertEqual(3, len(tree.stmts))
        self.assertIsInstance(tree.stmts[0], Statements)
        self.assertIsInstance(tree.stmts[0].stmts[0], Node)
        self.assertIsInstance(tree.stmts[1], Statements)
        self.assertIsInstance(tree.stmts[1].stmts[0], Node)
        self.assertIsInstance(tree.stmts[2], Statements)
        self.assertIsInstance(tree.stmts[2].stmts[0], Node)

    def test_diagram_includes_edges(self):
        code = """
               diagram {
                 A -> B -> C;
               }
               """
        tree = parse_string(code)
        self.assertIsInstance(tree, Diagram)
        self.assertEqual(1, len(tree.stmts))
        self.assertIsInstance(tree.stmts[0], Statements)
        self.assertEqual(2, len(tree.stmts[0].stmts))
        self.assertIsInstance(tree.stmts[0].stmts[0], Edge)
        self.assertIsInstance(tree.stmts[0].stmts[1], Edge)

        code = """
               diagram {
                 A -> B -> C [style = dotted];
                 D -> E, F;
               }
               """
        tree = parse_string(code)
        self.assertIsInstance(tree, Diagram)
        self.assertEqual(2, len(tree.stmts))
        self.assertIsInstance(tree.stmts[0], Statements)
        self.assertEqual(2, len(tree.stmts[0].stmts))
        self.assertIsInstance(tree.stmts[0].stmts[0], Edge)
        self.assertIsInstance(tree.stmts[0].stmts[1], Edge)
        self.assertIsInstance(tree.stmts[1], Statements)
        self.assertEqual(1, len(tree.stmts[1].stmts))
        self.assertIsInstance(tree.stmts[1].stmts[0], Edge)

    def test_diagram_includes_groups(self):
        code = """
               diagram {
                 group {
                   A; B;
                 }
                 group {
                   C -> D;
                 }
               }
               """
        tree = parse_string(code)
        self.assertIsInstance(tree, Diagram)
        self.assertEqual(2, len(tree.stmts))

        self.assertIsInstance(tree.stmts[0], Group)
        self.assertEqual(2, len(tree.stmts[0].stmts))
        self.assertIsInstance(tree.stmts[0].stmts[0], Statements)
        self.assertIsInstance(tree.stmts[0].stmts[0].stmts[0], Node)
        self.assertIsInstance(tree.stmts[0].stmts[1], Statements)
        self.assertIsInstance(tree.stmts[0].stmts[1].stmts[0], Node)

        self.assertIsInstance(tree.stmts[1], Group)
        self.assertEqual(1, len(tree.stmts[1].stmts))
        self.assertIsInstance(tree.stmts[1].stmts[0], Statements)
        self.assertIsInstance(tree.stmts[1].stmts[0].stmts[0], Edge)

    def test_diagram_includes_diagram_attributes(self):
        code = """
               diagram {
                 fontsize = 12;
                 node_width = 80;
               }
               """
        tree = parse_string(code)
        self.assertIsInstance(tree, Diagram)
        self.assertEqual(2, len(tree.stmts))

    def test_parenthesis_ness(self):
        with self.assertRaises(ParseException):
            code = ""
            parse_string(code)
