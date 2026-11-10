# Architecture cible (proposition initiale)

```text
CSV / saisie utilisateur
        |
        v
Validation des données et normalisation
        |
        v
Moteur d'ordonnancement (solveur OR)
        |
        +----> Planning structuré + métriques + raisons de contraintes
                         |
                         v
                Couche d'explication LLM
                         |
                         v
              Interface de consultation
```

## Séparation des responsabilités
- Le solveur est la source de vérité pour les affectations, horaires et contraintes.
- Le LLM reformule les résultats, répond aux questions et explique les causes à partir des sorties du solveur.
- Toute action de modification du planning repasse par le solveur et une validation.

## Choix techniques à décider
Comparer OR-Tools CP-SAT avec une formulation MILP adaptée. Justifier le choix selon les contraintes de ressources, précédence, temps de setup et replanification. Ne pas annoncer un choix définitif avant un petit benchmark.
