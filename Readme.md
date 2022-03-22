# Scrapping project 

Ce projet a été fait dans le cadre d'un rendu de cours. 

Ce script permet de récupérer les données des personage de Jojo's bizarre adventure sur le site : 

- https://jjba.fandom.com/
## Installation

Utiliser le gestionnaire  de package [pip](https://pip.pypa.io/en/stable/) poru installer les dépendances

- bs4.

```bash
pip install bs4
```
- BeautifulSoup
```bash
pip install BeautifulSoup
```
- pandas
```bash
pip install BeautifulSoup
```
- openpyxl pour créer un fichier excel
```bash
pip install openpyxl
```
## Description
Le script va à l'initialisation récolter les endPoints des chaque personnage à partir de la page suivante : 
- https://jjba.fandom.com/fr/wiki/Cat%C3%A9gorie:Personnages

Puis, va aller sur chaque page dédié des personnages pour récupérer la data présent dans le tableau de la sidebar de droite.

Chaque propriété d'un personnage sera stocké dans un objet et chaque objet (représentant un personnage) sera ajouté au tableau global.

Enfin grâce à pandas, un dataFrame sera créé et exporté au format csv

## Usage
Vous pouvez limiter le nombre de personnages à récupérer en remplissant une limite en paramètre de la fonction présent dans l'init du projet. Si la limit n'est pas un int, tout sera récupéré.
```python
get_characters_link(limite)
```

## Contribution
Les Pull requests sont les bienvenues et seront accepté si intéressant pour le projet.
