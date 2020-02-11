import nimpy

proc adder(a: int, b: int): int {.exportpy.} =
    a + b
