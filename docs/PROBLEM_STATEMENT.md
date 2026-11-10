# Énoncé du problème

## Contexte
Atelier fictif de fabrication de produits en tôle : armoires électriques, coffrets industriels et caissons de machines.

## Problème opérationnel
Les commandes doivent être transformées en opérations ordonnées. Chaque opération nécessite un type de machine, un outillage et un opérateur qualifié. Les opérations d’un même ordre respectent une précédence. Les ressources ont des calendriers et des capacités limités. Le changement de famille produit un temps de préparation (setup). Des perturbations peuvent rendre le planning courant invalide ou sous-optimal.

## Objectif du projet
Concevoir un prototype d’aide à la décision qui :
1. génère un planning initial soumis aux contraintes ;
2. minimise une fonction de coût explicitée (retards, makespan et/ou changements de série) ;
3. replanifie après une panne, une absence ou une commande urgente ;
4. explique les décisions à l’utilisateur à partir de données structurées.

## Utilisateurs cibles
Responsable d’atelier et planificateur de production.

## Hors périmètre
Pilotage réel de machines, intégration ERP/MES, données industrielles confidentielles et autonomie opérationnelle sans validation humaine.
