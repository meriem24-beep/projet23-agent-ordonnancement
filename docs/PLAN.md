# Plan de travail et jalons

## Phase 1 — Cadrage et données (en cours)
- [x] Choisir un contexte industriel fictif.
- [x] Générer un jeu de données déterministe.
- [x] Ajouter une commande urgente cohérente avec les tables de données.
- [x] Ajouter un validateur de cohérence structurelle.
- [ ] Auditer les hypothèses et la faisabilité par un modèle de planning.

## Phase 2 — Modélisation et solveur
- [ ] Définir variables, contraintes et fonction objectif.
- [ ] Implémenter un cas réduit (quelques ordres, machines et opérateurs).
- [ ] Tester précédences, non-chevauchement, qualifications et calendriers.
- [ ] Étendre au dataset complet et mesurer les retards / makespan.

## Phase 3 — Replanification
- [ ] Simuler panne machine.
- [ ] Simuler absence opérateur.
- [ ] Injecter commande urgente.
- [ ] Comparer planning initial et planning recalculé.

## Phase 4 — Explicabilité et interface
- [ ] Définir un format de raisons structuré produit par le solveur.
- [ ] Connecter le LLM en lecture seule sur les résultats.
- [ ] Créer une maquette de l'interface.
- [ ] Tester les réponses explicatives contre les faits du planning.

## Phase 5 — Évaluation et livraison
- [ ] Comparer au moins une règle heuristique de référence.
- [ ] Mesurer retards, temps total, utilisation et temps de calcul.
- [ ] Documenter limites, résultats et répartition des tâches.

## Répartition trinôme (à confirmer)
- Membre A : données, validation et préparation des scénarios.
- Membre B : formulation mathématique et solveur.
- Membre C : interface, explications LLM et tests d'intégration.
Les responsabilités sont provisoires et doivent être validées par les trois membres.
