# <br> <img align="center" alt="Hernane-Photoshop" height="130" width="140" src="https://user-images.githubusercontent.com/88516429/185773964-1c4adbaf-8d43-4c48-a3af-cb7451157dfd.png"> Simulador do Algoritmo de Tomasulo 



`ICEI` `Engenharia de Computação` `Arquitetura de Computadores III` `5º PERÍODO`

Este trabalho analisa o paralelismo em nível de instrução por meio
do estudo de pipelines escalares e superescalares. Inicialmente, são investiga-
dos hazards de dados e controle em um pipeline escalar de 5 estágios, avaliando
técnicas como forwarding e predição de desvios. Em seguida, aborda-se a ar-
quitetura superescalar, com foco em despacho múltiplo, execução fora de ordem
e aplicação do Algoritmo de Tomasulo. A renomeação de registradores é uti-
lizada para eliminar falsas dependências e ampliar o paralelismo. Por fim, os
resultados são integrados por meio da análise de métricas como CPI e IPC,
discutindo limites, custos e mecanismos de hardware voltados à melhoria de
desempenho em processadores modernos. O livro base consultado é "Arquitetura de Computadores, uma Abordagem Quantitativa", de Hennessy e Patterson.

<img align="center" alt="RiscV" height="15" width="150" src="https://github.com/gustavovalcastro/algoritmo-tomasulo/assets/88516429/c40ca4b6-a9a3-4467-bb05-8f0628dc2c5f"> 


 
## Integrantes

* [Daniel Lucas Soares Madureira](https://github.com/DanielLucas289)
* [Gabriel Marques da Cunha](https://github.com/GabrielMarquesCunha)
* [Vinicius Cezar Pereira Menezes](https://github.com/viniciusmenezes2003)



## Professor

* [Ricardo Carlini Sperandio](https://www.escavador.com/sobre/5847826/ricardo-carlini-sperandio)

## Instruções de utilização 

### Linguagem e Versão
- Python: 3.10.11

### Sistemas Operacionais testados
- Ubuntu 22.04.1
- Windows 11 v25H2

### Importante

O projeto está no diretório "toma". Para instalar as dependências, execute o comando:
```
pip install tabulate
```
Para uma formatação visual e agradável de dados tabulares em Python, utilizando a biblioteca Tabulate


## Execução do projeto

```
python main.py t1 - Para executar sequência com dependências RAW em cadeia

python main.py t2 - Sequência com WAR e WAW 
```
A interface formatada será carregada na tela do usuário assim que o programa for executado

