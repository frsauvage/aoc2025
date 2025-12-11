# AoC 2025 Day 11 - Reactor (Solution NetworkX)

## Problème

Un réacteur toroïdal alimente une usine. Les données circulent entre des **devices** connectés par des **outputs** (flux unidirectionnel = DAG).

- **Part 1** : Compter les chemins de `you` vers `out` (574 chemins)
- **Part 2** : Compter les chemins de `svr` (server rack) vers `out` passant par `dac` ET `fft` (306 trillions de chemins)

## Solution

### Part 1 : NetworkX natif

Avec seulement 574 chemins, on peut énumérer directement :

```python
sum(1 for _ in nx.all_simple_paths(devices, YOU, REACTOR_OUTPUT))
```

### Part 2 : DP (Dynamic Program) sur DAG (Directed Acyclic Graph)

306 trillions de chemins = impossible à énumérer. On utilise la **programmation dynamique** :

```
nb_paths[device][devices_requis_vus] = nombre de chemins
```

L'algorithme :

1. **Tri topologique** : ordonner les devices pour que si A → B, alors A apparaît avant B dans la liste. C'est possible car les données ne remontent jamais (DAG).
2. **Propagation** : parcourir les devices dans cet ordre et propager les compteurs vers les outputs
3. **Résultat** : `nb_paths['out'][{'dac', 'fft'}]`

## Choix de lisibilité

### 1. Remplacement de `yield` par `itertools.combinations`

**Avant** (masque de bits obscur) :

```python
def all_subsets(devices_set):
    devices_list = list(devices_set)
    for i in range(1 << len(devices_list)):
        yield frozenset(devices_list[j] for j in range(len(devices_list)) if i & (1 << j))
```

**Après** (explicite) :

```python
from itertools import combinations
visit_states = [
    frozenset(subset)
    for size in range(len(must_visit) + 1)
    for subset in combinations(must_visit, size)
]
# {'dac', 'fft'} -> [set(), {'dac'}, {'fft'}, {'dac', 'fft'}]
```

### 2. Remplacement des opérateurs `&` et `|` par des méthodes nommées

**Avant** (opérateurs cryptiques) :

```python
initial_visited = frozenset({from_device}) & must_visit
new_visited = visited | ({output} & must_visit)
```

**Après** (méthodes explicites) :

```python
initial_visited = must_visit.intersection({from_device})
new_visited = visited.union(must_visit.intersection({output}))
```

| Opérateur | Méthode | Signification |
|-----------|---------|---------------|
| `&` | `.intersection()` | Éléments communs |
| `\|` | `.union()` | Tous les éléments |

### 3. Variables nommées selon le problème

| Variable générique | Variable métier |
|--------------------|-----------------|
| `G`, `graph` | `devices` |
| `node` | `device` |
| `neighbor` | `output` |
| `start`, `end` | `from_device`, `to_device` |
| `topo_order` | `data_flow_order` |
| `required` | `must_visit` |
| `seen` | `visited` |

### 4. Constantes explicites

```python
YOU = 'you'              # Device de départ (part 1)
SERVER_RACK = 'svr'      # Server rack (part 2)
REACTOR_OUTPUT = 'out'   # Sortie principale du réacteur
DAC = 'dac'              # Digital-to-analog converter
FFT = 'fft'              # Fast Fourier transform
```

## Pourquoi NetworkX ?

| Fonctionnalité | Utilisation |
|----------------|-------------|
| `nx.DiGraph()` | Graphe dirigé (flux unidirectionnel) |
| `nx.topological_sort()` | Ordre de propagation DP |
| `nx.all_simple_paths()` | Énumération (Part 1 uniquement) |
| `.successors()` | Outputs d'un device |

**Limitation** : NetworkX n'a pas de fonction pour **compter** les chemins sans les énumérer. Notre DP maison reste nécessaire pour Part 2.

## Qu'est-ce qu'un DAG ?

**DAG** = Directed Acyclic Graph (Graphe Orienté Acyclique)

1. **Directed** (Orienté) : les arêtes ont une direction (A → B ≠ B → A)
2. **Acyclic** (Acyclique) : impossible de revenir au point de départ en suivant les arêtes

```
    DAG                     Pas un DAG (cycle)

    A → B → D               A → B
    ↓   ↓                   ↓   ↓
    C → E                   C ← D
```

### Pourquoi c'est un DAG ici ?

Le problème dit : *"Data only ever flows from a device through its outputs; it can't flow backwards."*

- `svr → fft → ccc → dac → out` ✓
- `out → dac → svr` ✗ (impossible, les données ne remontent pas)

### Avantage : Tri Topologique

On peut ordonner les devices pour que chaque connexion aille "vers l'avant" :

```
svr → aaa → fft → ccc → dac → fff → out
```

Cet ordre permet le **DP en un seul passage** (pas de récursion, pas de backtracking) :

```python
data_flow_order = nx.topological_sort(devices)

for device in data_flow_order:
    for output in devices.successors(device):
        nb_paths[output] += nb_paths[device]  # Propagation
```

### Comparaison

| Type de graphe | Comptage de chemins | Complexité |
|----------------|---------------------|------------|
| Général (avec cycles) | DFS + backtracking | O(n!) exponentiel |
| **DAG** | DP + tri topologique | O(V + E) linéaire |

C'est pourquoi Part 2 (306 trillions de chemins) se calcule **instantanément** : on propage des compteurs au lieu d'énumérer.

## Pourquoi le DP fonctionne (et pas les autres approches)

### Approches écartées

**1. DFS + backtracking** : marche pour Part 1, mais 306 trillions de chemins = impossible.

**2. Découpage en segments** :

```
chemins(svr→out via dac ET fft) = chemins(svr→dac) × chemins(dac→fft) × chemins(fft→out) ?
```

**Non !** Les chemins peuvent partager des nœuds entre segments → surcomptage.

**3. Mémoïsation avec `visited`** :

```python
cache[node][visited_bitmask][required_seen_mask]
```

**Non !** `visited_bitmask` a 2^643 états possibles (643 devices) → mémoire infinie.

### Pourquoi le DP sur DAG fonctionne

L'astuce : dans un DAG, **on n'a pas besoin de tracker les nœuds visités** !

- Pas de cycles → impossible de repasser par un nœud déjà vu
- L'état se réduit à : `(device_actuel, devices_requis_vus)`
- Seulement `643 × 4 = 2572` états au lieu de `643 × 2^643`

```python
# État minimal suffisant
nb_paths[device][visited]  # visited ∈ {∅, {dac}, {fft}, {dac,fft}}
```

## Complexité

| Part | Méthode | Complexité |
|------|---------|------------|
| 1 | Énumération | O(nombre de chemins) = O(574) |
| 2 | DP | O(V × E × 2^k) où k=2 devices requis |

## Résultats

- Part 1 : **574**
- Part 2 : **306 594 217 920 240**
