A parte 4 foi feita baseando se nas aulas do professor e nos estudos feitos com o chatGPT.
O código começa importando as bibliotecas necessárias, incluindo TensorFlow e suas classes e funções relacionadas ao modelo de linguagem LSTM.
É feita a importação da função get_data do módulo data, que é responsável por obter os dados usados para treinar o modelo. O conteúdo específico do módulo data não está presente no código fornecido.
A função train_model é definida para treinar o modelo de linguagem LSTM.
Os textos são carregados usando a função get_data e armazenados na variável texts.
Um loop é usado para pré-processar os textos, removendo espaços em branco extras e espaços no início e no final de cada texto.
Um objeto Tokenizer é criado e ajustado aos textos para construir um vocabulário interno e criar índices para as palavras.
Os textos são convertidos em sequências de índices de palavras usando o Tokenizer.
O comprimento máximo de sequência entre todas as sequências é calculado.
As sequências são preenchidas para que todas tenham o mesmo comprimento usando a função pad_sequences.
É definida a dimensão do espaço de incorporação.
Um modelo sequencial é criado e configurado com uma camada de entrada, uma camada de incorporação, uma camada LSTM e uma camada densa com ativação softmax.
O modelo é compilado com a função de perda "categorical_crossentropy" e o otimizador "adam".
Os dados de entrada X e de saída y são preparados.
O modelo é treinado com os dados de entrada e saída usando o método fit.
A função generate_sentence é definida para gerar frases com base em um termo inicial usando o modelo treinado.
A frase de consulta é convertida em uma sequência de índices de palavras e preenchida para ter o mesmo comprimento máximo.
Um loop é usado para gerar palavras adicionais com base nas probabilidades previstas pelo modelo.
A saída gerada é concatenada em uma frase final.
A frase final é retornada como resultado da função generate_sentence.
Tudo isso serviu para pegarmos os conteúdos das páginas que estavam no banco de dados, tokenizá-los, treinar um modelo de rede neural com esses dados tokenizados e predizer de acordo com o modelo treinado quais seriam as próximas palavras geradas. É bom dizer que não foi feito uma ánalise da acurácia do modelo uma vez que como um problema de regressão não podemos simplesmente colocar a acurácia nas métricas e ver se funcionou. É preciso um estudo talvez perguntando para as pessoas que estão usando o bot se as frases geradas fazem sentido. Mas provavelmente a acurácia sera baixa por conta de termos poucos dados e o modelo pode não estar adequado para geração de texto.