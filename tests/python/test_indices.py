from taichi.lang.misc import get_host_arch_list

import taichi as ti


@ti.test(arch=get_host_arch_list())
def test_indices():
    a = ti.field(ti.f32, shape=(128, 32, 8))

    b = ti.field(ti.f32)
    ti.root.dense(ti.j, 32).dense(ti.i, 16).place(b)

    mapping_a = a.snode.physical_index_position()

    assert mapping_a == {0: 0, 1: 1, 2: 2}

    mapping_b = b.snode.physical_index_position()

    assert mapping_b == {0: 0, 1: 1}
    # Note that b is column-major:
    # the virtual first index exposed to the user comes second in memory layout.

    @ti.kernel
    def fill():
        for i, j in b:
            b[i, j] = i * 10 + j

    @ti.kernel
    def get_field_addr(i: ti.i32, j: ti.i32) -> ti.u64:
        return ti.get_addr(b, [i, j])

    fill()
    for i in range(16):
        for j in range(32):
            assert b[i, j] == i * 10 + j
    assert get_field_addr(0, 1) + 4 == get_field_addr(1, 1)


@ti.test(arch=get_host_arch_list())
def test_float_as_index():
    a = ti.field(ti.f32, (8, 5))

    @ti.kernel
    def func():
        i = 6.66
        j = 3
        I = ti.Vector([2, 1])
        for _ in range(1):  # prevent constant fold
            a[i, j] = 233
            a[I + ti.Vector([1, 3.0])] = 666

    func()

    assert a[6, 3] == 233
    assert a[3, 4] == 666
