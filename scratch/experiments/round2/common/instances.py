from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Instance:
    id: str
    alias: str
    mu: tuple
    M: tuple
    honest: tuple
    focal: int
    index: int

    @property
    def K(self) -> int:
        return len(self.M)

    def is_honest(self, i: int) -> bool:
        return i in self.honest

    @property
    def M_top(self) -> float:
        return max(self.M)

    @property
    def M2(self) -> float:
        return sorted(self.M)[-2]

    def V(self, i: int) -> float:
        return max(m for j, m in enumerate(self.M) if j != i)

    @property
    def mu_H_star(self) -> float:
        return max(self.mu[h] for h in self.honest)


def load(path: Path | None = None) -> list[Instance]:
    with (path or HERE / "instances.json").open() as f:
        raw = json.load(f)["instances"]
    out = []
    for k, r in enumerate(raw):
        inst = Instance(r["id"], r["alias"], tuple(r["mu"]), tuple(r["M"]), tuple(r["honest"]), int(r["focal"]), k)
        for i in range(inst.K):
            assert 0.0 <= inst.mu[i] <= inst.M[i] <= 1.0, inst.id
        assert len(inst.honest) >= 1 and inst.focal not in inst.honest, inst.id
        out.append(inst)
    ids = [i.id for i in out] + [i.alias for i in out]
    assert len(ids) == len(set(ids)), "duplicate instance names"
    return out


def get(name: str, path: Path | None = None) -> Instance:
    for inst in load(path):
        if name in (inst.id, inst.alias):
            return inst
    raise KeyError(name)
