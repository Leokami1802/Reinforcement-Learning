# Reinforcement-Learning
## Características do código

- Modo de execução em paralelo do algoritmo de RL disponível.
- Ambientes bidimensionais ([OpenAi Gym](https://github.com/openai/gym)) e tridimensionais ([ViZDoom](https://github.com/mwydmuch/ViZDoom)) para o treinamento e teste de agentes.
- Configuração do treinamento/teste do agente via comandos no terminal ou via arquivos de configuração .cfg.
- Armazenamento de informações do treinamento em arquivos .csv e dos pesos das redes neurais como .h5.
- Facilidade e robustez para definir os hiperparâmetros sem a necessidade de modificar o código.
- Facilidade para a criação de arquiteturas de redes neurais sem a necessidade de modificar o código principal.
- Simulação com frames monocromáticos ou coloridos (RGB)
- Armazenamento dos episódios ao longo do treinamento e dos estados ao longo de um teste como imagens .gif.
- Plot dos mapas de ativação, zonas de máxima ativação na imagem de entrada e imagens de entrada que maximizam determinados filtros para cada uma das camadas de convolução de um modelo treinado.
- Pesos pré-treinados para os jogos Pong e para os dois mapas de ViZDoom que acompanham esse repositório.

## Performance 
Para melhorar o tempo de processamento gasto no treinamento dos agentes foi desenvolvido uma abordagem para o algoritmo de reinforcement learning rodar em paralelo. Essa abordagem consiste basicamente em amostrar as experiências da replay memory em paralelo enquanto o algoritmo de decisão é executado, assim quanto chegamos na parte de treinamento da rede neural o custo computacional da amostragem já foi executado. A seguir temos algumas imagens comparativas entre as performances em frames/segundo do modo serial (single-threading) e paralelo (multi-threading) no treinamento de agente para jogar o jogo de Atari 2600 Pong. 

<p align="center">
 <img src="docs/fps_bar.png">
</p>
*Os testes de performance foram realizado em cpu core i7 4790K e gpu nvidia geforce gtx 970*


Como podemos observar na imagem abaixo, embora a versão em paralelo introduza um "atraso" de uma amostragem, ambos os algoritmos aprenderam com sucesso a jogar o jogo Pong.

<p align="center">
 <img src="docs/pong_desemp_reward.png">
</p>

## Instalação
O código foi todo escrito e testado em python 3.6 com Windows 10. Para execução do código as seguintes bibliotecas se fazem necessárias:

````
Tensorflow (cpu ou gpu)
Keras
Pandas
Imageio
OpenCV
Matplotlib
OpenAI Gym
ViZDoom
````

Para a instalação das bibliotecas acima recomenda-se criar um [ambiente virtual](https://conda.io/docs/user-guide/tasks/manage-environments.html) com o [miniconda](https://conda.io/docs/user-guide/install/index.html). Com o ambiente virtual ativado a instalação das bibliotecas com o miniconda pode ser feita com os seguintes comandos:
Versão cpu do tensorflow
````
conda install tensorflow
````
Versão gpu do tensorflow
````
conda install tensorflow-gpu
````
Para as demais bibliotecas
````
conda install keras
conda install pandas
conda install imageio
conda install opencv
conda install matplotlib
````
Para a instalação da biblioteca open ai gym em conjunto com o ambiente de ATARI 2600 no windows, utiize o seguintes comandos:
````
pip install gym
pip install --no-index -f https://github.com/Kojoley/atari-py/releases atari_py
````
Para mais detalhes sobre a execução dos jogos de atari no windows, consultar esse [link](https://stackoverflow.com/questions/42605769/openai-gym-atari-on-windows).

Para a instalação do ViZDoom no windows consultar esse [link](https://github.com/mwydmuch/ViZDoom/blob/master/doc/Building.md#windows_bin)

Uma vez com todas as bibliotecas instaladas e o ambiente virtual configurado, basta dar download ou clonar esse repositório e executar o arquivo Base_agent.py para o treinamento de um agente com o algoritmo de reinforcement learning DQN ou DRQN.

## Utilização
Para começar o treinamento do agente em seu ambiente de escolha basta executar o arquivo Base_agent.py com as configurações de treinamento desejadas. Essas opções podem ser passadas via comandos de terminal ou escritas no arquivo Base_agent.cfg. **Caso algum comando de terminal seja enviado, a configuração de execução do script será feita exclusivamente por eles, e os parâmetros não enviados terão seus valores atribuídos como default.** Se nenhum parâmetro for enviado via terminal, o script procurará por um arquivo de mesmo nome com extensão .cfg. Dentro deste arquivo caso encontre configurações validas às mesmas serão lidas e de forma similar a configuração via terminal, os valores não definidos serão atribuídos aos seus valores default. Se nenhuma das opções de configuração acima seja feita, o agente será treinado com seus valores default, ou seja, serão utilizados os hiperparâmetros demonstrados no artigo [Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236) para o treinamento de um agente no jogo Pong.

A grande vantagem de se utilizar o arquivo .cfg é o fato de não precisar copiar e colar (ou escrever) comandos gigantes no terminal, além de facilitar o debug em caso de algum contratempo na inicialização de algum hiperparâmetro. Mais detalhes sobre a configuração dos arquivos .cfg pode ser vista no tópico [Arquivos CFG](#).

Antes do começo do treinamento do agente, o script exibe um resumo das configurações e hiperparâmetros que serão utilizados em sua execução, desta forma, é possível checar se esta tudo de acordo com o planejado.

<p align="center">
 <img src="docs/summary.png">
</p>



## Definindo a arquitetura da rede neural
É possível definir sua propria arquitetura de rede neural para o treinamento do seu agente. Para isso basta criar dentro do arquivo Networks.py sua própria rede neural como uma função utilizando a biblioteca [Keras](https://keras.io/) **(A arquitetura pode ser criada com a functional ou sequential API)**. Dessa forma, você pode experimentar de forma rápida e sem complicações os efeitos de diferentes arquiteturas, como por exemplo, camadas recorrentes, métodos de regularização (Dropout, distância L2), normalização, batch normalization no aprendizado do agente. Após definida sua arquitetura, o nome da função deve ser enviado como um argumento via comando de terminal com o comando:

````
python Base_agent.py --network_model "<nome_da_sua_funcao>"
````
Ou escrito no arquivo Base_agent.cfg como:
````
network_model = <nome_da_sua_funcao>
````
Caso a arquitetura possua camadas do tipo recorrente é necessario atribuir o valor verdadeiro a variável **is_recurrent** na hora da execução do script principal. Desta forma caso sua arquitetura seja recorrente o comando será:

````
python Base_agent.py --network_model "<nome_da_sua_funcao_recorrente> --is_recurrent True"
````
Ou escrito no arquivo Base_agent.cfg como:
````
network_model = <nome_da_sua_funcao_recorrente>
is_recurrent = True
````

### Requisitos
A rede neural desensolvida deve ter como entrada um tensor de dimensão **state_input_shape** e um nome igual a **name**, além da possibilidade da escolha se os pixel das entrada serão normalizados ou não pela variável **normalize** e deve possuir como saída um tensor com formato igual **actions_num**. A função deve ter como retorno o modelo Keras implementado pela função. Os parâmetros **state_input_shape**, **name**, **actions_num** e **normalize** são enviados ao arquivo Networks.py pelo script principal, que por sua vez, espera como retorno o modelo implementado. A seguir temos um exemplo de implementação da arquitetura (com a functional API do Keras) utilizada no artigo [Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236) dentro de uma função chamada **DQN**:

````
def DQN(state_input_shape, actions_num, name, normalize):
    input = Input(state_input_shape, name=name)
    if normalize:
        lamb = Lambda(lambda x: (2 * x - 255) / 255.0, )(input)
        conv_1 = Conv2D(32, (8, 8), strides=(4, 4), activation='relu')(lamb)
    else:
        conv_1 = Conv2D(32, (8, 8), strides=(4, 4), activation='relu')(input)
    conv_2 = Conv2D(64, (4, 4), strides=(2, 2), activation='relu')(conv_1)
    conv_3 = Conv2D(64, (3, 3), strides=(1, 1), activation='relu')(conv_2)
    conv_flattened = Flatten()(conv_3)
    hidden = Dense(512, activation='relu')(conv_flattened)
    output = Dense(actions_num)(hidden)
    model = Model(inputs=input, outputs=output)
    return model
````
Essa é a arquitetura padrão executada, caso nenhuma outra seja especificada na execução do agente. Dentro do arquivo [Networks.py](Networks.py) há outras arquiteturas de redes neurais (com camadadas recorrentes, métodos de normalização) que servem como exemplo.

## Arquivos de configuração .CFG
Os arquivos de extensão .cfg são arquivos que possuem configurações para a execução do algoritmo de reinforcement learning. Esses arquivos são uma alternativa que facilita a execução e o debug dos treinamentos/testes dos agentes nos ambientes escolhidos. Ao invés de digitar toda vez longos códigos no terminal para a execução do script, escrevemos essa configuração em arquivo .cfg de mesmo nome do script a ser executado, como por exemplo, Base_agent.cfg ou Plot_rl.cfg para os scripts Base_agent.py e Plot_rl.py respectivamente. De baixo dos panos, o que script faz é ler o arquivo .cfg e transformar as linhas válidas de código dentro do mesmo em comando de terminais e envia ao arquivo Argparser antes de inicializar qualquer coisa, assim, uma linha de código env = Doom se transforma em --env Doom e é enviada o método main do arquivo executado.
Um cuidado necessário na execução de nosso script configurado um arquivo .cfg é que :**Caso algum comando de terminal seja enviado, a configuração de execução do script será feita exclusivamente por eles, e os parâmetros não enviados terão seus valores atribuídos como default.** Se nenhum parâmetro for enviado via terminal, o script procurará por um arquivo de mesmo nome com extensão .cfg. Dentro deste arquivo caso encontre configurações validas às mesmas serão lidas e de forma similar a configuração via terminal, os valores não definidos serão atribuídos aos seus valores default.

### Escrevendo os arquivos .cfg
As regras de escrita dos arquivos .cfg são as seguintes:
- Linhas começando com os caracteres **#** ou **;** são tratadas como comentários.
- Linhas começando com o caractere **+** são continuações de linhas anteriores. Por exemplo, para um path do sistema que é muito longo.
- As linhas não são Case sensitive, ou seja, não há distinção entre minúscula ou maiúscula (ENV = DOOM é igual a env = Doom).
- Cada linha **deve possuir apenas um par de chave = valor**. Por exemplo, agent_mode = train em uma linha, e na próxima env = doom e assim por diante.
- Se um argumento não estiver especificado no arquivo .cfg e seja necessário para execução da tarefa desejada, seu valor padrão será carregado. Isto foi feito, para evitar a fatiga de toda vez ter escrever parâmetros que tem seus valores frequentes entre simulações. Para ver quais são os valores padrões de cada variável verificar o [DOC] e para exemplos e cuidados sobre esses valores verificar a sessão de [Exemplos](#Exemplo).
- Caminhos relativos ao diretório principal, podem ser inseridos utilizando os dois pontos (..) antes do path. Por exemplo: para acessar o diretório Weights, ao invés de especificarmos todo o path do sistema, podemos inserir apenas: ../Weights
- Os comandos serão lidos em sequência, logo, em caso de comandos repetidos apenas o último sera válido.

## Exemplos
A seguir serão apresentados alguns exemplos. Todos os parâmetros podem ser passados via comandos de terminal na execução do script ou via arquivo .cfg (como visto na sessão [Utilização](https://github.com/Leonardo-Viana/Reinforcement-Learning#utiliza%C3%A7%C3%A3o)). Relembrando que os parâmetros não configurados possuem seus valores iguais ao default. Para mais informações sobre cada opção disponivel e seus valores default verificar o [DOC](www.somelink.com) ou utilizar o comando de terminal:
````
python Base_agent.py --help
````
### Pong treinado com DQN básico
Como primeiro exemplo treinaremos um agente utilizando os hiperparâmetros especificados pelo excelente artigo [Speeding up DQN on PyTorch: how to solve Pong in 30 minutes](https://medium.com/mlreview/speeding-up-dqn-on-pytorch-solving-pong-in-30-minutes-81a1bd2dff55). O arquivo Base_agent.cfg deverá possuir :

```
agent_name = DQNPong30
num_simul_frames = 1000000
e_min = 0.02
e_lin_decay = 100000
target_update = 1000
num_states_stored = 100000
num_random_play = 10000
optimizer = adam
lr = 1e-4
random_seed = 1
```
E depois basta executar o script Base_agent.py sem nenhum argumento:
````
python Base_agent.py
````
Outra opção seria executar os comandos no terminal em conjunto com a execução do script:
````
python Base_agent.py --agent_name "DQNPong30" --num_simul_frames 1000000 --e_min 0.02 --e_lin_decay 100000 --target_update 1000 --num_states_stored 100000 --num_random_play 10000 --optimizer adam --lr 1e-4 --random_seed 1
````
Ambas as opções de configuração irão treinar o agente com hiperparâmetros especificados pelo artigo acima com a random seed fixa (em 1) durante 1 milhão de frames. 

### Treinamento de um agente dentro do VizDoom 
Esse repositório possui em suas dependencias dois mapas para o jogo Doom, **labyrinth e labyrinth_test**, que possuem como objetivo ensinar o agente a navegação tridimensional (mais detalhes sobre esses mapas no tópico [Mapas de Doom]). Para treinar o agente na fase labyrinth utilizando a arquitetura de rede neural DRQN proposta por [POR LINK do ARTIGO DRQN] podemos utilizar os seguintes comandos:
````
python Base_agent.py --env Doom --agent_name grayh4-LSTM --network_model DRQN --is_recurrent True --optimizer adam --lr 1e-4 --num_random_play 50000 --num_states_stored 250000 --e_lin_decay 250000 --num_simul_frames 5000000 --steps_save_weights 50000 --history_size 4 --input_shape (84,84,1) --to_save_episodes True steps_save_episodes 100 --multi_threading True
````
Ou podemos escrever dentro do arquivo Base_agent.cfg os seguintes comandos:
````
env = Doom
agent_name = grayh4-LSTM
network_model = DRQN
is_recurrent = True
optimizer = adam
lr = 1e-4
num_random_play = 50000
num_states_stored = 250000
e_lin_decay = 250000
num_simul_frames = 5000000
steps_save_weights = 50000
history_size = 4
input_shape = (84,84,1)
to_save_episodes = True
steps_save_episodes = 100
multi_threading = True
````
E depois basta executar o script Base_agent.py sem nenhum argumento:
````
python Base_agent.py
````
### Testando um agente treinado
O script Base_agent.py possui dois modos de execução treinamento (**train**) ou teste (**test**). O modo de treinamento é o default no qual o agente é treinado utilizando a premissa do reinforcement learning. Já no modo teste, a maioria dos hiperparâmetros de aprendizado são ignorados, o objetivo deste modo é o teste de um agente treinado. A seguir vemos um exemplo do teste de um agente treinado com o DQN (os pesos treinados desta simulação encontram-se neste repositório) com o jogo serendo renderizado:
````
python Base_agent.py --agent_mode test --env Doom --load_weights True --weights_load_path ../Weights/Pretrained/Doom/Labyrinth/grayh4-weights-Doom-labyrinth-5000000.h5 --agent_name doomh4 --to_render True --to_save_states False
````
````
agent_mode = test
env = Doom
load_weights = True
weights_load_path = ../Weights/Pretrained/Doom/Labyrinth/grayh4-weights-Doom-labyrinth-5000000.h5
agent_name = doomh4
to_render = True
to_save_states = False
````
# Documentação
## Configurações gerais/iniciais
* [agent_mode](#agent_mode)
* [agent_name](#agent_name)
* [env](#env)
## Atari GYM exclusivo
* [include_score](#include_score)
## DOOM exclusivo
* [config_file_path](#config_file_path)
## Redes Neurais
* [network_model](#network_model)
* [normalize_input](#normalize_input)
* [is_recurrent](#is_recurrent)
## Aprendizado
* [frame_skip](#frame_skip)
* [num_simul_frames](#num_simul_frames)
* [discount_rate](#discount_rate)
* [lr](#lr)
* [epsilon](#epsilon)
* [e_min](#e_min)
* [decay_mode](#decay_mode)
* [e_lin_decay](#e_lin_decay)
* [e_exp_decay](#e_exp_decay)
* [target_update](#target_update)
* [num_states_stored](#num_states_stored)
* [batch_size](#batch_size)
* [input_shape](#input_shape)
* [history_size](#history_size)
* [num_random_play](#num_random_play)
* [loss_type](#loss_type)
* [optimizer](#optimizer)
## Configurações gerais
* [load_weights](#load_weights)
* [weights_load_path](#weights_load_path)
* [steps_save_weights](#steps_save_weights)
* [path_save_weights](#path_save_weights)
* [steps_save_plot](#steps_save_plot)
* [path_save_plot](#path_save_plot)
* [to_save_episodes](#to_save_episodes)
* [steps_save_episodes](#steps_save_episodes)
* [to_save_episodes](#to_save_episodes)
* [path_save_episodes](#path_save_episodes)
* [silent_mode](#silent_mode)
* [multi_gpu](#multi_gpu)
* [gpu_device](#gpu_device)
* [multi_threading](#multi_threading)
* [to_render](#to_render)
* [random_seed](#random_seed)
## Exclusivo do modo de teste
* [to_save_states](#to_save_states)
* [path_save_states](#path_save_states)


---
### <a name="agent_mode"></a> `agent_mode`

| Comando de Terminal | `--agent_mode <value>`    |
| :--                 | :--                       |
| **Arquivo .cfg**    | **`agent_mode = <value>`**|
| Tipo                | string                    |
| Escolhas possíveis  | train, test               |
| **Valor default**   | **train**                 |


Variável que escolhe o modo de execução do algoritmo de reinforcement learning. Existem duas opções disponíveis: train e test. 

A opção de **train** treina um agente com base no algoritmo de reinforcement learning DQN ou em suas variantes, ou seja, o agente irá aprender a otimizar os pesos de sua rede neural com base em suas experiências vividas dentro do ambiente para maximizar sua premiação final. Logo, neste modo o algoritmo armazena as experiências passadas, otimiza a rede neural com os hiperparâmetros de aprendizagem.

A opção de **test** é usada para testar um agente que já aprendeu dentro de um ambiente. Essa opção é basicamente para o programador avaliar o desempenho do agente, gravar episódios, armazenar estados para plot.

---

### <a name="agent_name"></a> `agent_name`

| Comando de Terminal | `--agent_name <value>`    |
| :--                 | :--                       |
| **Arquivo .cfg**    | **`agent_name = <value>`**|
| Tipo                | string                    |
| **Valor default**   | **DQN**                   |


Nome do agente, além de identificação do agente será utilizado para nomear os arquivos que serão salvos (Weights, Plot, Episódios, Estados).

---

### <a name="env"></a> `env`

| Comando de Terminal | `--env <value>`           |
| :--                 | :--                       |
| **Arquivo .cfg**    | **`env = <value>`**       |
| Tipo                | string                    |
| **Valor default**   | **PongNoFrameSkip-v4**    |


Nome do ambiente (environment) a ser executado. Atualmente são suportados todos os jogos de atari disponíveis pela biblioteca OpenAi gym e o ambiente tridimensional Doom.

O nome dos jogos de atari, deverão seguir o seguinte template \<nome do jogo de atari\>NoFrameSkip-v4. É possível ver todos os jogos de atari disponíveis no seguinte [link](https://gym.openai.com/envs/#atari). Assim, para treinar o agente no ambiente breakout, devemos passar para a variável env o valor BreakoutNoFrameSkip-v4 (env = BreakoutNoFrameSkip-v4 ou --env BreakoutNoFrameSkip-v4). Com a parte do "NoFrameSkip" dizemos a biblioteca que não queremos a que a mesma realize o frame skipping, desta forma temos mais controle para realizar esta etapa em nosso código (dentro do arquivo (WrapperGym.py)[Environments/WrapperGym.py]).
 
Para executar o ambiente VizDoom, basta enviar para a variável env o valor doom (env = Doom ou --env Doom). 

---

### <a name="include_score"></a> `include_score`

| Comando de Terminal  | `--include_score <value>`    |
| :--                  | :--                          |
| **Arquivo .cfg**     | **`include_score = <value>`**|
| Tipo                 | bool                         |
| **Valor default**    | **False**                    |
| Exclusivo do ambiente| ATARI GYM                    |


Variável **exclusiva dos jogos de atari da biblioteca GYM** que controla se o score dos jogos de atari será incluído ou não nos frames/estados enviados pela biblioteca open ai gym. Por exemplo no jogo Pong, o score (pontuação) é localizado na parte superior da tela do jogo de atari.

---

### <a name="config_file_path"></a> `config_file_path`

| Comando de Terminal  | `--config_file_path <value>`       |
| :--                  | :--                                |
| **Arquivo .cfg**     | **`config_file_path = <value>`**   |
| Tipo                 | string (path do sistema)           |
| **Valor default**    | **../DoomScenarios/labyrinth.cfg** |
| Exclusivo do ambiente| ViZDOOM                            |


Caminho do sistema operacional (path) para o arquivo que carrega a fase de escolha do VizDoom. A configuração da fase do VizDoom no qual o agente será treinado é feita por um arquivo .cfg, cada fase do VizDoom deverá possuir um arquivo .cfg correspondente. Portanto, para treinarmos os agente em uma fase específica do VizDoom devemos carregar seu arquivo .cfg enviando para essa variável o seu caminho dentro do sistema operacional.

Para mais detalhes sobre os arquivos .cfg usados pela VizDoom, consulte esse [link](https://github.com/mwydmuch/ViZDoom/blob/master/doc/ConfigFile.md)

---

### <a name="network_model"></a> `network_model`

| Comando de Terminal  | `--network_model <value>`          |
| :--                  | :--                                |
| **Arquivo .cfg**     | **`network_model = <value>`**      |
| Tipo                 | string                             |
| **Valor default**    | **DQN**                            |

Nome da função que define a arquitetura da rede neural dentro do arquivo [Networks.py](Networks.py). Para mais detalhes sobre a implementação de sua própria arquitetura de rede neural consultar o tópico: [Definindo a arquitetura da rede neural](https://github.com/Leonardo-Viana/Reinforcement-Learning#definindo-a-arquitetura-da-rede-neural)

---

### <a name="normalize_input"></a> `normalize_input`

| Comando de Terminal  | `--normalize_input <value>`        |
| :--                  | :--                                |
| **Arquivo .cfg**     | **`normalize_input = <value>`**    |
| Tipo                 | bool                               |
| **Valor default**    | **True**                           |

Variável que controle se é para normalizar ou não pixels de entrada da rede neural.

---

### <a name="is_recurrent"></a> `is_recurrent`

| Comando de Terminal  | `--is_recurrent <value>`        |
| :--                  | :--                             |
| **Arquivo .cfg**     | **`is_recurrent = <value>`**    |
| Tipo                 | bool                            |
| **Valor default**    | **False**                       |

Variável que diz ao script principal se a arquitetura de rede neural possui ou não camadas do tipo recorrente. Logo, se o seu modelo possuir camadas deste tipo, essa variável tem que ser enviada com o valor **True** em conjunto com a variável **network_model**, se não o script jogará uma exceção. Caso seu modelo não possua camadas do tipo recorrente, essa variável não precisa ser mandada, já que seu valor padrão é False.

---

### <a name="frame_skip"></a> `frame_skip`

| Comando de Terminal  | `--frame_skip <value>`        |
| :--                  | :--                           |
| **Arquivo .cfg**     | **`frame_skip = <value>`**    |
| Tipo                 | int                           |
| **Valor default**    | **4**                         |

Um frame válido será considerado apenas a cada \<frame_skip\> frames. Por exemplo, com um frame_skip igual a 4, somente o último frame de uma sequência de 4 frames renderizados será enviado ao nosso código para a criação do nosso estado. Os outros 3 frames são "descartados". Uma excelente discussão esclarecendo as ambiguidades do artigo do DQN em relação as variáveis frame_skip e history_size pode ser vista [aqui](https://danieltakeshi.github.io/2016/11/25/frame-skipping-and-preprocessing-for-deep-q-networks-on-atari-2600-games/). O termo frame em outros tópicos se refere exclusivamente ao frames válidos que são considerados pelo script.

---

### <a name="num_simul_frames"></a> `num_simul_frames`

| Comando de Terminal  | `--num_simul_frames <value>`        |
| :--                  | :--                                 |
| **Arquivo .cfg**     | **`num_simul_frames = <value>`**    |
| Tipo                 | int                                 |
| **Valor default**    | **10000000**                        |

Número de frames no qual o agente será treinado. 

---

### <a name="discount_rate"></a> `discount_rate`

| Comando de Terminal  | `--discount_rate <value>`           |
| :--                  | :--                                 |
| **Arquivo .cfg**     | **`discount_rate = <value>`**       |
| Tipo                 | float                               |
| **Valor default**    | **0.99**                            |

Fator de desconto (discount rate) gamma. 

---

### <a name="lr"></a> `lr`

| Comando de Terminal  | `--lr <value>`           |
| :--                  | :--                      |
| **Arquivo .cfg**     | **`lr = <value>`**       |
| Tipo                 | float                    |
| **Valor default**    | **0.00025**              |

Taxa de aprendizado das redes neurais. 

---

### <a name="epsilon"></a> `epsilon`

| Comando de Terminal  | `--epsilon <value>`      |
| :--                  | :--                      |
| **Arquivo .cfg**     | **`epsilon = <value>`**  |
| Tipo                 | float                    |
| **Valor default**    | **1.0**                  |

**Valor inicial** da variável épsilon da política de aprendizado e-greedy (epsilon-greedy). Essa variável balanceia o quanto de exploração de novos conhecimentos vs exploração de conhecimentos prévios o agente deve realizar. Essa variável decai ao longo da simulação. 

---

### <a name="e_min"></a> `e_min`

| Comando de Terminal  | `--e_min <value>`        |
| :--                  | :--                      |
| **Arquivo .cfg**     | **`e_min = <value>`**    |
| Tipo                 | float                    |
| **Valor default**    | **0.1**                  |

**Valor final** da variável épsilon da política de aprendizado e-greedy (épsilon-greedy) após o decaimento.

---

### <a name="decay_mode"></a> `decay_mode`

| Comando de Terminal | `--decay_mode <value>`    |
| :--                 | :--                       |
| **Arquivo .cfg**    | **`decay_mode = <value>`**|
| Tipo                | string                    |
| Escolhas possíveis  | linear, exponential       |
| **Valor default**   | **linear**                |

Variável que escolhe o tipo de decaimento da variável épsilon. Existem dois modos possíveis de decaimento da variável épsilon nesse repositório, o modo linear e exponencial.

---

### <a name="e_lin_decay"></a> `e_lin_decay`

| Comando de Terminal  | `--e_lin_decay <value>`        |
| :--                  | :--                            |
| **Arquivo .cfg**     | **`e_lin_decay = <value>`**    |
| Tipo                 | int                            |
| **Valor default**    | **1000000**                    |

Número de frames no qual o **decaimento linear** de épsilon chegará ao seu valor final. Usando os valores padrão, a variável épsilon decairá linearmente de 1.0 (100% de jogadas aleatórias) para 0.1 (10% de jogadas aleatórias) em 1 milhão de frames.

---
### <a name="e_exp_decay"></a> `e_exp_decay`

| Comando de Terminal  | `--e_exp_decay <value>`        |
| :--                  | :--                            |
| **Arquivo .cfg**     | **`e_exp_decay = <value>`**    |
| Tipo                 | int                            |
| **Valor default**    | **200000**                     |

Constante de tempo do **decaimento exponencial** de épsilon, em outras palavras, em uma constante de tempo o valor de épsilon terá decaído em 63.2% do seu valor inicial. O decaimento exponencial se dará da seguinte forma:

|Número de constantes de tempo|Decaimento do valor total|
|---                          |---                      |
|1                            |63.2%                    |
|2                            |86.5%                    |
|3                            |95%                      |
|4                            |98.2%                    |
|5                            |99.3%                    |

Assim, em aproximadamente 5 constantes de tempo o valor de épsilon chega ao seu valor mínimo.

---

### <a name="target_update"></a> `target_update`

| Comando de Terminal  | `--target_update <value>`      |
| :--                  | :--                            |
| **Arquivo .cfg**     | **`target_update = <value>`**  |
| Tipo                 | int                            |
| **Valor default**    | **10000**                      |

Número de frames no qual os parâmetros da Q-target network serão atualizados com os valores da Q-network.

---

### <a name="num_states_stored"></a> `num_states_stored`

| Comando de Terminal  | `--num_states_stored <value>`      |
| :--                  | :--                                |
| **Arquivo .cfg**     | **`num_states_stored = <value>`**  |
| Tipo                 | int                                |
| **Valor default**    | **1000000**                        |

Número de experiências (estados) que serão armazenadas na replay memory.

---

### <a name="batch_size"></a> `batch_size`

| Comando de Terminal  | `--batch_size <value>`      |
| :--                  | :--                         |
| **Arquivo .cfg**     | **`batch_size = <value>`**  |
| Tipo                 | int                         |
| **Valor default**    | **32**                      |

Tamanho do batch que será utilizado para treinar as redes neurais. Em outras palavras, o número de experiências (estados) que serão amostrados da replay memory e usados para treinar a rede neural.

---

### <a name="input_shape"></a> `input_shape`

| Comando de Terminal  | `--input_shape <value>`      |
| :--                  | :--                          |
| **Arquivo .cfg**     | **`input_shape = <value>`**  |
| Tipo                 | string                       |
| **Valor default**    | **"84,84"**                  |

Dimensões nas quais os frames provindos das bibliotecas GYM/ViZDoom serão redimensionados e então amontoados para formarem as experiências/estados que serão utilizados pelo algoritmo de reinforcement learning. As dimensões devem ser colocadas entre aspas e com cada dimensão separada por virgula ou espaço seguindo o template: **"Largura, Altura, Número de canal de cores"**. Caso apenas Largura e Altura sejam enviados é assumido que a imagem será em escala de cinza (número de canal de cores = 1). Por exemplo, caso desejemos treinar nosso algoritmo com estados coloridos de tamanho 64 x 64 devemos enviar a essa variável o seguinte valor: "64,64,3".  

---

### <a name="history_size"></a> `history_size`

| Comando de Terminal  | `--history_size <value>`      |
| :--                  | :--                           |
| **Arquivo .cfg**     | **`history_size = <value>`**  |
| Tipo                 | int                           |
| **Valor default**    | **4**                         |

Número de frames em sequência que serão amontoados para formarem uma experiência/estado, desta forma, o agente possuirá uma "memória", e conseguirá por exemplo saber a direção, velocidade e aceleração de objetos no ambiente. No caso da arquitetura DQN, os estados serão um volume único com formato de "Largura, Altura, Número de canal de cores * History Size". Já na arquitetura DRQN, os estados serão uma sequência de 4 volumes com formato "Largura, Altura, Número de canal de cores". Por exemplo, considere um batch de 32 amostras amostrados da replay memory, no qual cada estado é formado de frames em escala de cinza com tamanho de 84x84 pixels. A tabela a seguir mostra o formato dos tensores que serão enviados às devidas redes neurais.

|Arquitetura| Formado do Estado   |
| ---       | ---                 |
| DQN       | 32, 84, 84, 4       |
| DRQN      | 32, 4, 84, 84, 1    |

---

### <a name="num_random_play"></a> `num_random_play`

| Comando de Terminal  | `--num_random_play <value>`      |
| :--                  | :--                              |
| **Arquivo .cfg**     | **`num_random_play = <value>`**  |
| Tipo                 | int                              |
| **Valor default**    | **50000**                        |

Número de estados gerados por jogadas aleatórias feitas pelo agente antes de começar o treinamento das redes neurais com o propósito de preencher a replay memory.

---
### <a name="loss_type"></a> `loss_type`

| Comando de Terminal | `--loss_type <value>`     |
| :--                 | :--                       |
| **Arquivo .cfg**    | **`loss_type = <value>`** |
| Tipo                | string                    |
| Escolhas possíveis  | huber, MSE                |
| **Valor default**   | **huber**                 |

Tipo de loss function que será utilizada para treinar as redes neurais do agente.

---
### <a name="optimizer"></a> `optimizer`

| Comando de Terminal | `--optimizer <value>`     |
| :--                 | :--                       |
| **Arquivo .cfg**    | **`optimizer = <value>`** |
| Tipo                | string                    |
| Escolhas possíveis  | rmsprop, adam             |
| **Valor default**   | **rmsprop**               |

Tipo de optimizer que será utilizado para treinar as redes neurais do agente.

---
### <a name="load_weights"></a> `load_weights`

| Comando de Terminal  | `--load_weights <value>`        |
| :--                  | :--                             |
| **Arquivo .cfg**     | **`load_weights = <value>`**    |
| Tipo                 | bool                            |
| **Valor default**    | **False**                       |

Variável que diz ao script principal se é para carregar ou não os pesos de um rede neural de um arquivo externo .h5.

---

### <a name="weights_load_path"></a> `weights_load_path`

| Comando de Terminal  | `--weights_load_path <value>`      |
| :--                  | :--                                |
| **Arquivo .cfg**     | **`weights_load_path = <value>`**  |
| Tipo                 | string (path do sistema)           |
| **Valor default**    | **""**                             |


Caminho do sistema operacional (path) para o arquivo .h5 que contêm os parâmetros das redes neurais a serem carregados. O valor padrão é uma string vazia. **Um parâmetro obrigatório para o TEST MODE**

---

### <a name="steps_save_weights"></a> `steps_save_weights`

| Comando de Terminal  | `--steps_save_weights <value>`      |
| :--                  | :--                                 |
| **Arquivo .cfg**     | **`steps_save_weights = <value>`**  |
| Tipo                 | int                                 |
| **Valor default**    | **50000**                           |

A cada \<steps_save_weights\> frames os pesos das redes neurais serão salvos no disco em um arquivo .h5.

---
### <a name="path_save_weights"></a> `path_save_weights`

| Comando de Terminal  | `--path_save_weights <value>`      |
| :--                  | :--                                |
| **Arquivo .cfg**     | **`path_save_weights = <value>`**  |
| Tipo                 | string (path do sistema)           |
| **Valor default**    | **..\Weights**                     |


Caminho do sistema operacional (path) para a pasta no qual serão salvos os pesos das redes neurais em arquivos de extensão .h5.

---
### <a name="steps_save_plot"></a> `steps_save_plot`

| Comando de Terminal  | `--steps_save_plot <value>`      |
| :--                  | :--                                 |
| **Arquivo .cfg**     | **`steps_save_plot = <value>`**  |
| Tipo                 | int                                 |
| **Valor default**    | **10000**                           |

A cada \<steps_save_plot\> frames as variáveis para plot armazenadas por episódio serão salvas no disco em arquivo .csv. As variáveis por episódio salvas são:
|Variáveis          |
| ---               |
| Rewards           |
| Loss              |
| Q-value médio     |
| Número de frames  |
| Tempo             |
| Frames por segundo|
| Epsilon           |

---

### <a name="path_save_plot"></a> `path_save_plot`

| Comando de Terminal  | `--path_save_plot <value>`         |
| :--                  | :--                                |
| **Arquivo .cfg**     | **`path_save_plot = <value>`**     |
| Tipo                 | string (path do sistema)           |
| **Valor default**    | **..\Plot**                        |


Caminho do sistema operacional (path) para a pasta no qual serão salvos as variáveis a serem plotadas em arquivo .csv.

---

### <a name="to_save_episodes"></a> `to_save_episodes`

| Comando de Terminal  | `--to_save_episodes <value>`        |
| :--                  | :--                                 |
| **Arquivo .cfg**     | **`to_save_episodes = <value>`**    |
| Tipo                 | bool                                |
| **Valor default**    | **False**                           |

Variável que controla se é para salvar ou não os episódios no disco como um arquivo .gif.

---
### <a name="steps_save_episodes"></a> `steps_save_episodes`

| Comando de Terminal  | `--steps_save_episodes <value>`      |
| :--                  | :--                                  |
| **Arquivo .cfg**     | **`steps_save_episodes = <value>`**  |
| Tipo                 | int                                  |
| **Valor default**    | **50**                               |

Caso o arquivo tenha que salvar os episódios ([to_save_episodes](#to_save_episodes)), eles serão salvos a cada \<steps_save_episodes\> episódios como um arquivo de imagem animada .gif.

---
### <a name="to_save_episodes"></a> `to_save_episodes`

| Comando de Terminal  | `--to_save_episodes <value>`        |
| :--                  | :--                                 |
| **Arquivo .cfg**     | **`to_save_episodes = <value>`**    |
| Tipo                 | bool                                |
| **Valor default**    | **False**                           |

Variável que controla se é para salvar ou não os episódios no disco como um arquivo .gif.

---
### <a name="path_save_episodes"></a> `path_save_episodes`

| Comando de Terminal  | `--path_save_episodes <value>`      |
| :--                  | :--                                |
| **Arquivo .cfg**     | **`path_save_episodes = <value>`**  |
| Tipo                 | string (path do sistema)           |
| **Valor default**    | **..\Episodes**                    |


Caminho do sistema operacional (path) para a pasta no qual serão salvos os episódios como uma imagem animada em formato .gif.

---
### <a name="silent_mode"></a> `silent_mode`

| Comando de Terminal  | `--silent_mode <value>`             |
| :--                  | :--                                 |
| **Arquivo .cfg**     | **`silent_mode = <value>`**         |
| Tipo                 | bool                                |
| **Valor default**    | **False**                           |

Caso essa variável seja verdadeira, nenhuma mensagem será exibida ao usuário.

---
### <a name="multi_gpu"></a> `multi_gpu`

| Comando de Terminal  | `--multi_gpu <value>`               |
| :--                  | :--                                 |
| **Arquivo .cfg**     | **`multi_gpu = <value>`**           |
| Tipo                 | bool                                |
| **Valor default**    | **False**                           |

Caso o usuário possua mais de uma gpu disponível e deseje usá-las para o treinamento do agente. (O gerenciamento das gpus em paralelo é feito pela biblioteca Keras)

---
### <a name="gpu_device"></a> `gpu_device`

| Comando de Terminal  | `--gpu_device <value>`               |
| :--                  | :--                                  |
| **Arquivo .cfg**     | **`gpu_device = <value>`**           |
| Tipo                 | int                                  |
| **Valor default**    | **0**                                |

Variável que permite a escolha de qual gpu a ser utilizada para o treinamento das redes neurais dos agentes. Assim, caso o usuário possua mais que uma gpu e não deseje utilizar todas elas em apenas um treinamento é possível escolher com essa variável qual gpu utilizar para o treinamento, bastando atribuir o ID da gpu a essa variável e o valor False para a variável [multi_gpu](#multi_gpu). Desta forma é possível, caso haja recursos computacionais suficientes (memória, processamento) simular vários agentes simultaneamente. **Enviar o gpu_device igual -1 e a variável [multi_gpu](#multi_gpu) False fará o treinamento da rede neural rodar no processador.**

---
### <a name="multi_threading"></a> `multi_threading`

| Comando de Terminal  | `--multi_threading <value>`         |
| :--                  | :--                                 |
| **Arquivo .cfg**     | **`multi_threading = <value>`**     |
| Tipo                 | bool                                |
| **Valor default**    | **False**                           |

Se essa variável for ativada, a parte da amostragem de experiências para o treinamento da rede neural é feita paralelamente com o restante do algoritmo de aprendizagem desta forma reduzindo o tempo necessário de processamento de cada episódio. Para mais detalhes consultar o tópico [Performance](https://github.com/Leonardo-Viana/Reinforcement-Learning#performance).

---
### <a name="to_render"></a> `to_render`

| Comando de Terminal  | `--to_render <value>`               |
| :--                  | :--                                 |
| **Arquivo .cfg**     | **`to_render = <value>`**           |
| Tipo                 | bool                                |
| **Valor default**    | **False**                           |

Variável que controle se o ambiente será renderizado (mostrado na tela) para o usuário ou não, durante o treinamento ou teste. Ao renderizar o ambiente, o treinamento sofrerá uma queda enorme de processamento por episódio.

### <a name="random_seed"></a> `random_seed`

| Comando de Terminal  | `--random_seed <value>`               |
| :--                  | :--                                  |
| **Arquivo .cfg**     | **`random_seed = <value>`**           |
| Tipo                 | int                                  |
| **Valor default**    | **-1**                                |

Variável que fixa a semente dos métodos (pseudo)estocásticos. Se o valor dessa variável é -1, nenhuma semente é fixada.

---
### <a name="to_save_states"></a> `to_save_states`

| Comando de Terminal  | `--to_save_states <value>`          |
| :--                  | :--                                 |
| **Arquivo .cfg**     | **`to_save_states = <value>`**      |
| Tipo                 | bool                                |
| **Valor default**    | **False**                           |
| Exclusivo do modo    | Test                               |

Variável que controla se é para salvar ou não os estados/experiências no disco como um arquivo .gif durante o modo TEST. Os estados salvos são utilizados pela biblioteca de plot, para o plot de zonas de ativação e zonas de máxima ativação.

---
### <a name="path_save_states"></a> `path_save_states`

| Comando de Terminal  | `--path_save_states <value>`       |
| :--                  | :--                                |
| **Arquivo .cfg**     | **`path_save_states = <value>`**   |
| Tipo                 | string (path do sistema)           |
| **Valor default**    | **..\States**                      |
| Exclusivo do modo    | Test                               |


Caminho do sistema operacional (path) para a pasta no qual serão salvos os estados como uma imagem animada em formato .gif.

---

## Referências
Se esse código foi útil para sua pesquisa, por favor considere citar:
```
@misc{LVTeixeira,
  author = {Leonardo Viana Teixeira},
  title = {Desenvolvimento de um agente inteligente para exploração autônoma de ambientes 3D via Visual Reinforcement Learning},
  year = {2018},
  publisher = {GitHub},
  journal = {GitHub repository},
  url = {https://github.com/Leonardo-Viana/Reinforcement-Learning},
}
```
