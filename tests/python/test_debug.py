import pytest

import taichi as ti


def test_cpu_debug_snode_reader():
    ti.init(arch=ti.x64, debug=True)

    x = ti.field(ti.f32, shape=())
    x[None] = 10.0

    assert x[None] == 10.0


@ti.test(require=ti.extension.assertion, debug=True, gdb_trigger=False)
def test_cpu_debug_snode_writer_out_of_bound():
    x = ti.field(ti.f32, shape=3)

    with pytest.raises(RuntimeError):
        x[3] = 10.0


@ti.test(require=ti.extension.assertion, debug=True, gdb_trigger=False)
def test_cpu_debug_snode_writer_out_of_bound_negative():
    x = ti.field(ti.f32, shape=3)
    with pytest.raises(RuntimeError):
        x[-1] = 10.0


@ti.test(require=ti.extension.assertion, debug=True, gdb_trigger=False)
def test_cpu_debug_snode_reader_out_of_bound():
    x = ti.field(ti.f32, shape=3)

    with pytest.raises(RuntimeError):
        a = x[3]


@ti.test(require=ti.extension.assertion, debug=True, gdb_trigger=False)
def test_cpu_debug_snode_reader_out_of_bound_negative():
    x = ti.field(ti.f32, shape=3)
    with pytest.raises(RuntimeError):
        a = x[-1]


@ti.test(require=ti.extension.assertion, debug=True, gdb_trigger=False)
def test_out_of_bound():
    x = ti.field(ti.i32, shape=(8, 16))

    @ti.kernel
    def func():
        x[3, 16] = 1

    with pytest.raises(RuntimeError):
        func()


@ti.test(require=ti.extension.assertion, debug=True, gdb_trigger=False)
def test_not_out_of_bound():
    x = ti.field(ti.i32, shape=(8, 16))

    @ti.kernel
    def func():
        x[7, 15] = 1

    func()


@ti.test(require=ti.extension.assertion, debug=True, gdb_trigger=False)
def test_out_of_bound_dynamic():
    x = ti.field(ti.i32)

    ti.root.dynamic(ti.i, 16, 4).place(x)

    @ti.kernel
    def func():
        x[17] = 1

    with pytest.raises(RuntimeError):
        func()


@ti.test(require=ti.extension.assertion, debug=True, gdb_trigger=False)
def test_not_out_of_bound_dynamic():
    x = ti.field(ti.i32)

    ti.root.dynamic(ti.i, 16, 4).place(x)

    @ti.kernel
    def func():
        x[3] = 1

    func()


@ti.test(require=ti.extension.assertion, debug=True, gdb_trigger=False)
def test_out_of_bound_with_offset():
    x = ti.field(ti.i32, shape=(8, 16), offset=(-8, -8))

    @ti.kernel
    def func():
        x[0, 0] = 1

    with pytest.raises(RuntimeError):
        func()
        func()


@ti.test(require=ti.extension.assertion, debug=True, gdb_trigger=False)
def test_not_out_of_bound_with_offset():
    x = ti.field(ti.i32, shape=(8, 16), offset=(-4, -8))

    @ti.kernel
    def func():
        x[-4, -8] = 1
        x[3, 7] = 2

    func()
