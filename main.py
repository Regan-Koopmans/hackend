from lark import Lark
parser_definition = open("lark_definition", "r").read()
l = Lark(parser_definition)
source_file = open("example.he", "r").read()
parsed = l.parse(source_file)
endpoints = [[
    c.children[0].children[0].data, 
    str(c.children[1].children[0].children[0]),
    str(c.children[2].children[0])] 
    for c in parsed.children]

body = ""
for endpoint in endpoints:
    if (endpoint[0] == "get"):
        body += """
  app.Get(""" + endpoint[1] + """, func(c *fiber.Ctx) {
    c.Send(""" + endpoint[2] + """)
  })\n"""

output_text = """// Generated from hackend

package main

import "github.com/gofiber/fiber"

func main() {
  app := fiber.New()
 """

output_text += body
output_text += """
  app.Listen(8080)
}
"""
output_file = open("output.go", "w")
output_file.write(output_text)
output_file.close()