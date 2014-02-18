import dis
import itertools
from ..symbolic import SymbolicExecution
from ..typing import Infer
from .. import types, compiler
from .support import testcase, main, assertTrue


def foo(a, b):
    sum = a
    sum = b
    if a == b:
        i = 0
        i = 1
        for i in range(b):
            sum += i
            i = 132
            i = 321

    return sum

@testcase
def test_type_coercion():
    signed = types.int8, types.int16, types.int32, types.int64
    unsigned = types.uint8, types.uint16, types.uint32, types.uint64
    real = types.float32, types.float64
    complex = types.complex64, types.complex128

    numerics = signed + unsigned + real + complex

    for fromty, toty in itertools.product(numerics, numerics):
        pts = fromty.try_coerce(toty)
        print '%s -> %s :: %s' % (fromty, toty, pts)

@testcase
def test_int64_to_float():
    assertTrue((types.int64.try_coerce(types.float32) >
                    types.int64.try_coerce(types.float64)),
               msg="int64 should prefer double")

@testcase
def test_infer():
    dis.dis(foo)
    se = SymbolicExecution(foo)
    se.interpret()

    for blk in se.blocks:
        print blk

    funclib, _ = compiler.get_builtin_context()
    

    infer = Infer(func = se.func,
                  blocks = se.blocks,
                  args = {'a': types.int32, 'b': types.int32},
                  return_type = types.int32,
                  funclib = funclib)
    infer.infer()
    
    for blk in se.blocks:
        print blk




if __name__ == '__main__':
    main()