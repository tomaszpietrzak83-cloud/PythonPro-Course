class A: ...


class B(A): ...


class C(A): ...


class D(B): ...


class E(C): ...


class F(D, E): ...


"""
mermaid graph TD
    B --> A
    C --> A
    D --> B
    E --> C
    F --> D
    F --> E
"""


print(F.mro())
