# Youtube Recommender
> Projeto de Machine Learning para recomendação de vídeos do youtube com o tema de Data Science.

<br>

![RandomForest](https://img.shields.io/badge/-RANDOM_FOREST_CLASSIFIER-blue?style=for-the-badge)
![LGBM](https://img.shields.io/badge/-LIGHT_GBM-red?style=for-the-badge)

![Precision](https://img.shields.io/badge/PRECISION-0.326-green?style=for-the-badge)
![ROC](https://img.shields.io/badge/ROC_AUC-0.73-green?style=for-the-badge)

<br>

<img src="home-youtube-recommender.png" alt="exemplo imagem">


## 💻 Descrição do Projeto

Nesse projeto, o problema de negócio emulado é: <b>atualmente gasto muito tempo procurando novos vídeos do tema de Data Science que realmente tem um 
fit com os vídeos que me interessam</b>. Para resolver esse problema, foi pensado em criar um algoritmo para recomendação de vídeos sobre Data Science onde
neles eu tivesse um <b>Score</b> para servir de métrica avaliadora de quais vídeos eu mais gostaria.

## 💻 Aplicação da Solução

- [x] Extração de dados do Youtube com a lib: [youtube-dl](https://github.com/ytdl-org/youtube-dl)
- [x] Processo de <b>Labeling</b> onde categorizei quais vídeos eu assistiria e quais eu não assistiria
- [x] Criação do Algoritmo Classificador:

    - [x] Criação de um primeiro modelo simples para servir de baseline com as métricas <b>Precisão</b> e <b>ROC AUC</b>
    - [x] Criação de modelos mais elaborados com Active Learning, TFIDF, Random Forest
    - [x] Criação de ensemble com os algoritmos que trouxeram as melhores métricas 
 
 - [x] Deploy local com Docker
 - [x] Deploy com [Heroku](https://www.heroku.com/) para criação do serviço em URL pública

<br>

> 👨‍💻 Projeto disponível [AQUI](https://youtube-recommender-1195.herokuapp.com/)
