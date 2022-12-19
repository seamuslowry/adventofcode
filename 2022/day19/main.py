
from dataclasses import dataclass
from enum import Enum
from functools import reduce

# this is used for types of robots, minerals currently collected, and costs to build robots
# it's doing a lot and gets confusing, but it's also useful to be able to map between those things
class Mineral(Enum):
  ORE = 1
  CLAY = 2
  OBSIDIAN = 3
  GEODE = 4

@dataclass
class Blueprint:
  id: int
  # first dict is robot type to a map representing the cost
  # second dict is type of mineral to number needed to build robot
  costs: dict[Mineral, dict[Mineral, int]]

@dataclass(eq=True, frozen=True)
class RobotState:
  producing: int
  building: int

@dataclass(eq=True, frozen=True)
class MiningState:
  robots: dict[Mineral, RobotState]
  minerals: dict[Mineral, int]
  max_minerals: dict[Mineral, int]

  def __hash__(self):
    return hash(
      tuple(
        [
          *list(map(lambda r: r.producing, self.robots.values())),
          *list(map(lambda m: m, self.minerals.values())),
          # I get my right answers slightly faster without this in the hash,
          # but I'm not convinced it isn't necessary
          *list(map(lambda r: r.building, self.robots.values()))
        ]
      )
    )

  def produce(self) -> 'MiningState':
    return MiningState(
      minerals={k:min(v + self.robots[k].producing, self.max_minerals[k] * 2) for k,v in self.minerals.items()},
      robots={**self.robots},
      max_minerals={**self.max_minerals}
    )

  def build(self, robot: Mineral, blueprint: Blueprint) -> 'MiningState':
    cost = blueprint.costs[robot]
    spent_minerals = {}
    for k,v in cost.items():
      spent_minerals[k] = self.minerals[k] - v

    new_minerals = {
      **self.minerals,
      **spent_minerals
    }

    if (any(val < 0 for val in [new_minerals[Mineral.ORE], new_minerals[Mineral.CLAY], new_minerals[Mineral.OBSIDIAN]])):
      raise ValueError("can't build with what you don't have")


    return MiningState(
      robots={k:RobotState(building=v.building + int(k==robot),producing=v.producing) for k,v in self.robots.items()},
      minerals=new_minerals,
      max_minerals={**self.max_minerals}
    )
  
  def finish_building(self) -> 'MiningState':
    return MiningState(
      minerals={**self.minerals},
      max_minerals={**self.max_minerals},
      robots={k:RobotState(producing=v.producing + v.building, building=0) for k,v in self.robots.items()}
    )

known_solutions: dict[int,int] = {}

def evaluate_blueprint(blueprint: Blueprint, state: MiningState, steps: int = 24) -> int:
  state_hash = hash((state, steps))
  if state_hash in known_solutions:
    return known_solutions[state_hash]
  if steps <= 0:
    return state.minerals[Mineral.GEODE]

  # try building robots
  productions = []

  for robot in Mineral:
    new_state = state
    if new_state.robots[robot].producing < new_state.max_minerals[robot]:
      try:
        new_state = new_state.build(robot, blueprint)
      except:
        pass
    new_state = new_state.produce()
    new_state = new_state.finish_building()
    productions.append(evaluate_blueprint(blueprint, new_state, steps - 1))

  ret = max(productions, default=0)
  known_solutions[state_hash] = ret
  return ret

def read_line(line: str) -> Blueprint:
  splits = line.split(" ")
  id = int(splits[1][:-1])
  ore_robot_cost = {Mineral.ORE:int(splits[6])}
  clay_robot_cost = {Mineral.ORE:int(splits[12])}
  obsidian_robot_cost = {Mineral.ORE:int(splits[18]), Mineral.CLAY:int(splits[21])}
  geode_robot_cost = {Mineral.ORE:int(splits[27]), Mineral.OBSIDIAN:int(splits[30])}
  return Blueprint(
                id,
                costs={
                  Mineral.ORE: ore_robot_cost,
                  Mineral.CLAY: clay_robot_cost,
                  Mineral.OBSIDIAN: obsidian_robot_cost,
                  Mineral.GEODE: geode_robot_cost,
                }
        )

# this is NOOOOOOT fast
def evaluate_blueprints(blueprints: list[Blueprint], steps: int) -> list[int]:
  vals: list[int] = []
  for b in blueprints:
    known_solutions.clear()
    vals.append(evaluate_blueprint(b, MiningState(
      robots={
        Mineral.ORE: RobotState(1,0),
        Mineral.CLAY: RobotState(0,0),
        Mineral.OBSIDIAN: RobotState(0,0),
        Mineral.GEODE: RobotState(0,0)
      },
      minerals={
        Mineral.ORE: 0,
        Mineral.CLAY: 0,
        Mineral.OBSIDIAN: 0,
        Mineral.GEODE: 0
      },
      max_minerals={
        Mineral.ORE: max(map(lambda v: v.get(Mineral.ORE, 0), b.costs.values())),
        Mineral.CLAY: max(map(lambda v: v.get(Mineral.CLAY, 0), b.costs.values())),
        Mineral.OBSIDIAN: max(map(lambda v: v.get(Mineral.OBSIDIAN, 0), b.costs.values())),
        Mineral.GEODE: 100000
      }
    ), steps))
  return vals


def p1():
  input = open("input.txt", "r").read().splitlines()
  blueprints = list(map(read_line, input))
  vals = evaluate_blueprints(blueprints, 24)
  return sum(map(lambda t: (t[0] + 1) * t[1], enumerate(vals)))

def p2():
  input = open("input.txt", "r").read().splitlines()
  blueprints = list(map(read_line, input))
  vals = evaluate_blueprints(blueprints[:3], 32)
  return reduce(lambda a,b: a*b,vals)

print(p1())
print(p2())